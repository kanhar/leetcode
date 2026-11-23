import threading
import time
from flask import Flask, request

app = Flask(__name__)

SCAN_SECONDS = 2

scans = {} # (tenant, scan id) -> the scan


@app.put("/v1/tenants/<tenant>/scans/<scan_id>")
def start_scan(tenant, scan_id):
    key = (tenant, scan_id)

    if key in scans:
        return scans[key], 200 # a retry: here is the scan we already have

    scans[key] = {"id": scan_id, "status": "queued", "params": request.get_json()}
    reply = dict(scans[key])

    threading.Thread(target=run_scan, args=(key,)).start()

    return reply, 202 # accepted, not finished yet


@app.get("/v1/tenants/<tenant>/scans/<scan_id>")
def get_scan(tenant, scan_id):
    scan = scans.get((tenant, scan_id))

    if scan is None:
        return error(404, "not_found", "no such scan")

    return scan


def run_scan(key):
    scans[key]["status"] = "running"
    time.sleep(SCAN_SECONDS)
    scans[key]["status"] = "succeeded"


def error(status, code, message):
    return {"error": {"code": code, "message": message}}, status
