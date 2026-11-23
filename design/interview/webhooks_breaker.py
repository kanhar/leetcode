import time
from collections import defaultdict

real_post = None # the real post(url, event) returning (status, retry_after)
clock = time.time

FAILS_TO_PAUSE = 5
PAUSE_SECONDS = 60

fails  = defaultdict(int)
paused = {} # url -> when it may be tried again


def post(url, event):
    if clock() < paused.get(url, 0):
        return 503, None # paused: skip the call, so a dead endpoint costs nothing

    status, retry_after = real_post(url, event)

    if status == 0 or status >= 500:
        fails[url] += 1
    else:
        fails[url] = 0

    if fails[url] >= FAILS_TO_PAUSE:
        paused[url] = clock() + PAUSE_SECONDS
        fails[url] = 0

    return status, retry_after
