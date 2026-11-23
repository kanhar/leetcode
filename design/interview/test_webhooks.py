"""Tests for the webhook files: simple, retry, isolated, relay and breaker. Run: python -m unittest"""
import threading
import time
import unittest

import webhooks_breaker as breaker
import webhooks_isolated as iso
import webhooks_relay as relay
import webhooks_retry as retry
import webhooks_simple as simple


def wait_until(condition, seconds=3.0):
    end = time.time() + seconds
    while time.time() < end:
        if condition():
            return True
        time.sleep(0.005)
    return False


class SimpleTests(unittest.TestCase):
    def setUp(self):
        simple.subscribers.clear()
        self.calls = []
        simple.post = lambda url, event: self.calls.append((url, event)) or 200

    def test_every_subscriber_of_the_repo_is_called_once(self):
        simple.subscribers["r1"] = ["a", "b"]
        simple.subscribers["r2"] = ["c"]
        simple.on_push("r1", {"n": 1})
        self.assertEqual(self.calls, [("a", {"n": 1}), ("b", {"n": 1})])

    def test_a_repo_with_no_subscribers_calls_nobody(self):
        simple.on_push("nobody", {"n": 1})
        self.assertEqual(self.calls, [])

    def test_the_simple_version_does_not_retry(self):
        simple.post = lambda url, event: self.calls.append(url) or 503
        simple.subscribers["r"] = ["a"]
        simple.on_push("r", {})
        self.assertEqual(self.calls, ["a"])


class RetryTests(unittest.TestCase):
    def setUp(self):
        retry.dead_letters.clear()
        self.statuses = []
        self.calls = 0
        self.sleeps = []
        self.ceilings = []

        def post(url, event):
            self.calls += 1
            return self.statuses.pop(0)

        def jitter(low, high):
            self.ceilings.append(high)
            return high

        retry.post = post
        retry.sleep = self.sleeps.append
        retry.jitter = jitter

    def test_a_2xx_is_delivered_at_once(self):
        self.statuses = [(204, None)]
        self.assertTrue(retry.deliver("u", {"n": 1}))
        self.assertEqual((self.calls, self.sleeps, retry.dead_letters), (1, [], []))

    def test_failures_that_can_get_better_are_retried_until_they_work(self):
        self.statuses = [(503, None), (0, None), (500, None), (200, None)]
        self.assertTrue(retry.deliver("u", {}))
        self.assertEqual(self.calls, 4)
        self.assertEqual(len(self.sleeps), 3)

    def test_each_retryable_status_is_retried(self):
        for status in (0, 408, 429, 500, 502, 503, 504):
            with self.subTest(status=status):
                self.calls = 0
                self.statuses = [(status, None), (200, None)]
                self.assertTrue(retry.deliver("u", {}))
                self.assertEqual(self.calls, 2)

    def test_a_misconfigured_endpoint_is_not_retried_and_goes_to_the_dead_letters(self):
        for status in (301, 400, 401, 403, 404, 410, 422):
            with self.subTest(status=status):
                retry.dead_letters.clear()
                self.calls = 0
                self.statuses = [(status, None)]
                self.assertFalse(retry.deliver("u", {"n": status}))
                self.assertEqual(self.calls, 1)
                self.assertEqual(retry.dead_letters, [("u", {"n": status})])

    def test_it_gives_up_after_the_maximum_tries_and_does_not_wait_after_the_last(self):
        self.statuses = [(503, None)] * retry.MAX_TRIES
        self.assertFalse(retry.deliver("u", {}))
        self.assertEqual(self.calls, retry.MAX_TRIES)
        self.assertEqual(len(self.sleeps), retry.MAX_TRIES - 1)
        self.assertEqual(len(retry.dead_letters), 1)

    def test_the_wait_doubles_and_is_capped(self):
        self.statuses = [(503, None)] * retry.MAX_TRIES
        retry.deliver("u", {})
        expected = [min(retry.CAP, retry.BASE * 2 ** n) for n in range(retry.MAX_TRIES - 1)]
        self.assertEqual(self.ceilings, expected)
        self.assertEqual(retry.wait_time(50, None), retry.CAP)

    def test_the_wait_is_random_between_zero_and_the_ceiling(self):
        import random
        retry.jitter = random.uniform
        for attempt in range(10):
            for _ in range(50):
                self.assertTrue(0 <= retry.wait_time(attempt, None) <= min(retry.CAP, retry.BASE * 2 ** attempt))

    def test_retry_after_overrides_the_schedule(self):
        self.statuses = [(429, 17), (200, None)]
        retry.deliver("u", {})
        self.assertEqual(self.sleeps, [17])


