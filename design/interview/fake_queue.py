"""A small in-memory stand-in for a FIFO queue with deduplication (like SQS FIFO), for tests.

 - send(): a message whose dedup_id was already sent within `dedup_seconds` is dropped
 - receive(): hands out messages one at a time; a message counts as handled only once the caller
   has finished with it. If the caller fails halfway, it stays "in flight" until redeliver_unacked()
   puts it back, which is what happens when a real queue's visibility timeout runs out.
"""
import threading


class DedupQueue:
    def __init__(self, dedup_seconds=300, clock=None):
        self.dedup_seconds = dedup_seconds
        self.clock = clock
        self.lock = threading.Lock()
        self.recent = {}
        self.waiting = []
        self.in_flight = []
        self.sent = 0
        self.dropped = 0

    def send(self, dedup_id, body):
        with self.lock:
            now = self.clock()
            sent_at = self.recent.get(dedup_id)
            if sent_at is not None and now - sent_at < self.dedup_seconds:
                self.dropped += 1
                return False
            self.recent[dedup_id] = now
            self.waiting.append(body)
            self.sent += 1
            return True

    def receive(self):
        while True:
            with self.lock:
                if not self.waiting:
                    return
                body = self.waiting.pop(0)
                self.in_flight.append(body)
            yield body
            # the caller finished its loop body without failing, so the message is handled
            with self.lock:
                self.in_flight.remove(body)

    def redeliver_unacked(self):
        with self.lock:
            self.waiting = self.in_flight + self.waiting
            self.in_flight = []
