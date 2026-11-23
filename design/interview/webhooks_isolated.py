import queue
import threading
from webhooks_retry import deliver

QUEUE_SIZE = 100

queues = {}
lock = threading.Lock()


def submit(url, event):
    queue_for(url).put(event) # waits here while this endpoint's queue is full


def try_submit(url, event):
    try:
        queue_for(url).put_nowait(event)
        return True # accepted
    except queue.Full:
        return False # full: the caller keeps the event and tries later


def queue_for(url):
    with lock:
        if url not in queues:
            queues[url] = queue.Queue(maxsize=QUEUE_SIZE)
            threading.Thread(target=worker, args=(url, queues[url]), daemon=True).start()

        return queues[url]


def worker(url, events):
    while True:
        event = events.get()
        deliver(url, event)
        events.task_done()
