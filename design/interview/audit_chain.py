import hashlib
import hmac
import json
from collections import defaultdict

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
