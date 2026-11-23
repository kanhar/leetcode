"""Tests for the drone delivery files: simple, booking, orders and failure. Run: python -m unittest"""
import os
import sqlite3
import tempfile
import threading
import unittest

import drone_booking as booking
import drone_failure as failure
import drone_orders as orders
import drone_simple as simple


def make_db():
    """A fresh database file. Every thread opens its own connection to it, like separate servers would."""
    path = os.path.join(tempfile.mkdtemp(), "drones.db")
    db = connect(path)
    db.execute("CREATE TABLE booked (drone TEXT, slot INTEGER, order_id TEXT, PRIMARY KEY (drone, slot))")
    db.execute("CREATE TABLE orders (order_id TEXT PRIMARY KEY, state TEXT, drone TEXT, start INTEGER)")
    db.commit()
    return path, db


def connect(path):
    return sqlite3.connect(path, timeout=60)


def run_in_threads(count, work):
    results = [None] * count

    def one(i):
        db = None
        try:
            db = connect(PATH[0])
            results[i] = work(db, i)
        finally:
            if db:
                db.close()

    threads = [threading.Thread(target=one, args=(i,)) for i in range(count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results


PATH = [None]


class SimpleTests(unittest.TestCase):
    def setUp(self):
        simple.drones[:] = ["D1", "D2"]
        simple.busy.clear()

    def test_each_order_gets_a_free_drone_until_there_are_none(self):
        self.assertEqual(simple.place_order("o1"), "D1")
        self.assertEqual(simple.place_order("o2"), "D2")
        self.assertIsNone(simple.place_order("o3"))


class BookingTests(unittest.TestCase):
    def setUp(self):
        PATH[0], self.db = make_db()

    def test_slots_needed_counts_the_round_trip_handling_and_buffer(self):
        self.assertEqual(booking.slots_needed(4), 2) # 10 min flying + 20 = 30 min
        self.assertEqual(booking.slots_needed(0), 2) # even a trip next door costs the 20 minutes
        self.assertEqual(booking.slots_needed(10), 3) # 25 + 20 = 45 min

    def test_a_free_slot_range_is_booked_whole(self):
        self.assertTrue(booking.book(self.db, "D1", 0, 2, "o1"))
        slots = [row[0] for row in self.db.execute("SELECT slot FROM booked WHERE drone = 'D1' ORDER BY slot")]
        self.assertEqual(slots, [0, 1, 2])

    def test_an_overlapping_booking_is_refused_and_keeps_nothing(self):
        booking.book(self.db, "D1", 2, 3, "o1")
        self.assertFalse(booking.book(self.db, "D1", 0, 2, "o2")) # slot 2 is taken
        slots = [row[0] for row in self.db.execute("SELECT slot FROM booked WHERE order_id = 'o2'")]
        self.assertEqual(slots, []) # slots 0 and 1 were rolled back, not left half booked

    def test_the_same_slots_on_another_drone_are_free(self):
        booking.book(self.db, "D1", 0, 1, "o1")
        self.assertTrue(booking.book(self.db, "D2", 0, 1, "o2"))

    def test_the_first_free_drone_and_the_earliest_start_win(self):
        self.assertEqual(booking.place_order(self.db, ["D1", "D2"], "o1", 4, 0, 7), ("D1", 0))
        self.assertEqual(booking.place_order(self.db, ["D1", "D2"], "o2", 4, 0, 7), ("D2", 0))
        self.assertEqual(booking.place_order(self.db, ["D1", "D2"], "o3", 4, 0, 7), ("D1", 2))

    def test_an_order_that_cannot_finish_inside_its_window_is_refused_with_a_reason(self):
        self.assertEqual(booking.place_order(self.db, ["D1"], "o1", 4, 0, 0), (None, "NO_DRONE_AVAILABLE"))
        self.assertEqual(booking.place_order(self.db, ["D1"], "o2", 50, 0, 100), (None, "OUT_OF_RANGE"))

    def test_when_every_slot_is_taken_the_answer_is_no(self):
        for i in range(4):
            self.assertEqual(booking.place_order(self.db, ["D1"], "o%d" % i, 4, 0, 7)[0], "D1")
        self.assertEqual(booking.place_order(self.db, ["D1"], "late", 4, 0, 7), (None, "NO_DRONE_AVAILABLE"))

    def test_thirty_orders_at_once_never_share_a_drone_slot(self):
        drones = ["D1", "D2", "D3"] # 8 slots each and 2 slots per order: room for 4 each, 12 in all
        answers = run_in_threads(30, lambda db, i: booking.place_order(db, drones, "o%d" % i, 4, 0, 7))
        booked = [a for a in answers if a[0] is not None]
        self.assertEqual(len(booked), 12) # the drones are exactly full, nothing is lost and nothing doubled
        rows = self.db.execute("SELECT drone, slot, COUNT(*) FROM booked GROUP BY drone, slot").fetchall()
        self.assertTrue(all(count == 1 for drone, slot, count in rows))
        self.assertEqual(len(rows), 24)


class OrderTests(unittest.TestCase):
    def setUp(self):
        PATH[0], self.db = make_db()
        self.drones = ["D1", "D2"]

    def test_a_new_order_is_assigned(self):
        self.assertEqual(orders.place(self.db, self.drones, "o1", 4, 0, 7), ("ASSIGNED", "D1", 0))

    def test_a_retry_gets_the_same_answer_and_books_nothing_more(self):
        first = orders.place(self.db, self.drones, "o1", 4, 0, 7)
        again = orders.place(self.db, self.drones, "o1", 4, 0, 7)
        self.assertEqual(tuple(again), first)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM booked WHERE order_id = 'o1'").fetchone()[0], 2)

    def test_twenty_simultaneous_retries_make_one_order(self):
        answers = run_in_threads(20, lambda db, i: orders.place(db, self.drones, "same-order", 4, 0, 7))
        self.assertEqual({tuple(a) for a in answers}, {("ASSIGNED", "D1", 0)})
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM orders").fetchone()[0], 1)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM booked").fetchone()[0], 2)

    def test_a_refused_order_says_why(self):
        self.assertEqual(orders.place(self.db, self.drones, "far", 50, 0, 100), ("REJECTED", None, "OUT_OF_RANGE"))

    def test_a_state_can_only_be_left_once(self):
        orders.place(self.db, self.drones, "o1", 4, 0, 7)
        self.assertTrue(orders.move(self.db, "o1", "ASSIGNED", "PICKED_UP"))
        self.assertFalse(orders.move(self.db, "o1", "ASSIGNED", "PICKED_UP")) # already moved on
        self.assertFalse(orders.move(self.db, "o1", "ASSIGNED", "CANCELLED")) # too late to cancel from ASSIGNED

    def test_delivered_notifies_once_even_when_the_drone_reports_it_many_times(self):
        orders.place(self.db, self.drones, "o1", 4, 0, 7)
        orders.move(self.db, "o1", "ASSIGNED", "DELIVERING")
        sent = []
        lock = threading.Lock()

        def notify(order_id):
            with lock:
                sent.append(order_id)

        run_in_threads(20, lambda db, i: orders.delivered(db, "o1", "D1", notify))
        self.assertEqual(sent, ["o1"])

    def test_a_drone_that_no_longer_holds_the_order_cannot_finish_it(self):
        orders.place(self.db, self.drones, "o1", 4, 0, 7) # D1
        failure.reassign(self.db, self.drones, "o1", "D1", 4, 1, 7) # given up on, now D2 holds it
        orders.move(self.db, "o1", "ASSIGNED", "DELIVERING")
        sent = []
        orders.delivered(self.db, "o1", "D1", sent.append) # the old drone was still flying and reports in
        self.assertEqual(sent, [])
        orders.delivered(self.db, "o1", "D2", sent.append)
        self.assertEqual(sent, ["o1"])


