"""Tests for the push notification files: push_simple, push_recipients, push_fanout, push_lanes and push_delivery. Run: python -m unittest"""
import random
import unittest
from collections import deque

import push_delivery as delivery
import push_fanout as fanout
import push_lanes as lanes_module
import push_recipients as rec
import push_simple as simple


def event(**more):
    base = {"id": "evt1", "repo": "r", "thread": "t1", "kind": "comment", "actor": "alice"}
    base.update(more)
    return base


class SimpleTests(unittest.TestCase):
    def setUp(self):
        simple.watchers.clear()
        simple.devices.clear()
        simple.inbox.clear()
        self.sent = []
        simple.send = lambda device, note: self.sent.append((device, note["id"]))

    def test_every_watcher_gets_an_inbox_entry_and_a_push_per_device(self):
        simple.watchers["r"] = {"bob", "carol"}
        simple.devices["bob"] = ["bob-phone", "bob-laptop"]
        simple.devices["carol"] = ["carol-phone"]
        simple.on_event({"id": "e1", "repo": "r"})
        self.assertEqual(len(simple.inbox["bob"]), 1)
        self.assertEqual(sorted(self.sent), [("bob-laptop", "e1"), ("bob-phone", "e1"), ("carol-phone", "e1")])

    def test_a_repo_nobody_watches_notifies_nobody(self):
        simple.on_event({"id": "e1", "repo": "empty"})
        self.assertEqual(self.sent, [])


class RecipientsTests(unittest.TestCase):
    def setUp(self):
        rec.watchers.clear()
        rec.participants.clear()
        rec.prefs.clear()

    def test_watchers_participants_mentions_reviewers_and_admins_each_get_their_reason(self):
        rec.watchers["r"] = {"w1", "w2"}
        rec.participants["t1"] = {"p1"}
        got = rec.recipients(event(mentions=["m1"], reviewers=["r1"]))
        self.assertEqual(got, {"w1": "watching", "w2": "watching", "p1": "participating", "m1": "mention", "r1": "review_request"})
        got = rec.recipients(event(kind="security", admins=["a1", "a2"]))
        self.assertEqual(got["a1"], "security")

    def test_the_strongest_reason_wins(self):
        rec.watchers["r"] = {"bob", "carol", "dave"}
        rec.participants["t1"] = {"bob", "carol"}
        got = rec.recipients(event(mentions=["carol"], reviewers=["dave"]))
        self.assertEqual(got, {"bob": "participating", "carol": "mention", "dave": "review_request"})

    def test_a_security_reason_beats_everything(self):
        rec.watchers["r"] = {"bob"}
        got = rec.recipients(event(kind="security", admins=["bob"], mentions=["bob"]))
        self.assertEqual(got["bob"], "security")

    def test_nobody_is_told_about_their_own_action(self):
        rec.watchers["r"] = {"alice", "bob"}
        got = rec.recipients(event(mentions=["alice"]))
        self.assertEqual(list(got), ["bob"])

    def test_channels_the_inbox_always_and_push_outside_quiet_hours(self):
        self.assertEqual(rec.channels("u", "mention", "t1", 12), ["inbox", "push"])

    def test_quiet_hours_hold_back_the_push_but_not_the_inbox(self):
        for hour in (22, 23, 0, 3, 6):
            with self.subTest(hour=hour):
                self.assertEqual(rec.channels("u", "mention", "t1", hour), ["inbox"])
        for hour in (7, 12, 21):
            with self.subTest(hour=hour):
                self.assertIn("push", rec.channels("u", "mention", "t1", hour))

    def test_security_alerts_push_even_in_quiet_hours(self):
        self.assertEqual(rec.channels("u", "security", "t1", 3), ["inbox", "push"])

    def test_quiet_hours_that_do_not_cross_midnight(self):
        self.assertTrue(rec.in_quiet(10, 9, 17))
        self.assertFalse(rec.in_quiet(17, 9, 17))
        self.assertFalse(rec.in_quiet(8, 9, 17))

    def test_a_muted_thread_gets_nothing_except_security(self):
        rec.prefs["u"]["muted"].add("t1")
        self.assertEqual(rec.channels("u", "mention", "t1", 12), [])
        self.assertEqual(rec.channels("u", "security", "t1", 12), ["inbox", "push"])
        self.assertEqual(rec.channels("u", "mention", "t2", 12), ["inbox", "push"])

    def test_someone_who_stopped_watching_hears_nothing_from_watching(self):
        rec.prefs["u"]["watching"] = False
        self.assertEqual(rec.channels("u", "watching", "t1", 12), [])
        self.assertEqual(rec.channels("u", "mention", "t1", 12), ["inbox", "push"])


