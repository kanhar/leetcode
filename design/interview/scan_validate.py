import uuid
from flask import request
from scan_simple import app, error

FIELDS   = ("target", "profile")
PROFILES = ("quick", "full")


@app.before_request
def check_input():
    if request.method != "PUT" or request.view_args is None:
        return

    scan_id = request.view_args["scan_id"]
    body    = request.get_json(silent=True)

    if not is_guid(scan_id):
        return error(400, "invalid_id", "the scan id must be a GUID, in lower case")

    if not isinstance(body, dict):
        return error(400, "invalid_request", "the body must be a JSON object")

    if any(name not in FIELDS for name in body):
        return error(400, "invalid_request", "unknown field")

    if not isinstance(body.get("target"), str) or not 0 < len(body["target"]) <= 255:
        return error(400, "invalid_request", "target must be text of 1 to 255 characters")

    if body.get("profile", "quick") not in PROFILES:
        return error(400, "invalid_request", "profile must be quick or full")


@app.after_request
def add_request_id(response):
    response.headers["X-Request-ID"] = str(uuid.uuid4()) # so a support ticket can be traced
    return response


@app.errorhandler(404)
def no_such_url(e):
    return error(404, "not_found", "no such resource")


@app.errorhandler(405)
def wrong_method(e):
    return error(405, "method_not_allowed", "that method is not supported here")


def is_guid(text):
    try:
        return str(uuid.UUID(text)) == text
    except ValueError:
        return False
