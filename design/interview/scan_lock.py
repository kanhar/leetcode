import threading
from flask import request
from scan_simple import app, scans, run_scan, error

lock = threading.Lock()


def start_scan(tenant, scan_id):
    key    = (tenant, scan_id)
    params = request.get_json()

    with lock: # the check and the create are one step now
        if key in scans:
            if scans[key]["params"] != params:
                return error(409, "id_in_use", "that scan id was used with different parameters")

            return dict(scans[key]), 200 # a retry: here is the scan we already have

        scans[key] = {"id": scan_id, "status": "queued", "params": params}
        reply = dict(scans[key])

    threading.Thread(target=run_scan, args=(key,)).start()

    return reply, 202 # accepted, not finished yet


app.view_functions["start_scan"] = start_scan # replaces the version without the lock
