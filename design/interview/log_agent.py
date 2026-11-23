import json
import os

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
