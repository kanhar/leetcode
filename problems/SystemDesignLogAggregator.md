{: .no_toc}
# Log Aggregator

> Many servers send their logs to one place every minute. Design the API to upload them, and the API to get back all the logs, merged and sorted by time.

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

Every server collects its own log lines and, once a minute, sends the new ones to a central service. Later, someone asks for "everything between 10:00 and 10:05, in time order, from all servers". That gives us two separate jobs: taking logs in, and handing logs out. We design each one on its own.

"Aggregate" here means one merged stream sorted by time. It does not mean counting things, such as errors per minute. That would be a different question.

### 2. The upload API

Each server sends one batch a minute: the lines it has written since the last batch.

```
PUT /v1/tenants/{tenant}/servers/{server_id}/batches/{batch_id}

{ "lines": [
    {"time": 1792922400120, "seq": 41,
     "level": "ERROR", "message": "..."},
    {"time": 1792922401450, "seq": 42,
     "level": "INFO", "message": "..."}
] }
```

The server makes up the `batch_id` (a GUID) for each batch. If the reply is lost and the server sends the same batch again, we recognise the ID and do not store the lines twice. Without this, every network hiccup would create duplicate logs. It is the same idea as the scan ID in [Remote Scans API](SystemDesignScanApi.md).

Each line carries its time, and a `seq`: its position in that server's own log, counting up. The sequence number settles the order when two lines have the same timestamp.

**Times are epoch milliseconds, always UTC:** a whole number counting milliseconds since 1 January 1970, like `1792922400120`, so there are no time zones or daylight saving to get wrong. Epoch seconds is the same count divided by 1,000 (10 digits, `1792922400`); we use milliseconds because logs need finer than one second, and a whole number avoids the rounding of decimals like `1792922400.12`.

The answer is `202 Accepted`. A batch that is empty or too large gets `400`. As always, there is a bearer token, the tenant must match the token, and too many requests get `429`.

### 3. What happens to a batch, and how we store it

We do not write straight into the final storage. The API checks the token and the batch, puts it on a queue, and answers. Workers then take batches off the queue and store the lines. If a thousand servers send at the same moment, the queue absorbs the spike and the API stays fast.

Lines are stored by tenant, and each tenant's table has an **index on (tenant, time)**. The index keeps the rows in time order, and that is the answer to "how do we sort?": if the data is kept in sorted order when it is stored, then reading a range comes back sorted for free. Nothing needs merging at query time. A time-series database, or any store with a sorted index, works this way. A late line simply slots into its place in the order.

Every row also carries two extra fields: the `server` it came from and its `seq`, the line's position in that server's own log. They are not part of finding the range. They are tie-breakers, for when two lines have exactly the same timestamp (see the edge cases at the end).

The data is also split into buckets by time, say one per hour per tenant. A question about 10:00 to 10:05 then looks at one bucket and ignores everything else we have ever stored.

### 4. The query API

```
GET /v1/tenants/{tenant}/logs
    ?from=1792922400000
    &to=1792922700000
```

`from` and `to` are required epoch milliseconds: `from` is included and `to` is not, so consecutive ranges never overlap or leave a gap. The answer is the lines in time order:

```
{ "lines": [
    {"time": 1792922400120, "server": "web-1",
     "level": "INFO", "message": "..."},
    ...
] }
```

This is the first version: it returns everything in the range. A range with millions of lines is the subject of section 7.

Errors are the usual ones: `400` for a missing or bad time range, `401` for no token, `404` for a tenant that does not match the token, and `429` when throttled.

### 5. A simple implementation

This keeps everything in memory, with one sorted list per tenant. In an interview the shape matters more than the details: an upload that ignores repeats and stores the lines, and a query that finds the start, reads forward, and stops at the end time. `SortedList` (from the `sortedcontainers` package, import not shown) is a list that keeps itself in order as items are added. It stands in for the database index from section 3, so the code never sorts anything itself.

<details><summary markdown="span">Execute! (upload and query, in memory)</summary>

```python
logs = defaultdict(SortedList)
seen = set()


def upload_batch(tenant, server_id, batch_id, lines):
    if (tenant, server_id, batch_id) in seen:
        return 200 # OK

    seen.add((tenant, server_id, batch_id))

    for line in lines:
        time, seq, level, message = unpack(line)
        logs[tenant].add((time, server_id, seq, level, message))

    return 202 # accepted


def get_logs(tenant, start, end):
    first = logs[tenant].bisect_left((start,))
    last  = logs[tenant].bisect_left((end,))

    lines = []
    for time, server, seq, level, message in logs[tenant][first:last]:
        lines.append({"time": time,   "server": server,
                      "level": level, "message": message})

    return lines # Or json.dumps(lines) if you want to return JSON


def unpack(line):
    return line["time"], line["seq"], line["level"], line["message"]
```

