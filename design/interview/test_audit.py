"""Tests for the audit log files: audit_simple, audit_outbox, audit_chain and audit_query. Run: python -m unittest"""
import json
import os
import random
import tempfile
import unittest
from unittest import mock

import audit_chain as chain
import audit_outbox as outbox
import audit_query as querying
import audit_simple as simple


def table(sql):
    db = outbox.connect()
    rows = db.execute(sql).fetchall()
    db.close()
    return rows


class BrokenList(list):
    def append(self, item):
        raise RuntimeError("crash between the action and the event")


class SimpleTests(unittest.TestCase):
    def setUp(self):
        simple.repos.clear()
        simple.repos.update({"r1", "r2"})
        simple.events.clear()

    def test_the_action_and_its_event(self):
        simple.delete_repo("acme", "alice", "r1")
        self.assertEqual(simple.repos, {"r2"})
        self.assertEqual(simple.events, [{"org": "acme", "actor": "alice", "action": "repo.delete", "target": "r1"}])

    def test_the_weakness_a_crash_between_the_two_loses_the_event(self):
        with mock.patch("audit_simple.events", new=BrokenList()):
            with self.assertRaises(RuntimeError):
                simple.delete_repo("acme", "alice", "r1")
        self.assertEqual(simple.repos, {"r2"}) # the repo is gone
        self.assertEqual(simple.events, [])    # and nothing says who did it


class OutboxTests(unittest.TestCase):
    def setUp(self):
        outbox.DB_FILE = os.path.join(tempfile.mkdtemp(), "audit.db")
        outbox.create_tables()
        db = outbox.connect()
        db.execute("INSERT INTO repos VALUES ('r1'), ('r2'), ('r3')")
        db.close()
        self.counter = 0
        self.clock = 1000

        def new_id():
            self.counter += 1
            return "evt-%03d" % self.counter

        def now():
            self.clock += 1
            return self.clock

        outbox.new_id = new_id
        outbox.now = now

    def test_the_action_and_its_event_are_saved_together(self):
        outbox.delete_repo("acme", "alice", "r1")
        self.assertEqual(table("SELECT id FROM repos ORDER BY id"), [("r2",), ("r3",)])
        rows = table("SELECT event_id, sent FROM outbox")
        self.assertEqual(rows, [("evt-001", 0)])
        self.assertEqual(json.loads(table("SELECT payload FROM outbox")[0][0])["actor"], "alice")

    def test_if_the_event_cannot_be_saved_the_action_does_not_happen(self):
        with mock.patch("audit_outbox.json.dumps", side_effect=RuntimeError("crash")):
            with self.assertRaises(RuntimeError):
                outbox.delete_repo("acme", "alice", "r1")
        self.assertEqual(table("SELECT id FROM repos ORDER BY id"), [("r1",), ("r2",), ("r3",)])
        self.assertEqual(table("SELECT * FROM outbox"), [])

    def test_if_the_action_fails_no_event_is_left_behind(self):
        outbox.new_id = lambda: "same"
        outbox.delete_repo("acme", "alice", "r1")
        with self.assertRaises(Exception):
            outbox.delete_repo("acme", "alice", "r2") # the second insert breaks the unique event id
        self.assertEqual(table("SELECT id FROM repos ORDER BY id"), [("r2",), ("r3",)])
        self.assertEqual(len(table("SELECT * FROM outbox")), 1)

    def test_the_relay_publishes_in_order_and_marks_each_one_sent(self):
        for repo in ("r1", "r2", "r3"):
            outbox.delete_repo("acme", "alice", repo)
        published = []
        outbox.relay(lambda payload: published.append(json.loads(payload)["target"]) or True)
        self.assertEqual(published, ["r1", "r2", "r3"])
        self.assertEqual(table("SELECT sent FROM outbox"), [(1,), (1,), (1,)])
        outbox.relay(lambda payload: published.append("again") or True)
        self.assertEqual(len(published), 3)

    def test_an_event_the_queue_did_not_confirm_stays_and_is_sent_next_time(self):
        for repo in ("r1", "r2"):
            outbox.delete_repo("acme", "alice", repo)
        outbox.relay(lambda payload: False)
        self.assertEqual(table("SELECT sent FROM outbox"), [(0,), (0,)])
        published = []
        outbox.relay(lambda payload: published.append(payload) or True)
        self.assertEqual(len(published), 2)

    def test_a_crash_after_publishing_and_before_marking_sends_it_again_and_the_consumer_ignores_the_repeat(self):
        outbox.delete_repo("acme", "alice", "r1")
        delivered = []

        def publish_then_crash(payload):
            delivered.append(payload)
            raise RuntimeError("the relay crashed before it could mark the row")

        with self.assertRaises(RuntimeError):
            outbox.relay(publish_then_crash)
        self.assertEqual(table("SELECT sent FROM outbox"), [(0,)])
        outbox.relay(lambda payload: delivered.append(payload) or True)
        self.assertEqual(len(delivered), 2)
        for payload in delivered:
            outbox.consume(payload)
        self.assertEqual(len(table("SELECT * FROM archive")), 1)

    def test_different_events_are_all_stored(self):
        for repo in ("r1", "r2", "r3"):
            outbox.delete_repo("acme", "alice", repo)
        outbox.relay(lambda payload: outbox.consume(payload) or True)
        self.assertEqual([r[0] for r in table("SELECT target FROM archive ORDER BY ts")], ["r1", "r2", "r3"])

    def test_random_failures_never_lose_an_event_and_never_store_one_twice(self):
        rng = random.Random(5)
        db = outbox.connect()
        db.execute("DELETE FROM repos")
        for n in range(40):
            db.execute("INSERT INTO repos VALUES (?)", ("repo%d" % n,))
        db.close()
        for n in range(40):
            outbox.delete_repo("acme", "alice", "repo%d" % n)

        def flaky(payload):
            roll = rng.random()
            if roll < 0.25:
                return False
            outbox.consume(payload)
            if rng.random() < 0.2:
                outbox.consume(payload) # the queue delivered it twice
            if roll > 0.9:
                raise RuntimeError("the relay died after the queue had it")
            return True

        for _ in range(200):
            try:
                outbox.relay(flaky)
            except RuntimeError:
                pass
            if not table("SELECT * FROM outbox WHERE sent = 0"):
                break
        targets = [row[0] for row in table("SELECT target FROM archive")]
        self.assertEqual(sorted(targets), sorted("repo%d" % n for n in range(40)))


