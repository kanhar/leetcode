"""Tests for log_aggregator_api.py, using Flask's test client. Run: python -m unittest"""
import unittest

import log_aggregator as agg
import log_aggregator_api as api


def line(time, seq, message="x", level="INFO"):
    return {"time": time, "seq": seq, "level": level, "message": message}


class ApiTests(unittest.TestCase):
    def setUp(self):
        agg.logs.clear()
        agg.seen.clear()
        self.client = api.app.test_client()

    def put(self, server, batch, lines, tenant="acme"):
        url = "/v1/tenants/%s/servers/%s/batches/%s" % (tenant, server, batch)
        return self.client.put(url, json={"lines": lines})

    def get(self, query, tenant="acme"):
        return self.client.get("/v1/tenants/%s/logs?%s" % (tenant, query))

    def test_upload_then_read_back_in_time_order(self):
        self.assertEqual(self.put("web-1", "b1", [line(10, 0, "a"), line(30, 1, "c")]).status_code, 202)
        self.assertEqual(self.put("web-2", "b1", [line(20, 0, "b")]).status_code, 202)
        answer = self.get("from=0&to=100")
        self.assertEqual(answer.status_code, 200)
        self.assertEqual([l["message"] for l in answer.json["lines"]], ["a", "b", "c"])
        self.assertEqual(answer.json["lines"][1], {"time": 20, "server": "web-2", "level": "INFO", "message": "b"})

    def test_a_repeated_batch_answers_200_and_is_stored_once(self):
        self.put("web-1", "b1", [line(10, 0)])
        again = self.put("web-1", "b1", [line(10, 0)])
        self.assertEqual(again.status_code, 200)
        self.assertEqual(len(self.get("from=0&to=100").json["lines"]), 1)

    def test_the_range_includes_from_and_excludes_to(self):
        self.put("s", "b", [line(i, i, str(i)) for i in range(10)])
        self.assertEqual([l["message"] for l in self.get("from=3&to=6").json["lines"]], ["3", "4", "5"])

    def test_tenants_are_separate(self):
        self.put("s", "b", [line(1, 0, "secret")], tenant="acme")
        self.assertEqual(self.get("from=0&to=10", tenant="globex").json["lines"], [])

    def test_bad_uploads_are_400_and_store_nothing(self):
        url = "/v1/tenants/acme/servers/s/batches/b"
        bad = [
            self.client.put(url, data="not json", content_type="application/json"),
            self.client.put(url, json={}),
            self.client.put(url, json={"lines": []}),
            self.client.put(url, json={"lines": "nope"}),
            self.client.put(url, json={"lines": [{"time": 1}]}),
            self.client.put(url, json={"lines": [line(1, 0), {"time": "late", "seq": 1, "level": "I", "message": "x"}]}),
            self.client.put(url, json={"lines": [5]}),
        ]
        for response in bad:
            self.assertEqual(response.status_code, 400, response.get_data(as_text=True))
            self.assertIn("error", response.json)
        self.assertEqual(self.get("from=0&to=100").json["lines"], [])

    def test_a_bad_batch_can_be_sent_again_once_fixed(self):
        url = "/v1/tenants/acme/servers/s/batches/b"
        self.assertEqual(self.client.put(url, json={"lines": [{"time": 1}]}).status_code, 400)
        self.assertEqual(self.put("s", "b", [line(1, 0)]).status_code, 202)

    def test_too_many_lines_is_413(self):
        too_many = [line(i, i) for i in range(5001)]
        self.assertEqual(self.put("s", "b", too_many).status_code, 413)
        self.assertEqual(self.get("from=0&to=100000").json["lines"], [])

    def test_missing_or_bad_range_is_400(self):
        for query in ("", "from=1", "to=5", "from=a&to=5", "from=1&to=2.5"):
            with self.subTest(query=query):
                answer = self.get(query)
                self.assertEqual(answer.status_code, 400)
                self.assertIn("error", answer.json)

    def test_an_empty_range_is_an_empty_list_not_an_error(self):
        self.put("s", "b", [line(10, 0)])
        self.assertEqual(self.get("from=50&to=60").json, {"lines": []})
        self.assertEqual(self.get("from=60&to=50").json, {"lines": []})

    def test_wrong_methods_and_unknown_urls_are_errors(self):
        self.assertEqual(self.client.post("/v1/tenants/acme/logs?from=0&to=1").status_code, 405)
        self.assertEqual(self.client.get("/v1/elsewhere").status_code, 404)


if __name__ == "__main__":
    unittest.main()