</details>
<BR>


How it reads. `logs` holds each tenant's lines (a `defaultdict` makes the tenant's empty sorted list the first time it is used), and `seen` remembers the batch IDs already stored. `upload_batch` returns early for a repeat. Otherwise it unpacks each line with the small helper `unpack`, and adds it to the tenant's sorted list, which puts it in the right place. A real service would also reject an empty or oversized batch, and would put the batch on a queue before storing it. This first version leaves those out, and section 8 adds the checks.

`get_logs` asks the sorted list for two positions. `bisect_left` is a binary search: it returns the position where a value would sit in the sorted list, without reading anything on the way. So `first` is the position of the first line at or after `start`, and `last` is the position of the first line at or after `end`. Everything between them, `rows[first:last]`, is exactly the lines in the range, the same way `range(first, last)` gives the numbers between two values. Each stored row is unpacked into named variables, so the loop reads like plain English. The limit and the cursor come later, in section 7.

I ran this against a deliberately simple reference that filters and sorts everything on each query, on a few hundred random sets of uploads, retries and queries. The answers always matched.

### 6. The numbers

Suppose 1,000 servers send about 1,000 lines a minute each. That is roughly a million lines a minute, or about 17,000 a second. At around 200 bytes a line it is about 200 MB a minute, which is roughly 290 GB a day.

So the real version needs compression, a stated retention period such as 30 days, and storage that can be spread across machines by tenant and by time. It also explains why the queue matters: ingest must be able to absorb bursts without losing data or slowing the servers.

### 7. Extending it

**What if the answer does not fit in memory?** The first version builds the whole answer in memory, so a range with millions of lines, such as a month of logs for an investigation, would not fit. There are three ways to deal with that.

*Pagination* is the first one to reach for. The client asks for at most `limit` lines, and the answer includes a **cursor** whenever there is more. The client processes the page and asks again with `cursor=...` to get the next one. The cursor is a marker for the last line returned: its time, server and sequence number, packaged as one opaque string, like `MTc5MjkyMjQwMDEyMHx3ZWItMXw0Mg==`. It is encoded (here as base64 text), not hashed, because a hash cannot be turned back and the server has to read the cursor again. Clients treat it as a sealed string and never open it. The snippet below returns the cursor as a plain tuple, and the REST layer encodes it on the way out and decodes it on the way in. To stop anyone editing a cursor, the server can also sign it and reject one that does not check out. When `next_cursor` is missing there is nothing more. Here is `get_logs` with the limit and the cursor added:

<details><summary markdown="span">Execute! (get_logs with a limit and a cursor)</summary>

```python
def get_logs_page(tenant, start, end, limit=500, cursor=None):
    first = logs[tenant].bisect_left((start,))
    last  = logs[tenant].bisect_left((end,))

    if cursor:
        time, server, seq = cursor
        first = logs[tenant].bisect_left((time, server, seq + 1))

    stop = min(last, first + limit)

    lines = []
    for time, server, seq, level, message in logs[tenant][first:stop]:
        lines.append({"time": time,   "server": server,
                      "level": level, "message": message})

    next_cursor = None
    if stop < last:
        time, server, seq, level, message = logs[tenant][stop - 1]
        next_cursor = (time, server, seq)

    return {"lines": lines, "next_cursor": next_cursor}
```

</details>
<BR>


Two things are new. If there is a cursor, reading starts just after it: `seq + 1` means "the position right after that line", and it still works if that line has since been deleted. And the page is cut at `first + limit`, or at the end of the range if that comes sooner. When lines are left over, the key of the last line returned becomes the next cursor.

A cursor is better than page numbers here because new logs keep arriving. With page numbers, a new line near the start would push everything down and the next page would repeat a line. A cursor always means "continue after this exact line". Pagination is simple, the server remembers nothing between requests, and if anything fails the client just retries from the last cursor. Any client can use it, over plain HTTP. The downsides are many round trips, so it can be slow for huge results, and the data can change between pages, because late lines may arrive while the client is reading.

