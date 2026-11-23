import math
import threading
import time
from flask import g
from scan_simple import app, error

clock = time.monotonic

BURST      = 10  # requests a token may make at once
PER_SECOND = 5.0 # and how fast the allowance refills

buckets = {} # token -> (requests left, when we last looked)
lock    = threading.Lock()


@app.before_request
def throttle():
    with lock:
        now = clock()
        left, last = buckets.get(g.token, (BURST, now))
        left = min(BURST, left + (now - last) * PER_SECOND)

        if left >= 1:
            buckets[g.token] = (left - 1, now)
            return # allowed

        buckets[g.token] = (left, now)
        wait = math.ceil((1 - left) / PER_SECOND)

    body, status = error(429, "rate_limited", "too many requests")
    return body, status, {"Retry-After": str(wait)}