class ChainTests(unittest.TestCase):
    def setUp(self):
        chain.chains.clear()
        for n in range(5):
            chain.append("acme", {"event_id": "e%d" % n, "actor": "alice", "action": "repo.delete", "target": "r%d" % n})

    def test_an_untouched_chain_verifies_and_so_does_an_empty_one(self):
        self.assertTrue(chain.verify("acme"))
        self.assertTrue(chain.verify("nobody"))

    def test_changing_any_event_is_detected(self):
        for position in range(5):
            with self.subTest(position=position):
                chain.chains.clear()
                self.setUp()
                chain.chains["acme"][position]["event"]["actor"] = "mallory"
                self.assertFalse(chain.verify("acme"))

    def test_removing_an_event_from_the_middle_is_detected(self):
        del chain.chains["acme"][2]
        self.assertFalse(chain.verify("acme"))

    def test_reordering_and_inserting_are_detected(self):
        chain.chains["acme"][1], chain.chains["acme"][2] = chain.chains["acme"][2], chain.chains["acme"][1]
        self.assertFalse(chain.verify("acme"))
        chain.chains.clear()
        self.setUp()
        chain.chains["acme"].insert(2, {"event": {"event_id": "fake"}, "hash": "0" * 64})
        self.assertFalse(chain.verify("acme"))

    def test_recomputing_the_hashes_without_the_key_does_not_help_an_attacker(self):
        import hashlib
        import json
        entries = chain.chains["acme"]
        entries[1]["event"]["actor"] = "mallory"
        previous = chain.ZERO
        for entry in entries:
            entry["hash"] = hashlib.sha256((previous + json.dumps(entry["event"], sort_keys=True)).encode()).hexdigest()
            previous = entry["hash"]
        self.assertFalse(chain.verify("acme"))

    def test_cutting_off_the_newest_events_is_only_caught_with_a_checkpoint(self):
        checkpoint = chain.make_checkpoint("acme")
        del chain.chains["acme"][-2:]
        self.assertTrue(chain.verify("acme"))
        self.assertFalse(chain.verify("acme", checkpoint))

    def test_an_honest_chain_matches_its_checkpoint(self):
        checkpoint = chain.make_checkpoint("acme")
        self.assertTrue(chain.verify("acme", checkpoint))
        chain.append("acme", {"event_id": "later"})
        self.assertFalse(chain.verify("acme", checkpoint)) # newer than the checkpoint: the length differs

    def test_orgs_have_separate_chains(self):
        chain.append("globex", {"event_id": "g1"})
        chain.chains["acme"][0]["event"]["actor"] = "mallory"
        self.assertTrue(chain.verify("globex"))
        self.assertFalse(chain.verify("acme"))


