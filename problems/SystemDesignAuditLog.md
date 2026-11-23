{: .no_toc}
# Audit Log System

> Design an audit log for a large developer platform: a permanent record of who did what, and when, that customers can search and trust.

<style>
/* Code on this page wraps instead of scrolling sideways, and the column is a little wider on desktop. */
pre, code { white-space: pre-wrap; overflow-wrap: anywhere; }
pre code { font-size: 12px; line-height: 1.45; }
@media (min-width: 961px) {
  .wrapper { width: 940px; }
  section { width: 640px; }
}
</style>

- TOC
{:toc}

### 1. What we are building

Somebody deletes a repository, adds a member to an organization, or creates an access token. A few months later a security team, or an auditor, asks: who did that, and when? The audit log is the answer to that question, and the whole value of it is that people trust it. That gives it two unusual rules. **Losing an event is never acceptable**, and **nobody can quietly change one**. Being a little slow is fine. A duplicate is fine too, because we can remove duplicates. A missing event is not.

The numbers to assume: 100 million events a day, which is about 1,200 a second on average and ten times that at peak. The log is written much more than it is read. It holds security actions, such as a repository deleted, a member added or a token created. High-volume things like Git reads are a separate, short-lived tier. Org admins read it in a UI and an API, and a stream goes to the customer's own security tools. It should be searchable within a minute, kept six months in fast storage, and longer in cheap archive.

The sentence to say first: this is append-only, write-heavy and read-rarely, and losing an event is worse than being slow.

### 2. The simplest version

The service does the action, and then writes an event saying that it did.

<details><summary markdown="span">Execute! (the simplest version)</summary>

```python
repos  = {"r1", "r2"} # the product's data
events = []           # the audit log


def delete_repo(org, actor, repo):
    repos.discard(repo) # the action

    events.append({"org": org, "actor": actor, "action": "repo.delete", "target": repo})
```

</details>
<BR>


That is the idea, and it already has the problem that shapes the whole design. The action and the event are two separate writes. If the service crashes between them, a repository is gone and nothing says who deleted it. If we swapped the order, we could log a deletion that never happened. And nothing stops somebody editing the list afterwards. The next sections fix these one at a time.

### 3. Getting the event out safely: the outbox

The fix is to make the action and its event **one change**. The service changes its data and records the event in an **outbox table in the same database transaction**. Both commit or neither does, so an action can never happen without its event.

<details><summary markdown="span">Execute! (the outbox, the relay and the consumer)</summary>

```python
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
```

</details>
<BR>


How it reads. `delete_repo` builds the event with a unique ID and a time, and then, inside one transaction, deletes the repository and inserts the event into the outbox. If anything fails in between, the rollback undoes both. A **relay** then reads the unsent rows in order, publishes each to the queue, and marks a row as sent **only after the queue confirms** it. If the queue does not confirm, the relay stops and the row stays for next time.

The consequence is **at-least-once delivery**. If the relay crashes after publishing but before marking the row, it publishes again later. That is fine, because duplicates are easy to remove: every event has a unique ID, and the consumer ignores an ID it has already stored. In the code, `INSERT OR IGNORE` on the event ID does exactly that.

Could we do at-most-once instead? Yes: mark the row sent *before* publishing. But a crash in between loses the event, and that is not acceptable for an audit log. So we choose at-least-once and remove the duplicates by event ID. Other ways to get events out, and why not: change data capture needs no relay code, but the events are tied to row changes. Publishing straight to the queue loses events if a crash falls between the change and the publish. Two-phase commit is correct in theory and slow and fragile in practice.

### 4. Where the events go

The outbox has almost no indexes, so the product's write stays fast. All the searchable indexes, by org, time, actor and action, are built **downstream**, off the critical path. We can also add or rebuild an index later by replaying events, with no change to the production database.

Between the relay and those indexes sits a **durable queue**: messages are written to disk and replicated before they are acknowledged, and kept for replay, as in Kafka. It gives us no loss, replay to rebuild an index, decoupling between the services and the consumers, and a place to absorb spikes. It costs more to operate, adds seconds of delay, orders only within a partition, and delivers duplicates. We **shard it by org**, so the events of one org stay in order, consumers work in parallel, and customers are isolated from one another. A huge org can be split across a few partitions, trading strict ordering for load. To make the queue truly durable, replicate it across zones, require acknowledgement from several replicas, and watch how far behind the consumers are. The outbox is the backstop: events stay in it until the queue acknowledges them, so even losing the queue only means publishing again.

Where the events finally land is **write-only storage**. The simplest version is that the consumers' database role can insert but never update or delete, and no human has write access. The archive goes to write-once storage in a separate account.

### 5. Making it tamper-evident

Add a **hash chain** for each org. Each event's hash covers the event and the hash of the one before it, so changing any event breaks every link after it.

<details><summary markdown="span">Execute! (a keyed hash chain, with checkpoints)</summary>