class FanOutTests(unittest.TestCase):
    def setUp(self):
        rec.watchers.clear()
        rec.participants.clear()
        rec.prefs.clear()
        fanout.cursors.clear()
        fanout.notes.clear()
        fanout.outgoing.clear()
        rec.watchers["r"] = {"u%04d" % n for n in range(2500)}
        self.tasks = []

    def users_in(self, tasks):
        return [u for task in tasks for u in task["reasons"]]

    def test_the_recipients_are_cut_into_chunks_of_a_thousand_covering_everyone_once(self):
        fanout.fan_out(event(), self.tasks.append)
        self.assertEqual([len(t["reasons"]) for t in self.tasks], [1000, 1000, 500])
        self.assertEqual(sorted(self.users_in(self.tasks)), sorted(rec.watchers["r"]))

    def test_a_chunk_makes_an_inbox_entry_and_a_push_for_each_user(self):
        fanout.fan_out(event(), self.tasks.append)
        fanout.notify_chunk(self.tasks[0], hour=12)
        self.assertEqual(len(fanout.notes), 2000)
        self.assertEqual(len(fanout.outgoing), 1000)

    def test_running_a_chunk_twice_does_nothing_the_second_time(self):
        fanout.fan_out(event(), self.tasks.append)
        fanout.notify_chunk(self.tasks[0], hour=12)
        fanout.notify_chunk(self.tasks[0], hour=12)
        self.assertEqual((len(fanout.notes), len(fanout.outgoing)), (2000, 1000))

    def test_quiet_hours_make_inbox_entries_but_no_pushes(self):
        fanout.fan_out(event(), self.tasks.append)
        fanout.notify_chunk(self.tasks[0], hour=3)
        self.assertEqual((len(fanout.notes), len(fanout.outgoing)), (1000, 0))

    def test_a_coordinator_that_crashes_resumes_where_it_stopped(self):
        calls = {"n": 0}

        def flaky(task):
            calls["n"] += 1
            if calls["n"] == 3:
                raise RuntimeError("crash")
            self.tasks.append(task)

        with self.assertRaises(RuntimeError):
            fanout.fan_out(event(), flaky)
        self.assertEqual(fanout.cursors["evt1"], 2000)
        fanout.fan_out(event(), self.tasks.append)
        self.assertEqual([len(t["reasons"]) for t in self.tasks], [1000, 1000, 500])

    def test_crashes_and_whole_reruns_send_nothing_twice_and_miss_no_one(self):
        rng = random.Random(3)
        for attempt in range(30):
            def flaky(task):
                if rng.random() < 0.3:
                    raise RuntimeError("crash before it was queued")
                self.tasks.append(task)
                if rng.random() < 0.3:
                    raise RuntimeError("crash after it was queued, before the cursor was saved")

            try:
                fanout.fan_out(event(), flaky)
            except RuntimeError:
                pass
            if fanout.cursors.get("evt1", 0) >= 2500:
                break
        for task in self.tasks + self.tasks[:2]:
            fanout.notify_chunk(task, hour=12)
        self.assertEqual(len(fanout.notes), 5000)
        self.assertEqual(len(fanout.outgoing), 2500)
        self.assertEqual(len(set(fanout.outgoing)), 2500)


class LanesTests(unittest.TestCase):
    def setUp(self):
        for lane in lanes_module.lanes.values():
            lane.clear()
        lanes_module.turn["i"] = 0

    def test_an_urgent_notification_gets_out_ahead_of_a_huge_broadcast(self):
        for n in range(100000):
            lanes_module.put("watching", ("broadcast", n))
        lanes_module.put("direct", ("mention", 0))
        takes = 0
        while True:
            takes += 1
            if lanes_module.take()[0] == "mention":
                break
        self.assertLessEqual(takes, 10)

        shared = deque(("broadcast", n) for n in range(100000))
        shared.append(("mention", 0))
        waited = 0
        while shared.popleft()[0] != "mention":
            waited += 1
        self.assertEqual(waited, 100000)

    def test_the_broadcast_still_moves_while_urgent_traffic_continues(self):
        for n in range(1000):
            lanes_module.put("security", ("security", n))
            lanes_module.put("watching", ("watching", n))
        first_hundred = [lanes_module.take()[0] for _ in range(100)]
        # the empty "direct" lane gives its turns away, so security and watching share them 6 to 1
        self.assertEqual(first_hundred.count("security"), 86)
        self.assertEqual(first_hundred.count("watching"), 14)

    def test_a_lane_keeps_its_own_order_and_an_empty_system_returns_none(self):
        self.assertIsNone(lanes_module.take())
        for n in range(5):
            lanes_module.put("direct", n)
        self.assertEqual([lanes_module.take() for _ in range(5)], [0, 1, 2, 3, 4])

    def test_random_traffic_is_all_delivered_exactly_once(self):
        rng = random.Random(1)
        put, got = [], []
        for n in range(3000):
            lane = rng.choice(["security", "direct", "watching"])
            lanes_module.put(lane, n)
            put.append(n)
            if rng.random() < 0.5:
                item = lanes_module.take()
                if item is not None:
                    got.append(item)
        while True:
            item = lanes_module.take()
            if item is None:
                break
            got.append(item)
        self.assertEqual(sorted(got), put)