*Streaming* means the server sends lines continuously, over one long response, as it reads them, and the client processes them as they arrive. Memory stays small on both sides, and there is no waiting for round trips, so it is fast. The downsides are that one long connection ties up the server for the whole time, a slow client holds that connection open and wastes server resources, proxies and timeouts tend to cut long responses, and if the connection breaks halfway the client has to start again, unless every line carries a cursor so it can resume. Streaming is the natural fit for following logs live as they arrive.

*An export job* is the third way, and it is the scan pattern again. The client asks for an export of a time range with a `PUT` and an ID it chose, and the server answers `202`. A worker writes the results to a file in cheap storage, and the client checks the status and then downloads the file from a link. There are no long connections and no memory pressure, a failure only restarts the job, and the file can be compressed. The downsides are the delay before the file is ready, the cost of storing it, and the need to delete old exports.

What I would say: keep the paged API for looking around, offer an export job for "give me everything", and use streaming only for following logs live.

### 8. The REST API in code

So far there are two plain functions. This is the thin layer on top that turns HTTP into calls to them. It does three jobs: read the JSON body and the URL parameters, refuse anything malformed, and call `upload_batch` or `get_logs`.

<details><summary markdown="span">Execute! (the REST layer, with Flask)</summary>

```python
app = Flask(__name__)

FIELDS = {"time", "seq", "level", "message"}


@app.put("/v1/tenants/<tenant>/servers/<server_id>/batches/<batch_id>")
def put_batch(tenant, server_id, batch_id):
    body = request.get_json(silent=True)

    if not body or not body.get("lines"):
        return {"error": "send JSON with a lines list"}, 400

    if len(body["lines"]) > 5000:
        return {"error": "at most 5000 lines per batch"}, 413

    if not all(is_good(line) for line in body["lines"]):
        return {"error": "each line needs time, seq, level, message"}, 400

    status = upload_batch(tenant, server_id, batch_id, body["lines"])
    return {"batch_id": batch_id}, status


@app.get("/v1/tenants/<tenant>/logs")
def read_logs(tenant):
    start = request.args.get("from", type=int)
    end   = request.args.get("to",   type=int)

    if start is None or end is None:
        return {"error": "from and to are required whole numbers"}, 400

    return {"lines": get_logs(tenant, start, end)}


def is_good(line):
    return (isinstance(line, dict)
            and FIELDS <= line.keys()
            and isinstance(line["time"], int)
            and isinstance(line["seq"], int))
```

</details>
<BR>


How it reads. The upload is a `PUT`, with the tenant, server and batch ID in the URL and the lines in the JSON body. `request.get_json(silent=True)` gives back nothing, instead of crashing, if the body is not valid JSON. Then come three guards, each answering with a clear message. No lines is a `400`. More than 5,000 lines is a `413`, meaning too large. A line that is missing a field, or has a time or sequence number that is not a whole number, is a `400`. Only then does it call `upload_batch`, and it passes along the status that function chose: `202` for a new batch, `200` for a repeat.

The lines are checked here, and not left to `upload_batch`, for a reason. `upload_batch` adds lines one at a time, so a bad line halfway through would leave half a batch stored while the batch ID is already remembered. A retry would then be told "200, I already have it", and the missing lines would be lost for good. So the whole batch is checked before anything is stored.

The read is a `GET`. The tenant comes from the URL path, and `from` and `to` come from the URL parameters, as whole numbers. If either is missing, or is not a whole number, the answer is `400`. Otherwise it returns `{"lines": [...]}`, which Flask turns into JSON. A range with nothing in it is an empty list, not an error.

What this layer leaves out is the token check, matching the tenant in the URL to the token, and throttling. They sit in front of both routes, as described in [Remote Scans API](SystemDesignScanApi.md), and every error should use the same shape.

### 9. Running on more than one server: the race condition

In the code so far, `seen` and `logs` are in memory, in one process. With several API servers they cannot stay there. A retry can arrive while the original is still being handled, and the two requests can land on two different servers at the same moment. If each one does "check whether we have seen this batch, then store it", both checks say "not seen", and the lines are stored twice.

The fix is to stop making the API servers decide. Put one shared queue between the API and the storage, and let the queue do the deduplicating. Each message carries a **dedup ID** built from the tenant, the server and the batch ID. The queue is one place for all the API servers, so it does not matter which server got which copy. The queue drops a second message with the same dedup ID, and it does that check in one atomic step, so there is no race. The API just sends the message and answers `202`.

<details><summary markdown="span">Execute! (upload through a deduplicating queue)</summary>

```python
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
```

</details>
<BR>


