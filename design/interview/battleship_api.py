import secrets
import threading
from flask import Flask, request
from battleship import new_game, place, fire, view, BadInput, NotAllowed

app = Flask(__name__)

games = {} # game id -> {"game": ..., "tokens": {"A": ..., "B": ...}, "lock": ...}


class ApiError(Exception):
    def __init__(self, status, message):
        self.status  = status
        self.message = message


@app.errorhandler(ApiError)
def api_error(e):
    return {"error": e.message}, e.status


@app.errorhandler(BadInput)
def bad_input(e):
    return {"error": str(e)}, 400


@app.errorhandler(NotAllowed)
def not_allowed(e):
    return {"error": str(e)}, 409


@app.post("/games")
def create_game():
    game_id = secrets.token_hex(4)
    tokens  = {"A": secrets.token_hex(8), "B": secrets.token_hex(8)}
    games[game_id] = {"game": new_game(), "tokens": tokens, "lock": threading.Lock()}

    return {"id": game_id, "tokens": tokens}, 201


@app.post("/games/<game_id>/ships")
def place_ship(game_id):
    entry, player = find(game_id)
    body = request.get_json(silent=True) or {}

    with entry["lock"]:
        place(entry["game"], player, body.get("ship"), body.get("row"),
              body.get("col"), body.get("orientation"))
        return view(entry["game"], player), 201


@app.post("/games/<game_id>/fire")
def fire_shot(game_id):
    entry, player = find(game_id)
    body = request.get_json(silent=True) or {}

    with entry["lock"]:
        return fire(entry["game"], player, body.get("row"), body.get("col"))


@app.get("/games/<game_id>")
def get_game(game_id):
    entry, player = find(game_id)

    with entry["lock"]:
        return view(entry["game"], player)


def find(game_id):
    entry = games.get(game_id)
    if entry is None:
        raise ApiError(404, "no such game")

    token = request.headers.get("X-Player-Token", "")
    for player, secret in entry["tokens"].items():
        if secrets.compare_digest(secret.encode(), token.encode()):
            return entry, player

    raise ApiError(401, "missing or wrong X-Player-Token")
