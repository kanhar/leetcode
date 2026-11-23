"""Tests for log_queue.py, using the in-memory stand-in queue in fake_queue.py. Run: python -m unittest"""
import os
import tempfile
import threading
import unittest

import log_queue as lq
from fake_queue import DedupQueue


class FakeClock:
    def __init__(self):
        self.now = 1000.0

    def __call__(self):
        return self.now


def line(time, seq, message="x"):
    return {"time": time, "seq": seq, "level": "INFO", "message": message}


def stored_rows():
    db = lq.connect()
    rows = db.execute("SELECT tenant, time, server, seq FROM logs ORDER BY tenant, time, server, seq").fetchall()
    db.close()
    return rows


class QueueDedupTests(unittest.TestCase):
    def setUp(self):
        self.clock = FakeClock()
        lq.queue = DedupQueue(dedup_seconds=300, clock=self.clock)
        lq.DB_FILE = os.path.join(tempfile.mkdtemp(), "logs.db")
        lq.create_tables()
        self.real_unpack = lq.unpack

    def tearDown(self):
        lq.unpack = self.real_unpack

    def test_upload_answers_202_and_stores_nothing_until_the_worker_runs(self):
        self.assertEqual(lq.upload_batch("t", "s", "b1", [line(1, 0)]), 202)
        self.assertEqual(stored_rows(), [])
        lq.worker()
        self.assertEqual(stored_rows(), [("t", 1, "s", 0)])

    def test_a_repeat_within_the_ttl_is_dropped_by_the_queue(self):
        self.assertEqual(lq.upload_batch("t", "s", "b1", [line(1, 0)]), 202)
        self.assertEqual(lq.upload_batch("t", "s", "b1", [line(1, 0)]), 202)
        self.assertEqual(lq.queue.sent, 1)
        self.assertEqual(lq.queue.dropped, 1)
        lq.worker()
        self.assertEqual(len(stored_rows()), 1)

    def test_a_repeat_after_the_ttl_gets_through_the_queue_but_changes_nothing(self):
        lq.upload_batch("t", "s", "b1", [line(1, 0), line(2, 1)])
        lq.worker()
        self.clock.now += 301
        lq.upload_batch("t", "s", "b1", [line(1, 0), line(2, 1)])
        self.assertEqual(lq.queue.sent, 2)
        lq.worker()
        self.assertEqual(len(stored_rows()), 2)

    def test_forty_simultaneous_copies_put_exactly_one_message_on_the_queue(self):
        results = []
        lock = threading.Lock()

        def call():
            code = lq.upload_batch("t", "s", "b1", [line(i, i) for i in range(20)])
            with lock:
                results.append(code)

        threads = [threading.Thread(target=call) for _ in range(40)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(results, [202] * 40)
        self.assertEqual(lq.queue.sent, 1)
        lq.worker()
        self.assertEqual(len(stored_rows()), 20)

    def test_the_dedup_id_includes_tenant_server_and_batch(self):
        lq.upload_batch("a", "s", "b", [line(1, 0)])
        lq.upload_batch("b", "s", "b", [line(1, 0)])
        lq.upload_batch("a", "t", "b", [line(1, 0)])
        lq.upload_batch("a", "s", "c", [line(1, 1)])
        self.assertEqual(lq.queue.sent, 4)
        lq.worker()
        self.assertEqual(len(stored_rows()), 4)

    def test_a_message_delivered_twice_is_stored_once(self):
        lq.upload_batch("t", "s", "b1", [line(1, 0), line(2, 1)])
        lq.worker()
        lq.queue.waiting.append(("t", "s", [line(1, 0), line(2, 1)]))
        lq.worker()
        self.assertEqual(len(stored_rows()), 2)

    def test_a_worker_that_dies_halfway_is_finished_by_the_redelivery(self):
        lq.upload_batch("t", "s", "b1", [line(i, i) for i in range(5)])
        calls = {"count": 0}

        def flaky_unpack(one):
            calls["count"] += 1
            if calls["count"] == 3:
                raise RuntimeError("worker crashed")
            return self.real_unpack(one)

        lq.unpack = flaky_unpack
        with self.assertRaises(RuntimeError):
            lq.worker()
        self.assertEqual(len(stored_rows()), 2)
        lq.unpack = self.real_unpack
        lq.queue.redeliver_unacked()
        lq.worker()
        self.assertEqual(len(stored_rows()), 5)

    def test_two_workers_at_once_still_store_each_line_once(self):
        lq.upload_batch("t", "s", "b1", [line(i, i) for i in range(30)])
        lq.queue.waiting.append(lq.queue.waiting[0])
        threads = [threading.Thread(target=lq.worker) for _ in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(len(stored_rows()), 30)


if __name__ == "__main__":
    unittest.main()