class IsolatedTests(unittest.TestCase):
    def setUp(self):
        iso.queues.clear()
        retry.dead_letters.clear()
        iso.QUEUE_SIZE = 3
        self.delivered = []
        self.release = threading.Event()
        self.entered = threading.Event()
        retry.sleep = lambda seconds: None

        def post(url, event):
            if url == "stuck":
                self.entered.set()
                self.release.wait(5)
            self.delivered.append((url, event))
            return 200, None

        retry.post = post

    def tearDown(self):
        self.release.set()
        for events in list(iso.queues.values()):
            events.join() # let the old workers finish, so they cannot leak into the next test
        iso.QUEUE_SIZE = 100

    def test_a_stuck_endpoint_does_not_delay_a_healthy_one(self):
        for n in range(5):
            iso.try_submit("stuck", n)
        self.assertTrue(self.entered.wait(2))
        for n in range(10):
            iso.submit("healthy", n)
        self.assertTrue(wait_until(lambda: len([d for d in self.delivered if d[0] == "healthy"]) == 10))
        self.assertEqual([d for d in self.delivered if d[0] == "stuck"], [])

    def test_the_queue_is_bounded_and_try_submit_says_when_it_is_full(self):
        self.assertTrue(iso.try_submit("stuck", 0))
        self.assertTrue(self.entered.wait(2))
        answers = [iso.try_submit("stuck", n) for n in range(1, 8)]
        self.assertEqual(answers.count(True), iso.QUEUE_SIZE)
        self.assertEqual(answers[:3], [True, True, True])
        self.assertEqual(answers[3:], [False] * 4)
        self.assertEqual(iso.queues["stuck"].qsize(), iso.QUEUE_SIZE)

    def test_submit_waits_while_full_and_goes_through_once_there_is_room(self):
        iso.try_submit("stuck", 0)
        self.assertTrue(self.entered.wait(2))
        for n in range(1, 4):
            iso.try_submit("stuck", n)
        finished = threading.Event()

        def blocked_call():
            iso.submit("stuck", 99)
            finished.set()

        thread = threading.Thread(target=blocked_call, daemon=True)
        thread.start()
        self.assertFalse(finished.wait(0.3))
        self.release.set()
        self.assertTrue(finished.wait(3))
        self.assertTrue(wait_until(lambda: len(self.delivered) == 5))

    def test_one_endpoint_gets_its_events_in_order(self):
        for n in range(20):
            iso.submit("healthy", n)
        self.assertTrue(wait_until(lambda: len(self.delivered) == 20))
        self.assertEqual([e for _, e in self.delivered], list(range(20)))

    def test_a_failing_endpoint_does_not_stop_another_from_delivering(self):
        retry.post = lambda url, event: ((500, None) if url == "broken" else (200, None))
        self.delivered_ok = []
        original = retry.post

        def post(url, event):
            status = original(url, event)
            if status[0] == 200:
                self.delivered_ok.append((url, event))
            return status

        retry.post = post
        iso.submit("broken", "x")
        for n in range(5):
            iso.submit("fine", n)
        self.assertTrue(wait_until(lambda: len([d for d in self.delivered_ok if d[0] == "fine"]) == 5))


