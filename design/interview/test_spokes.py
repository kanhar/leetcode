"""Tests for the Spokes teaching model: spokes_one, spokes_vote, spokes_read and spokes_place. Run: python -m unittest"""
import random
import sys
import threading
import time
import unittest

import spokes_one as one
import spokes_place as placing
import spokes_read as reading
import spokes_vote as vote


def reset_vote():
    for copy in vote.copies:
        copy.clear()
    for repo_set in vote.stale:
        repo_set.clear()
    vote.down.clear()
    vote.locks.clear()


class OneServerTests(unittest.TestCase):
    def setUp(self):
        one.heads.clear()

    def test_create_then_move_the_head(self):
        self.assertTrue(one.write("r", None, "c1"))
        self.assertTrue(one.write("r", "c1", "c2"))
        self.assertEqual(one.read("r"), "c2")

    def test_a_write_from_an_out_of_date_view_is_refused(self):
        one.write("r", None, "c1")
        one.write("r", "c1", "c2")
        self.assertFalse(one.write("r", "c1", "c3"))
        self.assertEqual(one.read("r"), "c2")

    def test_creating_a_repo_that_exists_is_refused(self):
        one.write("r", None, "c1")
        self.assertFalse(one.write("r", None, "other"))

    def test_an_unknown_repo_reads_as_none(self):
        self.assertIsNone(one.read("nope"))