class QueryTests(unittest.TestCase):
    def setUp(self):
        outbox.DB_FILE = os.path.join(tempfile.mkdtemp(), "audit.db")
        outbox.create_tables()

    def add(self, org, ts, event_id, actor="alice"):
        event = {"event_id": event_id, "ts": ts, "org": org, "actor": actor, "action": "repo.delete", "target": "r"}
        outbox.consume(json.dumps(event))

    def read_all(self, org, start, end, limit):
        got, cursor, pages = [], None, 0
        while True:
            answer = querying.query(org, start, end, cursor, limit)
            got.extend(answer["events"])
            pages += 1
            self.assertLess(pages, 1000)
            cursor = answer["next_cursor"]
            if cursor is None:
                return got

    def test_newest_first_within_the_range_and_the_end_is_excluded(self):
        for ts in range(10):
            self.add("acme", ts, "e%d" % ts)
        got = self.read_all("acme", 3, 7, 100)
        self.assertEqual([row[0] for row in got], [6, 5, 4, 3])

    def test_orgs_never_see_each_others_events(self):
        self.add("acme", 1, "a1")
        self.add("globex", 2, "g1")
        self.assertEqual([row[1] for row in self.read_all("acme", 0, 10, 10)], ["a1"])

    def test_pages_join_with_no_gaps_and_no_repeats_even_among_equal_timestamps(self):
        for n in range(23):
            self.add("acme", 5, "e%02d" % n)
        got = self.read_all("acme", 0, 10, 4)
        self.assertEqual([row[1] for row in got], ["e%02d" % n for n in reversed(range(23))])

    def test_a_full_last_page_has_no_cursor(self):
        for n in range(8):
            self.add("acme", n, "e%d" % n)
        first = querying.query("acme", 0, 100, None, 4)
        second = querying.query("acme", 0, 100, first["next_cursor"], 4)
        self.assertEqual(len(second["events"]), 4)
        self.assertIsNone(second["next_cursor"])

    def test_random_queries_match_a_plain_filter(self):
        rng = random.Random(8)
        events = []
        for n in range(120):
            ts, org = rng.randint(0, 30), rng.choice(["a", "b"])
            event_id = "e%03d" % n
            events.append((org, ts, event_id))
            self.add(org, ts, event_id)
        for _ in range(60):
            org = rng.choice(["a", "b"])
            start = rng.randint(0, 30)
            end = rng.randint(start, 35)
            limit = rng.randint(1, 9)
            expected = sorted([(ts, eid) for o, ts, eid in events if o == org and start <= ts < end], reverse=True)
            got = [(row[0], row[1]) for row in self.read_all(org, start, end, limit)]
            self.assertEqual(got, expected)


if __name__ == "__main__":
    unittest.main()