class FailureTests(unittest.TestCase):
    def setUp(self):
        PATH[0], self.db = make_db()
        self.drones = ["D1", "D2"]

    def test_a_failed_drone_loses_the_order_to_another_drone_inside_the_window(self):
        orders.place(self.db, self.drones, "o1", 4, 0, 7) # D1, slots 0-1
        self.assertEqual(failure.reassign(self.db, self.drones, "o1", "D1", 4, 1, 7), ("D2", 1))
        rows = self.db.execute("SELECT drone, slot FROM booked WHERE order_id = 'o1' ORDER BY slot").fetchall()
        self.assertEqual(rows, [("D2", 1), ("D2", 2)]) # the old slots are free again, only one set is held
        self.assertEqual(orders.current(self.db, "o1"), ("ASSIGNED", "D2", 1))

    def test_the_slots_the_failed_drone_gave_back_can_be_used_by_the_next_order(self):
        orders.place(self.db, self.drones, "o1", 4, 0, 7)
        failure.reassign(self.db, self.drones, "o1", "D1", 4, 1, 7)
        self.assertEqual(orders.place(self.db, self.drones, "o2", 4, 0, 1), ("ASSIGNED", "D1", 0))

    def test_when_nobody_can_take_it_the_answer_is_no_and_nothing_is_held(self):
        orders.place(self.db, ["D1"], "o1", 4, 0, 1)
        self.assertEqual(failure.reassign(self.db, ["D1"], "o1", "D1", 4, 0, 1), (None, "NO_DRONE_AVAILABLE"))
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM booked").fetchone()[0], 0)


if __name__ == "__main__":
    unittest.main()