```python
KEY  = b"the chain key, kept in a key vault and never in the database"
ZERO = "0" * 64

chains = defaultdict(list) # org -> [{"event": ..., "hash": ...}, ...]


def append(org, event):
    chain    = chains[org]
    previous = chain[-1]["hash"] if chain else ZERO

    chain.append({"event": event, "hash": link(previous, event)})


def verify(org, checkpoint=None):
    previous = ZERO

    for entry in chains[org]:
        if entry["hash"] != link(previous, entry["event"]):
            return False # an event was changed, or one was removed before this one

        previous = entry["hash"]

    if checkpoint:
        return (len(chains[org]), previous) == (checkpoint["length"], checkpoint["hash"])

    return True


def make_checkpoint(org):
    chain = chains[org]
    return {"length": len(chain), "hash": chain[-1]["hash"] if chain else ZERO}


def link(previous, event):
    text = previous + json.dumps(event, sort_keys=True)
    return hmac.new(KEY, text.encode(), hashlib.sha256).hexdigest()
```

</details>
<BR>


How it reads. `append` links a new event to the last hash. `verify` walks the chain from the start, recomputes every link, and fails at the first one that does not match. That catches an edited event, a removed one, a reordered one and an inserted one. Two gaps need closing, and the code closes both. **A plain hash can be recomputed**: an attacker who edits an event just recomputes everything after it. So the hash is **keyed**, with a secret held in a key vault. Without the key an attacker cannot make a valid chain. And **cutting off the newest events** leaves a valid chain behind, because a shorter chain is still a chain. So we save periodic **checkpoints**, the length and the latest hash, somewhere the attacker cannot write, and `verify` compares against them. The customer's streamed copy is also independent evidence that we cannot alter. The honest claim is "tamper-evident and hard to tamper with", not "tamper-proof".

### 6. Finding events

Reads are by org and time, newest first, so key the index that way. Use a **cursor** and not an offset. The cursor is the time and ID of the last event the caller saw, and the next page is "everything older than that", which stays correct while new events arrive. The ID is in the cursor so that events with the same timestamp are not skipped or repeated.

<details><summary markdown="span">Execute! (query by org and time, with a cursor)</summary>

```python
def query(org, start, end, cursor=None, limit=50):
    db     = connect()
    cursor = cursor or (end, "")

    rows = db.execute("""SELECT ts, event_id, actor, action, target FROM archive
                         WHERE org = ? AND ts >= ? AND ts < ? AND (ts, event_id) < (?, ?)
                         ORDER BY ts DESC, event_id DESC LIMIT ?""",
                      (org, start, end, cursor[0], cursor[1], limit + 1)).fetchall()
    db.close()

    events      = rows[:limit]
    next_cursor = None
    if len(rows) > limit:
        next_cursor = (events[-1][0], events[-1][1])

    return {"events": events, "next_cursor": next_cursor}
```

</details>
<BR>


How it reads. It asks for one more row than the limit. If the extra row exists, there is another page, and the cursor is the last row that was returned. Exports of large ranges should be background jobs, and every query is scoped to the caller's org.

I tested all of this, including the failures: a crash between the action and its event, a relay that dies after publishing, a queue that delivers twice, a changed, removed, reordered or inserted event, a chain cut short, and pages that end among events with the same timestamp. Each rule was also broken on purpose to see that the tests notice.

### 7. Privacy, and two different keys

Audit logs are immutable, but personal data such as names and IP addresses may need to be erased. The right to erasure has legal exceptions, so confirm the specifics with legal. The approaches, in order of preference. **Log less**: IDs, not emails. Events hold an **opaque person ID**, and names and details live in an **identity service**. Erasing a person means deleting their row there, and the log is untouched. If a personal field has to stay in the event, **encrypt it with a per-person key**, kept with the identity service in the key store. To erase, **destroy the key**: the data becomes unreadable, but the chain still verifies, because the hash covers the encrypted bytes. Never put personal data in plaintext into the archive or into the hash input.

There are **two different keys** here, and they must not be confused. The **chain key**, one per org, protects the hash chain so it cannot be forged. It is kept for the life of the log, because erasing it would stop you verifying the chain. The **person key**, one per person, protects that person's personal fields. It is destroyed on an erasure request.

### 8. Edge cases and what to watch for

**The queue backs up.** Events wait safely in the outbox, and the product is not slowed down.

**The hot store is down.** The archive has everything, and the index can be rebuilt from the queue.

**The indexer lags.** Alert on how far behind the consumers are.

**Writing events needs no ingest service.** Each service writes its outbox in its own transaction, using a shared library that builds events in one consistent shape. A thin ingest API is only a fallback for services without a database.

**The APIs.** Reading: `GET /orgs/{org}/audit-log?from=&to=&actor=&action=&cursor=`. Exports: `POST /orgs/{org}/audit-log/exports`, then `GET /orgs/{org}/audit-log/exports/{id}` to check on it. Customer streaming is configured with `PUT /orgs/{org}/audit-log/streams`.

**Failing closed.** For events that must never be lost, the action should not be allowed to happen unless its event was durably saved. The outbox gives you that on the server. For the same idea on the machine that produces the logs, see [Losing logs on the server itself](SystemDesignLogAggregator.md#10-losing-logs-on-the-server-itself-the-agent-and-failing-closed).