class Crash(Exception):
    pass


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        delivery.sent.clear()
        self.out = []
        delivery.send = lambda note: self.out.append(note["id"])

    def test_a_notification_goes_out_once_and_a_repeat_is_ignored(self):
        delivery.deliver({"id": "n1"})
        delivery.deliver({"id": "n1"})
        self.assertEqual(self.out, ["n1"])

    def test_a_crash_before_sending_leaves_no_record_so_the_retry_sends(self):
        def broken(note):
            raise Crash()

        delivery.send = broken
        with self.assertRaises(Crash):
            delivery.deliver({"id": "n1"})
        self.assertEqual(delivery.sent, set())
        delivery.send = lambda note: self.out.append(note["id"])
        delivery.deliver({"id": "n1"})
        self.assertEqual(self.out, ["n1"])

    def test_a_crash_after_sending_means_a_repeat_not_a_loss(self):
        class Dies(set):
            def add(self, item):
                raise Crash()

        delivery.sent = Dies()
        with self.assertRaises(Crash):
            delivery.deliver({"id": "n1"})
        delivery.sent = set()
        delivery.deliver({"id": "n1"})
        self.assertEqual(self.out, ["n1", "n1"])

    def simulate(self, order, count, chance, seed):
        """Send `count` notifications through a worker that crashes with probability `chance` before each step,
        and whose message is redelivered after every crash. Returns (lost, sent twice)."""
        rng = random.Random(seed)
        times_sent = {}
        done = set()

        def send(note):
            if rng.random() < chance:
                raise Crash()
            times_sent[note["id"]] = times_sent.get(note["id"], 0) + 1

        class Memory(set):
            def add(self, item):
                if rng.random() < chance:
                    raise Crash()
                super().add(item)

        memory = Memory()

        def claim_then_send(note):
            if note["id"] in memory:
                return # a retry sees the claim and gives up
            memory.add(note["id"])
            send(note)

        def send_then_mark(note):
            if note["id"] in memory:
                return
            send(note)
            memory.add(note["id"])

        worker = claim_then_send if order == "claim first" else send_then_mark
        for n in range(count):
            note = {"id": "n%d" % n}
            for _ in range(1000):
                try:
                    worker(note)
                    break
                except Crash:
                    continue
        lost = sum(1 for n in range(count) if times_sent.get("n%d" % n, 0) == 0)
        twice = sum(1 for n in range(count) if times_sent.get("n%d" % n, 0) > 1)
        return lost, twice

    def test_claiming_first_loses_notifications_and_sending_first_repeats_them(self):
        claim_lost, claim_twice = self.simulate("claim first", 50000, 0.02, 1)
        send_lost, send_twice = self.simulate("send first", 50000, 0.02, 1)
        self.assertGreater(claim_lost, 500)
        self.assertEqual(claim_twice, 0)
        self.assertEqual(send_lost, 0)
        self.assertGreater(send_twice, 500)

    def test_the_real_deliver_function_behaves_like_the_send_first_simulation(self):
        rng = random.Random(2)
        times_sent = {}

        def send(note):
            if rng.random() < 0.05:
                raise Crash()
            times_sent[note["id"]] = times_sent.get(note["id"], 0) + 1

        class Memory(set):
            def add(self, item):
                if rng.random() < 0.05:
                    raise Crash()
                super().add(item)

        delivery.send = send
        delivery.sent = Memory()
        for n in range(5000):
            note = {"id": "n%d" % n}
            for _ in range(1000):
                try:
                    delivery.deliver(note)
                    break
                except Crash:
                    continue
        self.assertTrue(all(times_sent.get("n%d" % n, 0) >= 1 for n in range(5000)))
        self.assertTrue(any(times_sent["n%d" % n] > 1 for n in range(5000)))


if __name__ == "__main__":
    unittest.main()