How it reads. `upload_batch` no longer touches the data. It puts the batch on the queue with its dedup ID, and answers `202` straight away. A separate `worker` takes messages off the queue and calls `store`, which writes each line into the shared table. The table's primary key is tenant, time, server and sequence number, and `INSERT OR IGNORE` skips a line that is already there.

The comment above `upload_batch` is the important caveat. The queue only remembers a dedup ID for a limited time, called its TTL, which is 5 minutes on an SQS FIFO queue. A retry that arrives after that is treated as a new message. A server that was offline for an hour and then retries a batch will get through the queue a second time.

That is why the last step matters. A queue usually delivers a message at least once, and sometimes twice, for example when a worker crashes before confirming it. So `store` has to be safe to repeat, and it is: a line that is already stored is ignored, so storing the same batch twice changes nothing. The queue's dedup saves work in the common case, and the table's primary key keeps the data correct in every case.

This needs no database transaction. If a worker crashes halfway through a batch, the queue hands the message to another worker. The lines that were already stored are ignored, and the rest are stored, so the batch ends up complete.

One thing changes for the client. The API can no longer tell a new batch from a repeat when it answers, because all it did was send a message. So it returns `202` for both, and the `200` for a repeat is gone. The agent does not mind, since both mean "done, stop retrying".

**Big batches.** A batch can be around 1 MB, which some queues refuse, and every redelivery copies it again. So save the lines in object storage (such as S3) under a key made from the tenant, server and batch ID, and send the queue only that key. The worker reads the lines from storage. For smaller sizes, compressing the batch or splitting it into smaller messages can be enough. The costs are one more system, and a rule that deletes old batches after a few days.

### 10. Losing logs on the server itself: the agent, and failing closed

Everything so far starts when a batch reaches the API. But the agent on each server collects lines, say 100 of them, before it sends a batch. If it keeps them in memory and the server crashes, those lines are gone for good. And a server that is crashing is exactly the one whose last log lines you most want.

The first fix is to write each line to a file on the server's own disk before doing anything else, force it onto the disk (`fsync`), and ship only from that file. A second small file remembers how far the shipping got. After a crash and a restart the agent reads both files and carries on. A few details make this work. The batch ID is the range of sequence numbers it contains, like `1-100`, so after a crash, or a lost reply, the same lines go out under the same batch ID and the deduplication in section 9 does its job. If the agent sends a short batch because a minute passed, and then more lines are added before a retry, the same lines can arrive under two different batch IDs. The line's primary key from section 9 makes that harmless. A crash in the middle of a write leaves half a line at the end of the file, and the agent ignores it. That is safe for a reason explained below. Lines that have been shipped are deleted later by rotating the file, which is not shown.

What this still loses is lines on a disk or a machine that is destroyed before they were shipped. You can shrink that window by shipping more often. You cannot close it, because there is always some time between writing a line and shipping it.

If you really must never lose a log line, which is a requirement for something like GitHub's audit log, the only way to guarantee it is to **fail closed**: write the log line durably first, and only if that succeeds, do the action. If the line cannot be saved, the action does not happen. Any design that acts first and logs afterwards has a gap in which the action happened and its log was lost. This is the same idea as the outbox in [Audit Log System](SystemDesignAuditLog.md).

<details><summary markdown="span">Execute! (the agent: save to disk first, ship in batches, fail closed)</summary>

```python
LOG = "agent.log"
SENT = "agent.sent"
BATCH = 100

last = {"seq": 0}
upload = None # upload(batch_id, records) returns the HTTP status of the PUT


def start():
    records = read_log()
    last["seq"] = records[-1]["seq"] if records else 0


def save(line):
    record = dict(line, seq=last["seq"] + 1)

    with open(LOG, "a") as f:
        f.write(json.dumps(record) + "\n")
        f.flush()
        os.fsync(f.fileno()) # on disk before we return

    last["seq"] = record["seq"]
    return record


def log_then_act(line, act):
    save(line) # raises if the line cannot be saved, so the action never happens
    return act()


def ship(force=False):
    sent   = read_sent()
    unsent = [r for r in read_log() if r["seq"] > sent]

    while unsent and (len(unsent) >= BATCH or force):
        batch    = unsent[:BATCH]
        unsent   = unsent[BATCH:]
        batch_id = f"{batch[0]['seq']}-{batch[-1]['seq']}"

        if upload(batch_id, batch) not in (200, 202):
            return # still on disk, the next try sends the same batch again

        write_sent(batch[-1]["seq"])


def read_log():
    records = []

    if not os.path.exists(LOG):
        return records

    for text in open(LOG):
        try:
            records.append(json.loads(text))
        except ValueError:
            break # a half-written last line: its action never happened

    return records


def read_sent():
    if not os.path.exists(SENT):
        return 0

    return int(open(SENT).read())


def write_sent(seq):
    with open(SENT + ".tmp", "w") as f:
        f.write(str(seq))
        f.flush()
        os.fsync(f.fileno())

    os.replace(SENT + ".tmp", SENT)
```

