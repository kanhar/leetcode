import sqlite3
from log_aggregator import unpack

queue = None # a FIFO queue with deduplication, such as SQS FIFO
DB_FILE = "logs.db"


# The queue drops a second message with the same dedup_id, but only for
# its TTL (5 minutes on SQS FIFO). A retry after that is a new message.
def upload_batch(tenant, server_id, batch_id, lines):
    queue.send(dedup_id=f"{tenant}/{server_id}/{batch_id}",
               body=(tenant, server_id, lines))

    return 202 # accepted


def worker():
    for tenant, server_id, lines in queue.receive():
        store(tenant, server_id, lines)


def store(tenant, server_id, lines):
    db = connect()

    for line in lines:
        time, seq, level, message = unpack(line)
        db.execute("INSERT OR IGNORE INTO logs VALUES (?, ?, ?, ?, ?, ?)",
                   (tenant, time, server_id, seq, level, message))

    db.close()


def create_tables():
    db = connect()
    db.execute("""CREATE TABLE IF NOT EXISTS logs (
                  tenant, time, server, seq, level, message,
                  PRIMARY KEY (tenant, time, server, seq))""")
    db.close()


def connect():
    return sqlite3.connect(DB_FILE, isolation_level=None, timeout=30)
