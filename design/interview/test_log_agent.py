"""Tests for log_agent.py: crashes, restarts, failed uploads, fail closed, and an end-to-end run into the queue store. Run: python -m unittest"""
import os
import tempfile
import unittest
from unittest import mock

import log_agent as agent
import log_queue as lq
from fake_queue import DedupQueue


def entry(n):
    return {"time": 1000 + n, "level": "INFO", "message": "line %d" % n}


class FakeServer:
    """Records every upload; can be told to fail, or to take the batch but lose the reply."""

    def __init__(self):
        self.calls = []
        self.fail_next = 0
        self.lose_reply_next = 0

    def __call__(self, batch_id, records):
        self.calls.append((batch_id, [r["seq"] for r in records]))
        if self.lose_reply_next:
            self.lose_reply_next -= 1
            return 500
        if self.fail_next:
            self.fail_next -= 1
            return 503
        return 202


class AgentTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.mkdtemp()
        agent.LOG = os.path.join(folder, "agent.log")
        agent.SENT = os.path.join(folder, "agent.sent")
        agent.last["seq"] = 0
        self.server = FakeServer()
        agent.upload = self.server

    def restart(self):
        """What a crash and restart does: all memory is gone, only the files remain."""
        agent.last["seq"] = 12345
        agent.start()

    def save_many(self, count, first=1):
        for n in range(first, first + count):
            agent.save(entry(n))

    def test_saved_lines_survive_a_crash_and_are_shipped_after_the_restart(self):
        self.save_many(120)
        self.restart()
        agent.ship()
        self.assertEqual(self.server.calls, [("1-100", list(range(1, 101)))])
        agent.ship(force=True)
        self.assertEqual(self.server.calls[-1], ("101-120", list(range(101, 121))))

    def test_sequence_numbers_continue_after_a_restart_without_reuse(self):
        self.save_many(5)
        self.restart()
        self.assertEqual(agent.save(entry(6))["seq"], 6)

    def test_batches_are_a_hundred_lines_and_the_rest_waits(self):
        self.save_many(250)
        agent.ship()
        self.assertEqual([c[0] for c in self.server.calls], ["1-100", "101-200"])
        agent.ship(force=True)
        self.assertEqual(self.server.calls[-1][0], "201-250")

    def test_nothing_ships_below_a_full_batch_unless_forced(self):
        self.save_many(99)
        agent.ship()
        self.assertEqual(self.server.calls, [])

    def test_a_failed_upload_keeps_the_lines_and_the_retry_uses_the_same_batch_id(self):
        self.save_many(100)
        self.server.fail_next = 1
        agent.ship()
        agent.ship()
        self.assertEqual([c[0] for c in self.server.calls], ["1-100", "1-100"])
        self.assertEqual(agent.read_sent(), 100)

    def test_a_lost_reply_is_resent_with_the_same_batch_id_even_after_a_restart(self):
        self.save_many(100)
        self.server.lose_reply_next = 1
        agent.ship()
        self.restart()
        agent.ship()
        self.assertEqual([c[0] for c in self.server.calls], ["1-100", "1-100"])

    def test_shipped_lines_are_not_sent_again_after_a_restart(self):
        self.save_many(100)
        agent.ship()
        self.restart()
        agent.ship(force=True)
        self.assertEqual(len(self.server.calls), 1)

    def test_a_half_written_last_line_is_ignored_and_the_numbering_carries_on(self):
        self.save_many(3)
        with open(agent.LOG, "a") as f:
            f.write('{"time": 1004, "level": "INFO", "mess')
        self.restart()
        self.assertEqual(len(agent.read_log()), 3)
        self.assertEqual(agent.last["seq"], 3)

    def test_every_save_is_forced_to_disk(self):
        with mock.patch("os.fsync", wraps=os.fsync) as fsync:
            self.save_many(4)
        self.assertEqual(fsync.call_count, 4)

    def test_fail_closed_the_action_does_not_happen_if_the_line_cannot_be_saved(self):
        done = []
        with mock.patch("builtins.open", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                agent.log_then_act(entry(1), lambda: done.append("deleted the repo"))
        self.assertEqual(done, [])

    def test_the_action_happens_after_the_line_is_saved(self):
        order = []

        def act():
            order.append(("act", len(agent.read_log())))
            return "ok"

        self.assertEqual(agent.log_then_act(entry(1), act), "ok")
        self.assertEqual(order, [("act", 1)])

    def test_an_action_that_fails_after_saving_still_has_its_log_line(self):
        def act():
            raise RuntimeError("the action failed")

        with self.assertRaises(RuntimeError):
            agent.log_then_act(entry(1), act)
        self.assertEqual(len(agent.read_log()), 1)

    def test_end_to_end_crashes_and_failures_lose_nothing_and_store_nothing_twice(self):
        lq.queue = DedupQueue(dedup_seconds=300, clock=lambda: 0.0)
        lq.DB_FILE = os.path.join(tempfile.mkdtemp(), "logs.db")
        lq.create_tables()
        failures = {"left": 2}

        def upload_to_api(batch_id, records):
            if failures["left"]:
                failures["left"] -= 1
                lq.upload_batch("acme", "web-1", batch_id, records)
                return 500  # the server took it, but the reply was lost
            return lq.upload_batch("acme", "web-1", batch_id, records)

        agent.upload = upload_to_api
        self.save_many(230)
        agent.ship()
        self.restart()
        agent.ship()
        self.save_many(15, first=231)
        self.restart()
        agent.ship(force=True)
        lq.worker()
        db = lq.connect()
        seqs = [row[0] for row in db.execute("SELECT seq FROM logs ORDER BY seq")]
        db.close()
        self.assertEqual(seqs, list(range(1, 246)))


if __name__ == "__main__":
    unittest.main()
