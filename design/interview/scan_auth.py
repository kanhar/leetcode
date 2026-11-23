import hashlib
from flask import g, request
from scan_simple import app, error

tokens = {} # sha256 of a token -> {"tenant": "acme", "scopes": ["scans:read", "scans:write"]}
NEEDS  = {"GET": "scans:read", "HEAD": "scans:read", "PUT": "scans:write"}


@app.before_request
def check_token():
    kind, _, token = request.headers.get("Authorization", "").partition(" ")
    g.token = hashlib.sha256(token.strip().encode()).hexdigest()
    g.who   = tokens.get(g.token)

    if kind.lower() != "bearer" or g.who is None:
        return error(401, "unauthenticated", "send Authorization: Bearer <token>")


@app.before_request
def check_tenant_and_scope():
    if request.view_args is None:
        return # not one of our URLs

    if request.view_args["tenant"] != g.who["tenant"]:
        return error(404, "not_found", "no such resource") # not 403: do not reveal that it exists

    needs = NEEDS.get(request.method)
    if needs and needs not in g.who["scopes"]:
        return error(403, "forbidden", "this token lacks the scope " + needs)