class RelayTests(unittest.TestCase):
    def setUp(self):
        iso.queues.clear()
        relay.outbox.clear()
        iso.QUEUE_SIZE = 3
        self.delivered = []
        self.release = threading.Event()
        self.entered = threading.Event()
        retry.sleep = lambda seconds: None

        def post(url, event):
            if url == "stuck":
                self.entered.set()
                self.release.wait(5)
            self.delivered.append((url, event))
            return 200, None

        retry.post = post

    def tearDown(self):
        self.release.set()
        for events in list(iso.queues.values()):
            events.join() # let the old workers finish, so they cannot leak into the next test
        iso.QUEUE_SIZE = 100

    def test_events_that_do_not_fit_stay_in_the_outbox_and_nothing_is_lost(self):
        relay.outbox.extend(("stuck", n) for n in range(10))
        relay.relay()
        self.assertTrue(self.entered.wait(2))
        still_waiting = len(relay.outbox)
        self.assertGreater(still_waiting, 0)
        self.release.set()
        for _ in range(200):
            relay.relay()
            if not relay.outbox and len(self.delivered) == 10:
                break
            time.sleep(0.01)
        self.assertEqual(relay.outbox, [])
        self.assertEqual(sorted(e for _, e in self.delivered), list(range(10)))

    def test_a_full_endpoint_does_not_hold_back_events_for_another(self):
        relay.outbox.extend(("stuck", n) for n in range(10))
        relay.outbox.extend(("healthy", n) for n in range(4))
        def pass_and_count():
            relay.relay() # a pass may leave a few behind while a queue is momentarily full
            return len([d for d in self.delivered if d[0] == "healthy"]) == 4

        self.assertTrue(wait_until(pass_and_count))
        self.assertTrue(any(url == "stuck" for url, _ in relay.outbox))


class BreakerTests(unittest.TestCase):
    def setUp(self):
        breaker.fails.clear()
        breaker.paused.clear()
        self.now = 1000.0
        breaker.clock = lambda: self.now
        self.calls = []
        self.answers = {}

        def real_post(url, event):
            self.calls.append(url)
            return self.answers.get(url, (200, None))

        breaker.real_post = real_post

    def test_after_enough_failures_the_endpoint_is_paused_and_not_called(self):
        self.answers["dead"] = (500, None)
        for _ in range(breaker.FAILS_TO_PAUSE):
            breaker.post("dead", {})
        before = len(self.calls)
        for _ in range(20):
            self.assertEqual(breaker.post("dead", {})[0], 503)
        self.assertEqual(len(self.calls), before)

    def test_it_is_tried_again_after_the_pause(self):
        self.answers["dead"] = (500, None)
        for _ in range(breaker.FAILS_TO_PAUSE):
            breaker.post("dead", {})
        self.now += breaker.PAUSE_SECONDS + 1
        self.answers["dead"] = (200, None)
        self.assertEqual(breaker.post("dead", {}), (200, None))

    def test_a_success_resets_the_count(self):
        for _ in range(breaker.FAILS_TO_PAUSE - 1):
            self.answers["x"] = (500, None)
            breaker.post("x", {})
        self.answers["x"] = (200, None)
        breaker.post("x", {})
        self.answers["x"] = (500, None)
        for _ in range(breaker.FAILS_TO_PAUSE - 1):
            breaker.post("x", {})
        self.assertNotIn("x", breaker.paused)

    def test_client_errors_do_not_count_as_failures(self):
        self.answers["x"] = (404, None)
        for _ in range(20):
            breaker.post("x", {})
        self.assertNotIn("x", breaker.paused)

    def test_one_dead_endpoint_does_not_pause_another(self):
        self.answers["dead"] = (500, None)
        for _ in range(breaker.FAILS_TO_PAUSE):
            breaker.post("dead", {})
        self.assertEqual(breaker.post("fine", {}), (200, None))

    def test_a_paused_endpoint_makes_the_retry_loop_wait_and_not_hammer(self):
        self.answers["dead"] = (500, None)
        retry.post = breaker.post
        retry.sleep = lambda seconds: None
        retry.jitter = lambda low, high: 0
        retry.dead_letters.clear()
        retry.deliver("dead", {})
        self.assertEqual(self.calls.count("dead"), breaker.FAILS_TO_PAUSE)
        self.assertEqual(len(retry.dead_letters), 1)


if __name__ == "__main__":
    unittest.main()