class VoteTests(unittest.TestCase):
    def setUp(self):
        reset_vote()

    def test_a_write_lands_on_all_three_copies(self):
        self.assertTrue(vote.write("r", None, "c1"))
        self.assertEqual([c.get("r") for c in vote.copies], ["c1", "c1", "c1"])

    def test_with_one_replica_down_the_write_works_and_that_replica_goes_stale(self):
        vote.write("r", None, "c1")
        vote.down.add(2)
        self.assertTrue(vote.write("r", "c1", "c2"))
        self.assertEqual([c.get("r") for c in vote.copies], ["c2", "c2", "c1"])
        self.assertEqual(vote.stale[2], {"r"})
        self.assertEqual(vote.stale[0], set())

    def test_with_two_replicas_down_the_write_is_refused_and_changes_nothing(self):
        vote.write("r", None, "c1")
        vote.down.update({1, 2})
        self.assertFalse(vote.write("r", "c1", "c2"))
        self.assertEqual([c.get("r") for c in vote.copies], ["c1", "c1", "c1"])
        self.assertEqual([len(s) for s in vote.stale], [0, 0, 0])

    def test_a_write_from_an_out_of_date_view_is_refused_everywhere(self):
        vote.write("r", None, "c1")
        vote.write("r", "c1", "c2")
        self.assertFalse(vote.write("r", "c1", "c3"))
        self.assertEqual([c.get("r") for c in vote.copies], ["c2", "c2", "c2"])

    def test_a_write_that_only_one_replica_accepts_is_undone(self):
        vote.copies[0]["r"] = "x"
        vote.copies[1]["r"] = "y"
        vote.copies[2]["r"] = "y"
        self.assertFalse(vote.write("r", "x", "z"))
        self.assertEqual([c.get("r") for c in vote.copies], ["x", "y", "y"])

    def test_a_stale_replica_cannot_vote(self):
        vote.write("r", None, "c1")
        vote.down.add(2)
        vote.write("r", "c1", "c2")
        vote.down.clear()
        vote.down.add(1)
        # replica 2 is back but stale, replica 1 is down: only one voter is left
        self.assertFalse(vote.write("r", "c2", "c3"))

    def test_repos_are_independent(self):
        vote.write("a", None, "a1")
        vote.down.add(2)
        vote.write("b", None, "b1")
        self.assertEqual(vote.stale[2], {"b"})

    def test_twenty_writers_with_the_same_old_value_produce_exactly_one_winner(self):
        vote.write("r", None, "c0")
        before = sys.getswitchinterval()
        sys.setswitchinterval(1e-6)
        try:
            for round_number in range(30):
                reset_vote()
                vote.write("r", None, "c0")
                results = []
                lock = threading.Lock()

                def attempt(n):
                    won = vote.write("r", "c0", "w%d" % n)
                    with lock:
                        results.append((n, won))

                threads = [threading.Thread(target=attempt, args=(n,)) for n in range(20)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                winners = [n for n, won in results if won]
                self.assertEqual(len(winners), 1, results)
                self.assertEqual([c.get("r") for c in vote.copies], ["w%d" % winners[0]] * 3)
        finally:
            sys.setswitchinterval(before)


class SlowDict(dict):
    """A replica that takes a moment to read and write, so that two writers really do overlap."""

    def get(self, key, default=None):
        time.sleep(0.001)
        return super().get(key, default)

    def __setitem__(self, key, value):
        time.sleep(0.001)
        super().__setitem__(key, value)


class OverlappingWritersTests(unittest.TestCase):
    def setUp(self):
        reset_vote()
        for i in range(3):
            vote.copies[i] = SlowDict()

    def tearDown(self):
        for i in range(3):
            vote.copies[i] = {}
        reset_vote()

    def test_writers_that_overlap_still_produce_one_winner_and_no_stale_surprises(self):
        for round_number in range(15):
            reset_vote()
            vote.write("r", None, "c0")
            results = []
            lock = threading.Lock()

            def attempt(n):
                won = vote.write("r", "c0", "w%d" % n)
                with lock:
                    results.append((n, won))

            threads = [threading.Thread(target=attempt, args=(n,)) for n in range(6)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            winners = [n for n, won in results if won]
            self.assertEqual(len(winners), 1, results)
            for i in range(3):
                if "r" not in vote.stale[i]:
                    self.assertEqual(vote.copies[i].get("r"), "w%d" % winners[0], (round_number, i))
            self.assertEqual(reading.read("r"), "w%d" % winners[0])


class ReadAndRepairTests(unittest.TestCase):
    def setUp(self):
        reset_vote()

    def test_a_read_returns_the_latest_value(self):
        vote.write("r", None, "c1")
        vote.write("r", "c1", "c2")
        self.assertEqual(reading.read("r"), "c2")

    def test_a_stale_replica_never_serves_a_read(self):
        vote.write("r", None, "c1")
        vote.down.add(0)
        vote.write("r", "c1", "c2")
        vote.down.clear()
        for _ in range(5):
            self.assertEqual(reading.read("r"), "c2")

    def test_reads_survive_one_failure_and_even_two_if_one_good_replica_is_left(self):
        vote.write("r", None, "c1")
        vote.down.update({0, 1})
        self.assertEqual(reading.read("r"), "c1")

    def test_reads_work_when_writes_are_refused(self):
        vote.write("r", None, "c1")
        vote.down.update({0, 1})
        self.assertFalse(vote.write("r", "c1", "c2"))
        self.assertEqual(reading.read("r"), "c1")

    def test_with_only_a_stale_replica_reachable_the_read_is_refused_not_old(self):
        vote.write("r", None, "c1")
        vote.down.add(2)
        vote.write("r", "c1", "c2")
        vote.down.clear()
        vote.down.update({0, 1})
        with self.assertRaises(reading.Unavailable):
            reading.read("r")

    def test_repair_copies_from_a_good_replica_and_the_replica_votes_again(self):
        vote.write("r", None, "c1")
        vote.down.add(2)
        vote.write("r", "c1", "c2")
        vote.down.clear()
        self.assertTrue(reading.repair("r"))
        self.assertEqual([c.get("r") for c in vote.copies], ["c2", "c2", "c2"])
        self.assertEqual(vote.stale[2], set())
        vote.down.add(0)
        self.assertTrue(vote.write("r", "c2", "c3"))

    def test_repair_skips_a_replica_that_is_still_down(self):
        vote.write("r", None, "c1")
        vote.down.add(2)
        vote.write("r", "c1", "c2")
        self.assertTrue(reading.repair("r"))
        self.assertEqual(vote.copies[2].get("r"), "c1")
        self.assertEqual(vote.stale[2], {"r"})

    def test_repair_with_no_good_replica_does_nothing(self):
        vote.write("r", None, "c1")
        vote.down.add(2)
        vote.write("r", "c1", "c2")
        vote.down.clear()
        vote.down.update({0, 1})
        self.assertFalse(reading.repair("r"))

    def test_random_failures_never_break_the_promise(self):
        rng = random.Random(11)
        for trial in range(300):
            reset_vote()
            truth = {}
            for step in range(rng.randint(5, 40)):
                action = rng.choice(["write", "write", "write", "down", "up", "repair", "read"])
                repo = rng.choice(["a", "b"])
                if action == "write":
                    old = truth.get(repo) if rng.random() < 0.8 else "wrong"
                    new = "v%d" % step
                    voters = [i for i in range(3) if i not in vote.down and repo not in vote.stale[i]]
                    expect = len(voters) >= 2 and old == truth.get(repo)
                    got = vote.write(repo, old, new)
                    self.assertEqual(got, expect, (trial, step))
                    if got:
                        truth[repo] = new
                elif action == "down":
                    vote.down.add(rng.randrange(3))
                elif action == "up":
                    vote.down.discard(rng.randrange(3))
                elif action == "repair":
                    reading.repair(repo)
                else:
                    good = [i for i in range(3) if i not in vote.down and repo not in vote.stale[i]]
                    if good:
                        self.assertEqual(reading.read(repo), truth.get(repo), (trial, step))
                    else:
                        with self.assertRaises(reading.Unavailable):
                            reading.read(repo)
                # every replica that is not stale holds the latest acknowledged value
                for i in range(3):
                    for r in ("a", "b"):
                        if r not in vote.stale[i]:
                            self.assertEqual(vote.copies[i].get(r), truth.get(r), (trial, step, i, r))


class PlaceTests(unittest.TestCase):
    def servers(self):
        return [
            {"name": "s1", "rack": "r1", "load": 5, "down": False},
            {"name": "s2", "rack": "r1", "load": 1, "down": False},
            {"name": "s3", "rack": "r2", "load": 2, "down": False},
            {"name": "s4", "rack": "r3", "load": 9, "down": False},
            {"name": "s5", "rack": "r4", "load": 4, "down": False},
        ]

    def test_three_copies_on_three_different_racks_preferring_the_least_loaded(self):
        self.assertEqual(placing.place(self.servers()), ["s2", "s3", "s5"])

    def test_dead_servers_are_skipped(self):
        servers = self.servers()
        servers[1]["down"] = True
        self.assertEqual(placing.place(servers), ["s3", "s5", "s1"])

    def test_not_enough_racks_means_no_placement(self):
        servers = [s for s in self.servers() if s["rack"] in ("r1", "r2")]
        self.assertIsNone(placing.place(servers))

    def test_the_racks_are_always_distinct(self):
        rng = random.Random(3)
        for _ in range(200):
            servers = [{"name": "s%d" % i, "rack": "r%d" % rng.randint(0, 5), "load": rng.randint(0, 9), "down": rng.random() < 0.2} for i in range(rng.randint(0, 12))]
            chosen = placing.place(servers)
            if chosen is not None:
                racks = [s["rack"] for s in servers if s["name"] in chosen]
                self.assertEqual(len(chosen), 3)
                self.assertEqual(len(set(racks)), 3)
                self.assertFalse(any(s["down"] for s in servers if s["name"] in chosen))


if __name__ == "__main__":
    unittest.main()
