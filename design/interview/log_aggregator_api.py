from flask import Flask, request
from log_aggregator import upload_batch, get_logs

app = Flask(__name__)

FIELDS = {"time", "seq", "level", "message"}


@app.put("/v1/tenants/<tenant>/servers/<server_id>/batches/<batch_id>")
def put_batch(tenant, server_id, batch_id):
    body = request.get_json(silent=True)

    if not body or not body.get("lines"):
        return {"error": "send JSON with a lines list"}, 400

    if len(body["lines"]) > 5000:
        return {"error": "at most 5000 lines per batch"}, 413

    if not all(is_good(line) for line in body["lines"]):
        return {"error": "each line needs time, seq, level, message"}, 400

    status = upload_batch(tenant, server_id, batch_id, body["lines"])
    return {"batch_id": batch_id}, status


@app.get("/v1/tenants/<tenant>/logs")
def read_logs(tenant):
    start = request.args.get("from", type=int)
    end   = request.args.get("to",   type=int)

    if start is None or end is None:
        return {"error": "from and to are required whole numbers"}, 400

    return {"lines": get_logs(tenant, start, end)}


def is_good(line):
    return (isinstance(line, dict)
            and FIELDS <= line.keys()
            and isinstance(line["time"], int)
            and isinstance(line["seq"], int))