</details>
<BR>


How it reads. `save` appends the line to the file and forces it to disk before it returns, and gives the line the next sequence number. `log_then_act` calls `save` first. If `save` raises an error, for example because the disk is full, the action is never called. `ship` reads the lines that have not been shipped yet, cuts them into batches of 100, and uploads each one. It writes down how far it got only after the server said yes, so a failed upload leaves the lines on disk and the next try sends the same batch again. `start` runs after a restart and picks the sequence numbers up where they left off.

The order matters. The log line is written before the action. If the server crashes in between, there is a log line for something that did not happen, and that is acceptable, because the opposite, an action with no log, is the failure we cannot allow. It also explains why a half-written line can be ignored: `save` had not returned, so its action never started. If you also need to know that the action finished, write a second line afterwards. An "attempted" line with no "completed" line is a signal to go and check.

How safe "saved" really is depends on where it was saved. A line that is forced to the local disk survives a crash of the program and a reboot, but not the loss of the machine. To survive that as well, `save` has to wait until another machine confirms it has the line, for example a replicated queue that answers once a majority has it, before the action may go ahead. That adds a network round trip to every action.

The costs are real. If the logging can no longer save lines, the actions stop. That is a choice of consistency over availability, the same trade as in [Git Storage (Spokes)](SystemDesignSpokes.md), where a write that cannot be made safe is refused. And every action now waits for a durable write. You can soften that by letting several actions share one `fsync`, and by failing closed only for the events that must never be lost, such as permission changes, deletions and sign-ins. Ordinary debug logs stay best-effort and batched.

What I would say: keep the buffer on disk and not in memory, with batch IDs that repeat exactly on a retry. For events that must never be lost, write the log durably before the action and refuse the action if it cannot be written, accepting the cost in availability and speed.

### 11. Edge cases and what to watch for

**Late logs.** A server that was offline uploads logs from 10:01 at 10:09. We sort by the time the event happened, not by when it arrived, so the lines slot into the right place. But anyone who already ran a query for 10:00 to 10:05 missed them. Say clearly that recent results can still change for a while, and that logs show up a minute or so after they happen, because of the batches and the queue.

**Two lines with the same timestamp.** Which one comes first does not matter, but the order must be the same every time (time, then server, then sequence number), so the cursor can point at exactly one line. A cursor of just "after this time" would skip or repeat the other lines that share it.

**Clocks that disagree.** Two servers can differ by a few seconds, so the merged order across servers is only approximate. Within one server it is exact, which is what the sequence number is for. Keeping servers' clocks in sync with NTP keeps the error small.

**Duplicates.** The batch ID handles a repeated batch. A batch ID reused for different lines is a bug on the agent's side, and the second batch would be silently dropped, so every new batch needs a new ID.

**Running on more than one server.** `seen` and `logs` live inside one process, so a second API server would know nothing about what the first one stored. Both have to move into storage that every server can reach, and a retry that reaches two servers at the same moment must not be stored twice. Section 9 shows how.

**One huge batch, or a huge query.** Cap the number of lines in a batch and the size of the time range in a query. A query for a whole year must be refused or must go through the cursor in small pages.

**A server coming back after an outage.** It may send hours of logs at once. Accept them in several batches, throttle if needed, and let the queue smooth it out.

**One noisy tenant.** A tenant sending far more than others should be throttled, and limited in how much it can read, so it cannot slow everyone else.

**Reading while writing.** New lines arrive during a query. The cursor makes this safe: each page continues after an exact line, so nothing repeats, and a line that arrives later in the range may simply appear on a later page, or not at all if it sorts before the cursor.

**Old data deleted by retention.** A cursor pointing at deleted data should still work, by continuing from the next line that exists.

**Secrets in logs.** Logs often contain tokens, passwords and personal data by accident. Consider scrubbing on the server before uploading, and make sure every query checks the tenant.

**Which server did a line come from?** Each line is stored with its server ID, and every line in the answer shows it, so the merged stream still tells you where each line came from.
