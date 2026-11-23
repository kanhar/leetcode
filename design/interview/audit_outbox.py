import json
import sqlite3
import time
import uuid
from contextlib import contextmanager

DB_FILE = "audit.db"

new_id = lambda: str(uuid.uuid4())
now    = lambda: int(time.time() * 1000)


def delete_repo(org, actor, repo):
    event = {"event_id": new_id(), "ts": now(), "org": org, "actor": actor,
             "action": "repo.delete", "target": repo}

    with transaction() as db:
        db.execute("DELETE FROM repos WHERE id = ?", (repo,))
        db.execute("INSERT INTO outbox (event_id, payload, sent) VALUES (?, ?, 0)",
                   (event["event_id"], json.dumps(event)))


def relay(publish):
    db   = connect()
    rows = db.execute("SELECT event_id, payload FROM outbox WHERE sent = 0 ORDER BY rowid").fetchall()

    for event_id, payload in rows:
        if not publish(payload):
            break # the queue did not confirm it: leave it, and try again next time

        db.execute("UPDATE outbox SET sent = 1 WHERE event_id = ?", (event_id,))

    db.close()


def consume(payload):
    event = json.loads(payload)
    db    = connect()

    db.execute("INSERT OR IGNORE INTO archive VALUES (?, ?, ?, ?, ?, ?, ?)",
               (event["event_id"], event["ts"], event["org"], event["actor"],
                event["action"], event["target"], payload)) # a repeat of an event_id is ignored

    db.close()


@contextmanager
def transaction():
    db = connect()
    db.execute("BEGIN")
    try:
        yield db
        db.execute("COMMIT")
    except BaseException:
        db.execute("ROLLBACK") # the action and its event both vanish, or neither
        raise
    finally:
        db.close()


def create_tables():
    db = connect()
    db.execute("CREATE TABLE IF NOT EXISTS repos (id PRIMARY KEY)")
    db.execute("CREATE TABLE IF NOT EXISTS outbox (event_id PRIMARY KEY, payload, sent)")
    db.execute("""CREATE TABLE IF NOT EXISTS archive (
                  event_id PRIMARY KEY, ts, org, actor, action, target, payload)""")
    db.close()


def connect():
    return sqlite3.connect(DB_FILE, isolation_level=None, timeout=30)
