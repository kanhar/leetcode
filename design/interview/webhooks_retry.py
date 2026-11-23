import random
import time

post = None # post(url, event) returns (status, retry_after); status 0 means no answer at all
sleep = time.sleep
jitter = random.uniform

MAX_TRIES = 8
BASE = 1.0
CAP = 3600.0

dead_letters = []


def deliver(url, event):
    for attempt in range(MAX_TRIES):
        status, retry_after = post(url, event)

        if 200 <= status < 300:
            return True # delivered

        if not worth_retrying(status):
            break # the endpoint is set up wrongly, trying again will not help

        if attempt < MAX_TRIES - 1:
            sleep(wait_time(attempt, retry_after))

    dead_letters.append((url, event))
    return False


def worth_retrying(status):
    return status == 0 or status in (408, 429) or status >= 500


def wait_time(attempt, retry_after):
    if retry_after:
        return retry_after # the endpoint told us how long to wait

    ceiling = min(CAP, BASE * 2 ** attempt)
    return jitter(0, ceiling)
