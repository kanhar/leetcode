"""Tests for the scan API files: scan_simple, scan_auth, scan_throttle, scan_validate and scan_lock. Run: python -m unittest"""
import hashlib
import importlib.util
import os
import threading
import time
import unittest
import uuid

import scan_simple
import scan_auth        # these four imports each plug one more check into the same app
import scan_throttle
import scan_validate
import scan_lock

HERE = os.path.dirname(os.path.abspath(__file__))


def wait_until(condition, seconds=5.0):
    end = time.time() + seconds
    while time.time() < end:
        if condition():
            return True
        time.sleep(0.01)
    return False


def guid():
    return str(uuid.uuid4())


def sha(token):
    return hashlib.sha256(token.encode()).hexdigest()


def load_alone():
    """A separate copy of the simplest version, with none of the extra checks plugged in."""
    spec = importlib.util.spec_from_file_location("scan_simple_alone_%s" % uuid.uuid4().hex, os.path.join(HERE, "scan_simple.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def let_scans_finish():
    wait_until(lambda: threading.active_count() == 1, 5.0)


class SlowDict(dict):
    """A dictionary whose lookups take a moment, so that two requests really do overlap."""

    def __contains__(self, key):
        found = super().__contains__(key)
        time.sleep(0.01)
        return found


class FakeClock:
    def __init__(self):
        self.now = 100.0

    def __call__(self):
        return self.now


class SimpleAloneTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_alone()
        self.mod.SCAN_SECONDS = 0.05
        self.client = self.mod.app.test_client()

    def tearDown(self):
        let_scans_finish()

    def put(self, scan_id, body=None, tenant="acme"):
        return self.client.put("/v1/tenants/%s/scans/%s" % (tenant, scan_id), json=body or {"target": "example.com"})

    def get(self, scan_id, tenant="acme"):
        return self.client.get("/v1/tenants/%s/scans/%s" % (tenant, scan_id))

    def test_start_answers_202_queued_and_then_the_scan_runs_to_the_end(self):
        scan_id = guid()
        first = self.put(scan_id)
        self.assertEqual((first.status_code, first.json["status"]), (202, "queued"))
        self.assertTrue(wait_until(lambda: self.get(scan_id).json["status"] == "succeeded"))

    def test_a_repeat_returns_the_same_scan_and_starts_nothing_new(self):
        scan_id = guid()
        self.put(scan_id)
        again = self.put(scan_id)
        self.assertEqual(again.status_code, 200)
        self.assertEqual(again.json["id"], scan_id)
        self.assertEqual(len(self.mod.scans), 1)

    def test_the_same_id_can_exist_in_two_tenants(self):
        scan_id = guid()
        self.assertEqual(self.put(scan_id, tenant="a").status_code, 202)
        self.assertEqual(self.put(scan_id, tenant="b").status_code, 202)
        self.assertEqual(self.get(scan_id, tenant="c").status_code, 404)

    def test_an_unknown_scan_is_404_with_the_error_shape(self):
        answer = self.get(guid())
        self.assertEqual(answer.status_code, 404)
        self.assertEqual(set(answer.json["error"]), {"code", "message"})


class PluggedInTests(unittest.TestCase):
    """The whole app: simple version plus token, tenant, scope, throttling, input checks and the lock."""

    def tearDown(self):
        let_scans_finish()

    def setUp(self):
        let_scans_finish()
        scan_simple.scans.clear()
        scan_simple.SCAN_SECONDS = 0.05
        self.clock = FakeClock()
        scan_throttle.clock = self.clock
        scan_throttle.buckets.clear()
        scan_throttle.BURST = 50
        scan_throttle.PER_SECOND = 5.0
        scan_auth.tokens.clear()
        scan_auth.tokens[sha("acme-token")] = {"tenant": "acme", "scopes": ["scans:read", "scans:write"]}
        scan_auth.tokens[sha("acme-readonly")] = {"tenant": "acme", "scopes": ["scans:read"]}
        scan_auth.tokens[sha("globex-token")] = {"tenant": "globex", "scopes": ["scans:read", "scans:write"]}
        self.client = scan_simple.app.test_client()

    def put(self, scan_id, body=None, token="acme-token", tenant="acme"):
        return self.client.put("/v1/tenants/%s/scans/%s" % (tenant, scan_id), json=body if body is not None else {"target": "example.com"},
                               headers={"Authorization": "Bearer " + token})

    def get(self, scan_id, token="acme-token", tenant="acme"):
        return self.client.get("/v1/tenants/%s/scans/%s" % (tenant, scan_id), headers={"Authorization": "Bearer " + token})

    # --------------------------------------------------------------- who is calling

    def test_missing_or_wrong_tokens_are_401(self):
        scan_id = guid()
        for headers in ({}, {"Authorization": "Bearer nope"}, {"Authorization": "Basic abc"}, {"Authorization": "Bearer "}, {"Authorization": "bearer"},
                        {"Authorization": "Basic acme-token"}, {"Authorization": "acme-token"}):
            with self.subTest(headers=headers):
                answer = self.client.get("/v1/tenants/acme/scans/" + scan_id, headers=headers)
                self.assertEqual(answer.status_code, 401)
                self.assertEqual(answer.json["error"]["code"], "unauthenticated")

    def test_a_good_token_works_end_to_end(self):
        scan_id = guid()
        self.assertEqual(self.put(scan_id).status_code, 202)
        self.assertTrue(wait_until(lambda: self.get(scan_id).json["status"] == "succeeded"))

    def test_another_tenants_token_sees_nothing_and_changes_nothing(self):
        scan_id = guid()
        self.put(scan_id)
        self.assertEqual(self.get(scan_id, token="globex-token", tenant="acme").status_code, 404)
        self.assertEqual(self.put(guid(), token="globex-token", tenant="acme").status_code, 404)
        self.assertEqual(len(scan_simple.scans), 1)

    def test_a_read_only_token_can_read_but_not_start(self):
        scan_id = guid()
        self.put(scan_id)
        self.assertEqual(self.get(scan_id, token="acme-readonly").status_code, 200)
        before = len(scan_simple.scans)
        answer = self.put(guid(), token="acme-readonly")
        self.assertEqual((answer.status_code, answer.json["error"]["code"]), (403, "forbidden"))
        self.assertEqual(len(scan_simple.scans), before)

    def test_the_token_is_looked_up_by_its_hash(self):
        self.assertNotIn("acme-token", scan_auth.tokens)
        self.assertIn(sha("acme-token"), scan_auth.tokens)

    # ------------------------------------------------------------------ throttling

    def test_requests_beyond_the_burst_get_429_with_retry_after(self):
        scan_throttle.BURST = 3
        scan_throttle.buckets.clear()
        scan_id = guid()
        codes = [self.get(scan_id).status_code for _ in range(3)]
        self.assertEqual(codes, [404, 404, 404])
        blocked = self.get(scan_id)
        self.assertEqual(blocked.status_code, 429)
        self.assertEqual(blocked.headers["Retry-After"], "1")
        self.assertEqual(blocked.json["error"]["code"], "rate_limited")

    def test_the_allowance_refills_with_time(self):
        scan_throttle.BURST = 2
        scan_throttle.PER_SECOND = 1.0
        scan_throttle.buckets.clear()
        scan_id = guid()
        self.get(scan_id)
        self.get(scan_id)
        self.assertEqual(self.get(scan_id).status_code, 429)
        self.clock.now += 1.0
        self.assertEqual(self.get(scan_id).status_code, 404)
        self.assertEqual(self.get(scan_id).status_code, 429)

    def test_one_token_being_throttled_does_not_affect_another(self):
        scan_throttle.BURST = 1
        scan_throttle.PER_SECOND = 0.1
        scan_throttle.buckets.clear()
        scan_id = guid()
        self.get(scan_id)
        self.assertEqual(self.get(scan_id).status_code, 429)
        self.assertEqual(self.get(scan_id, token="globex-token", tenant="globex").status_code, 404)

    def test_throttled_requests_start_no_scans(self):
        scan_throttle.BURST = 1
        scan_throttle.buckets.clear()
        self.get(guid())
        self.assertEqual(self.put(guid()).status_code, 429)
        self.assertEqual(len(scan_simple.scans), 0)

    # -------------------------------------------------------------- input and errors

    def test_bad_input_is_400_and_starts_nothing(self):
        cases = [
            ("not-a-guid", {"target": "x"}),
            (guid().upper(), {"target": "x"}),
            (guid(), {}),
            (guid(), {"target": ""}),
            (guid(), {"target": "x" * 256}),
            (guid(), {"target": 5}),
            (guid(), {"target": "x", "profile": "deep"}),
            (guid(), {"target": "x", "colour": "red"}),
            (guid(), ["target"]),
        ]
        for scan_id, body in cases:
            with self.subTest(scan_id=scan_id, body=body):
                answer = self.put(scan_id, body)
                self.assertEqual(answer.status_code, 400)
                self.assertEqual(set(answer.json["error"]), {"code", "message"})
        self.assertEqual(len(scan_simple.scans), 0)

    def test_a_body_that_is_not_json_is_400(self):
        answer = self.client.put("/v1/tenants/acme/scans/" + guid(), data="target=x", headers={"Authorization": "Bearer acme-token"})
        self.assertEqual(answer.status_code, 400)

    def test_every_error_has_one_shape_and_every_response_has_a_request_id(self):
        responses = [
            self.client.get("/v1/tenants/acme/scans/" + guid()),
            self.get(guid()),
            self.put("nope"),
            self.client.get("/v1/elsewhere", headers={"Authorization": "Bearer acme-token"}),
            self.client.post("/v1/tenants/acme/scans/" + guid(), headers={"Authorization": "Bearer acme-token"}),
            self.put(guid()),
        ]
        for answer in responses:
            with self.subTest(status=answer.status_code):
                self.assertIn("X-Request-ID", answer.headers)
                if answer.status_code >= 400:
                    self.assertEqual(set(answer.json), {"error"})
                    self.assertEqual(set(answer.json["error"]), {"code", "message"})

    # ------------------------------------------------------- two retries at once

    def test_the_same_id_with_different_parameters_is_a_conflict(self):
        scan_id = guid()
        self.put(scan_id, {"target": "example.com"})
        answer = self.put(scan_id, {"target": "other.example.com"})
        self.assertEqual((answer.status_code, answer.json["error"]["code"]), (409, "id_in_use"))

    def test_the_same_request_twice_is_200_the_second_time(self):
        scan_id = guid()
        self.assertEqual(self.put(scan_id).status_code, 202)
        self.assertEqual(self.put(scan_id).status_code, 200)

    def test_twenty_simultaneous_identical_requests_start_exactly_one_scan(self):
        started = []
        real = scan_lock.run_scan
        scan_lock.run_scan = lambda key: started.append(key)
        scan_throttle.BURST = 100000
        scan_throttle.buckets.clear()
        try:
            for round_number in range(10):
                scan_simple.scans.clear()
                started.clear()
                scan_id = guid()
                codes = []
                lock = threading.Lock()

                def call():
                    code = self.put(scan_id).status_code
                    with lock:
                        codes.append(code)

                threads = [threading.Thread(target=call) for _ in range(20)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                self.assertEqual(codes.count(202), 1, codes)
                self.assertEqual(codes.count(200), 19, codes)
                self.assertEqual(len(started), 1)
        finally:
            scan_lock.run_scan = real

    def test_overlapping_identical_requests_still_start_exactly_one_scan_with_the_lock(self):
        original = scan_simple.scans
        slow = SlowDict()
        scan_simple.scans = slow
        scan_lock.scans = slow
        started = []
        real = scan_lock.run_scan
        scan_lock.run_scan = lambda key: started.append(key)
        scan_throttle.BURST = 100000
        scan_throttle.buckets.clear()
        try:
            for round_number in range(5):
                slow.clear()
                started.clear()
                scan_id = guid()
                codes = []
                lock = threading.Lock()

                def call():
                    code = self.put(scan_id).status_code
                    with lock:
                        codes.append(code)

                threads = [threading.Thread(target=call) for _ in range(6)]
                for thread in threads:
                    thread.start()
                for thread in threads:
                    thread.join()
                self.assertEqual(codes.count(202), 1, codes)
                self.assertEqual(len(started), 1)
        finally:
            scan_simple.scans = original
            scan_lock.scans = original
            scan_lock.run_scan = real

    def test_without_the_lock_two_requests_can_both_start_the_scan(self):
        """The version in scan_simple has the race that scan_lock fixes. A slow dictionary makes it easy to hit."""

        alone = load_alone()
        alone.SCAN_SECONDS = 0
        started = []
        alone.run_scan = lambda key: started.append(key)
        alone.scans = SlowDict()
        client = alone.app.test_client()
        codes = []
        lock = threading.Lock()

        def call():
            code = client.put("/v1/tenants/acme/scans/" + "11111111-1111-4111-8111-111111111111", json={"target": "x"}).status_code
            with lock:
                codes.append(code)

        threads = [threading.Thread(target=call) for _ in range(6)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertGreater(codes.count(202), 1, "the race did not show up, so this test proves nothing")
        self.assertGreater(len(started), 1)


if __name__ == "__main__":
    unittest.main()
