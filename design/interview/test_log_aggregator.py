"""Randomized checks of log_aggregator.py and log_aggregator_paged.py against a plain version. Run: python -m unittest"""
import random
import unittest

import log_aggregator as agg
import log_aggregator_paged as paged


class Reference:
    """The slow, simple way: keep everything, filter and sort on every query."""

    def __init__(self):
        self.lines = []

    def add(self, tenant, server, lines):
        for line in lines:
            self.lines.append((tenant, line["time"], server, line["seq"], line["level"], line["message"]))

    def query(self, tenant, start, end):
        found = [line for line in self.lines if line[0] == tenant and start <= line[1] < end]
        found.sort(key=lambda line: (line[1], line[2], line[3]))
        return [(line[1], line[2], line[4], line[5]) for line in found]


def reset():
    agg.logs.clear()
    agg.seen.clear()


def as_tuples(lines):
    return [(l["time"], l["server"], l["level"], l["message"]) for l in lines]


def read_every_page(tenant, start, end, limit):
    """Walk the pages with the cursor until it runs out."""
    collected = []
    cursor = None
    pages = 0
    while True:
        answer = paged.get_logs_page(tenant, start, end, limit, cursor)
        collected.extend(as_tuples(answer["lines"]))
        pages += 1
        assert pages < 10000, "the cursor never ends"
        cursor = answer["next_cursor"]
        if cursor is None:
            return collected


def one_line(time, seq, message="x", level="I"):
    return {"time": time, "seq": seq, "level": level, "message": message}


class LogAggregatorTests(unittest.TestCase):
    def setUp(self):
        reset()

    def test_lines_from_several_servers_come_back_in_time_order(self):
        agg.upload_batch("t", "web-1", "b1", [one_line(10, 0, "a"), one_line(30, 1, "c")])
        agg.upload_batch("t", "web-2", "b1", [one_line(20, 0, "b"), one_line(40, 1, "d")])
        self.assertEqual([l["message"] for l in agg.get_logs("t", 0, 100)], ["a", "b", "c", "d"])

    def test_every_line_says_which_server_it_came_from(self):
        agg.upload_batch("t", "web-1", "b1", [one_line(10, 0)])
        agg.upload_batch("t", "web-2", "b1", [one_line(20, 0)])
        self.assertEqual([l["server"] for l in agg.get_logs("t", 0, 100)], ["web-1", "web-2"])

    def test_the_end_time_is_exclusive_and_the_start_inclusive(self):
        agg.upload_batch("t", "s", "b", [one_line(i, i, str(i)) for i in range(10)])
        self.assertEqual([l["message"] for l in agg.get_logs("t", 3, 6)], ["3", "4", "5"])

    def test_a_retried_batch_is_stored_once(self):
        lines = [one_line(1, 0)]
        self.assertEqual(agg.upload_batch("t", "s", "b1", lines), 202)
        self.assertEqual(agg.upload_batch("t", "s", "b1", lines), 200)
        self.assertEqual(len(agg.get_logs("t", 0, 10)), 1)

    def test_late_lines_slot_into_the_right_place(self):
        agg.upload_batch("t", "s", "b1", [one_line(100, 5, "later")])
        agg.upload_batch("t", "s", "b2", [one_line(50, 2, "earlier")])
        self.assertEqual([l["message"] for l in agg.get_logs("t", 0, 200)], ["earlier", "later"])

    def test_equal_timestamps_keep_each_servers_own_order(self):
        agg.upload_batch("t", "s", "b", [one_line(5, i, str(i)) for i in (3, 1, 2, 0)])
        self.assertEqual([l["message"] for l in agg.get_logs("t", 0, 10)], ["0", "1", "2", "3"])

    def test_tenants_never_see_each_others_logs(self):
        agg.upload_batch("a", "s", "b", [one_line(1, 0, "secret")])
        self.assertEqual(agg.get_logs("b", 0, 10), [])
        self.assertEqual(paged.get_logs_page("b", 0, 10)["lines"], [])

    # ------------------------------------------------------- the paged version

    def test_pages_join_up_with_no_gaps_and_no_repeats(self):
        agg.upload_batch("t", "s", "b", [one_line(i, i, str(i)) for i in range(25)])
        pages = []
        cursor = None
        while True:
            answer = paged.get_logs_page("t", 0, 100, limit=10, cursor=cursor)
            pages.append([l["message"] for l in answer["lines"]])
            cursor = answer["next_cursor"]
            if cursor is None:
                break
        self.assertEqual([len(p) for p in pages], [10, 10, 5])
        self.assertEqual([m for p in pages for m in p], [str(i) for i in range(25)])

    def test_an_exactly_full_last_page_has_no_cursor(self):
        agg.upload_batch("t", "s", "b", [one_line(i, i) for i in range(20)])
        first = paged.get_logs_page("t", 0, 100, limit=10)
        second = paged.get_logs_page("t", 0, 100, limit=10, cursor=first["next_cursor"])
        self.assertEqual(len(second["lines"]), 10)
        self.assertIsNone(second["next_cursor"])

    def test_a_page_that_ends_among_equal_timestamps_neither_skips_nor_repeats(self):
        agg.upload_batch("t", "a", "b1", [one_line(5, i, "a%d" % i) for i in range(4)])
        agg.upload_batch("t", "b", "b1", [one_line(5, i, "b%d" % i) for i in range(4)])
        first_page = paged.get_logs_page("t", 0, 10, limit=3)["lines"]
        self.assertEqual(len(first_page), 3)
        everything = read_every_page("t", 0, 10, 3)
        self.assertEqual([m for _, _, _, m in everything], ["a0", "a1", "a2", "a3", "b0", "b1", "b2", "b3"])

    # ------------------------------------------------------------- randomized

    def build_random(self, rng):
        reset()
        ref = Reference()
        servers = ["web-%d" % i for i in range(rng.randint(1, 5))]
        seqs = {s: 0 for s in servers}
        batch_no = 0
        for _ in range(rng.randint(0, 12)):
            server = rng.choice(servers)
            lines = []
            for _ in range(rng.randint(1, 8)):
                # times repeat on purpose, so ties are common
                lines.append(one_line(rng.randint(0, 30), seqs[server], "m%d" % rng.randint(0, 99), rng.choice("IWE")))
                seqs[server] += 1
            batch_no += 1
            tenant = rng.choice(["a", "b"])
            batch_id = "b%d" % batch_no
            self.assertEqual(agg.upload_batch(tenant, server, batch_id, lines), 202)
            ref.add(tenant, server, lines)
            if rng.random() < 0.3:
                self.assertEqual(agg.upload_batch(tenant, server, batch_id, lines), 200)
        return ref

    def test_random_uploads_and_queries_match_the_reference(self):
        rng = random.Random(2024)
        for trial in range(300):
            ref = self.build_random(rng)
            for _ in range(10):
                tenant = rng.choice(["a", "b"])
                start = rng.randint(0, 30)
                end = rng.randint(start, 35)
                self.assertEqual(as_tuples(agg.get_logs(tenant, start, end)), ref.query(tenant, start, end), (trial, tenant, start, end))

    def test_random_paging_matches_the_reference(self):
        rng = random.Random(7)
        for trial in range(300):
            ref = self.build_random(rng)
            for _ in range(10):
                tenant = rng.choice(["a", "b"])
                start = rng.randint(0, 30)
                end = rng.randint(start, 35)
                limit = rng.randint(1, 7)
                self.assertEqual(read_every_page(tenant, start, end, limit), ref.query(tenant, start, end), (trial, tenant, start, end, limit))


if __name__ == "__main__":
    unittest.main()
