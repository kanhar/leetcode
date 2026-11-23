{: .no_toc}
# Battleship Game API

A practical question: design and write a working game engine, or a REST API around one, for a simple turn-based game like Battleship or Tic-Tac-Toe. The skill being tested is how you structure the code, how you name the states, and how you handle illegal moves. Python, with Flask for the API.

<style>
/* Code on this page wraps instead of scrolling sideways, and the column is a little wider on desktop. */
pre, code { white-space: pre-wrap; overflow-wrap: anywhere; }
pre code { font-size: 12px; line-height: 1.45; }
@media (min-width: 961px) {
  .wrapper { width: 940px; }
  section { width: 640px; }
}
</style>

- TOC
{:toc}

### 1. What we are building

Two players each hide a fleet of ships on a 10 by 10 grid, and then take turns firing at cells of the other player's grid. A shot is a hit or a miss, a ship whose cells have all been hit is sunk, and the first player to sink the whole fleet wins.

Before writing anything, ask. Which game and which rules? Battleship, with five ships and the turn passing after every shot. Engine only, or an API too? Both: the engine first, then a thin API on top. How many games and players? Many games at once, two players each. Does the state need to survive a restart? Start in memory, and say how you would persist it. Can players cheat? Each player gets a secret token, and nobody ever sees the opponent's ships. Then say the sentence that sets the shape of the answer: "I'll keep the rules in an engine that knows nothing about HTTP, and put a thin API on top."

The order I would work in is the order of this page. Start with the smallest thing that plays a game. Then name the **states** the game goes through, and write down every **illegal action** before coding it. Raise a typed error for each kind. Let the API turn the error type into a status code, so there is no ladder of string checks anywhere.

### 2. The simplest version

Each player has a set of cells their ships cover, and a set of cells they have fired at. Firing is a lookup. The winner is whoever has hit every enemy cell.

<details><summary markdown="span">Execute! (the simplest version)</summary>

```python
ships = {"A": set(), "B": set()} # the cells each player's ships cover
shots = {"A": set(), "B": set()} # the cells each player has fired at


def place(player, cells):
    ships[player] = set(cells)


def fire(player, cell):
    enemy = "B" if player == "A" else "A"
    shots[player].add(cell)

    if cell in ships[enemy]:
        return "hit"

    return "miss"


def winner():
    for player, enemy in (("A", "B"), ("B", "A")):
        if ships[enemy] and ships[enemy] <= shots[player]:
            return player # every enemy cell has been hit
```

</details>
<BR>


That is a game. It is also missing nearly everything that makes it a game you could trust. Nothing stops a ship leaving the board or overlapping another. There is no setup phase, no turns, so one player can fire ten times in a row. A cell can be fired at twice. A hit does not say which ship was hit, and nothing is ever sunk. The next sections add these one at a time.

### 3. The rules: states, turns and illegal moves

A game is always in one of three **states**: `setup` while the players place their ships, `playing` while they take turns, and `finished` when somebody has won. Every action is legal in only some of them: ships can only be placed during setup, and shots can only be fired while playing. Writing that down first prevents most of the bugs.

Then list the illegal actions, because each one needs an answer. A ship placed off the board, overlapping another, or twice. An unknown ship name or direction. A shot off the board, or at a cell already fired at. A shot before the game starts or after it ends. A shot out of turn. These fall into two kinds. Either the request itself is wrong (`BadInput`, which the API will answer with `400`), or the request is fine but not allowed right now (`NotAllowed`, which becomes `409`).

<details><summary markdown="span">Execute! (the rules engine)</summary>

```python
SIZE  = 10
FLEET = {"carrier": 5, "battleship": 4, "cruiser": 3, "submarine": 3, "destroyer": 2}


class BadInput(Exception):
    pass # the request itself is wrong: the API answers 400


class NotAllowed(Exception):
    pass # fine request, but not allowed right now: the API answers 409


def new_game():
    return {"phase": "setup", "turn": None, "winner": None,
            "fleet": {"A": {}, "B": {}}, # player -> {ship name: its cells}
            "ships": {"A": {}, "B": {}}, # player -> {cell: ship name}
            "shots": {"A": set(), "B": set()}} # player -> the cells they fired at


def place(game, player, name, row, col, direction):
    if game["phase"] != "setup":
        raise NotAllowed("ships can only be placed during setup")

    if name not in FLEET or name in game["fleet"][player]:
        raise BadInput("unknown ship, or already placed: %s" % name)

    if direction not in ("H", "V"):
        raise BadInput("direction must be H or V")

    if not on_board((row, col)):
        raise BadInput("the start cell is off the board")

    cells = []
    for i in range(FLEET[name]):
        cells.append((row + i, col) if direction == "V" else (row, col + i))

    for cell in cells:
        if not on_board(cell):
            raise BadInput("%s does not fit on the board" % name)

        if cell in game["ships"][player]:
            raise BadInput("%s overlaps another ship" % name)

    game["fleet"][player][name] = cells
    for cell in cells:
        game["ships"][player][cell] = name

    if all(len(game["fleet"][p]) == len(FLEET) for p in "AB"):
        game["phase"] = "playing"
        game["turn"]  = "A"


def fire(game, player, row, col):
    if game["phase"] != "playing":
        raise NotAllowed("the game is not being played right now")

    if game["turn"] != player:
        raise NotAllowed("it is not your turn")

    cell = (row, col)
    if not on_board(cell):
        raise BadInput("that cell is off the board")

    if cell in game["shots"][player]:
        raise BadInput("you already fired at that cell")

    enemy = other(player)
    game["shots"][player].add(cell)

    result = "miss"
    name   = game["ships"][enemy].get(cell)

    if name:
        result = "sunk" if all(c in game["shots"][player] for c in game["fleet"][enemy][name]) else "hit"

    if all(c in game["shots"][player] for c in game["ships"][enemy]):
        game["phase"]  = "finished"
        game["winner"] = player
        game["turn"]   = None
    else:
        game["turn"] = enemy

    return {"result": result, "ship": name, "winner": game["winner"]}


def view(game, player):
    enemy = other(player)

    mine = []
    for cell, name in sorted(game["ships"][player].items()):
        mine.append({"row": cell[0], "col": cell[1], "ship": name,
                     "hit": cell in game["shots"][enemy]})

    fired = []
    for cell in sorted(game["shots"][player]):
        fired.append({"row": cell[0], "col": cell[1],
                      "hit": cell in game["ships"][enemy]})

    return {"phase": game["phase"], "turn": game["turn"], "winner": game["winner"],
            "ships_placed": sorted(game["fleet"][player]),
            "my_ships": mine, "my_shots": fired}


def on_board(cell):
    row, col = cell
    return (isinstance(row, int) and isinstance(col, int)
            and 0 <= row < SIZE and 0 <= col < SIZE)


def other(player):
    return "B" if player == "A" else "A"
```

</details>
<BR>


How it reads. `new_game` is a dictionary: the phase, whose turn it is, the winner, and for each player their fleet, the cells their ships cover, and the cells they have fired at. `place` checks the phase, then the ship name, direction and starting cell, then works out the cells and checks each one fits and is free, and only then saves the ship. When both fleets are complete the phase becomes `playing`, and A moves first. `fire` is a row of guard clauses in order: the phase, the turn, the cell is on the board, the cell has not been fired at. Only after all of them pass does it change anything. That ordering is deliberate: a refused shot does not cost the player their turn. After the shot it works out miss, hit or sunk, ends the game if the last ship went down, and otherwise passes the turn.

`view` is what a player is allowed to see: their own ships, with a mark on each cell the enemy has hit, and only the hits and misses of their own shots. It never contains the enemy's ship positions, so even a buggy client or a curious player cannot find them in a response.

### 4. The REST API

Now the thin layer. Each player gets a secret token when the game is created, and sends it in an `X-Player-Token` header. The routes are `POST /games` to create a game, `POST /games/{id}/ships` to place a ship, `POST /games/{id}/fire` to fire, and `GET /games/{id}` to look at your view.

<details><summary markdown="span">Execute! (the REST layer, with Flask)</summary>

```python
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
```

</details>
<BR>


How it reads. The two error types from the engine are turned into status codes in one place each: `BadInput` is `400` and `NotAllowed` is `409`, so none of the routes has to think about errors. A third, `ApiError`, covers the cases that belong to the API and not the rules: `404` when the game does not exist, and `401` when the token is missing or wrong. `find` looks up the game and works out which player the token belongs to. Each game has its own lock, so two requests for the same game cannot interleave, but different games never wait for each other. The routes themselves are short because every rule lives in the engine.

The status codes carry meaning. `400` means your input is wrong. `409` means the request is fine but not allowed right now. `401` means I do not know who you are, and `404` means that game does not exist. A real session against the server looks like this:

```
$ curl -s -X POST localhost:5057/games
{"id":"04d291b8","tokens":{"A":"15a967ee165729ff","B":"3d4b64b01816bb66"}}

$ place a destroyer at row 0, col 0, horizontal
{"my_ships":[{"col":0,"hit":false,"row":0,"ship":"destroyer"}, ...],"phase":"setup", ...}   [HTTP 201]

$ place a carrier at row 0, col 8 (does not fit)
{"error":"carrier does not fit on the board"}   [HTTP 400]

$ fire before the game has started
{"error":"the game is not being played right now"}   [HTTP 409]

$ look with a wrong token
{"error":"missing or wrong X-Player-Token"}   [HTTP 401]

$ look at a game that does not exist
{"error":"no such game"}   [HTTP 404]
```

I tested all of it, including the cases that are easy to get wrong: a refused shot keeps the turn, a whole game over HTTP from setup to a winner, random games that always end, a player never receiving the enemy's ships, a non-ASCII token answering `401` and not crashing, and several overlapping shots from one player letting exactly one through. Each rule was also broken on purpose to check that the tests notice.

### 5. Edge cases and what to watch for

**Two moves at the same moment.** The per-game lock makes them take turns, and the second one is refused as out of turn. With a database, store the game as a JSON document with a **version number** and update it only if the version has not changed, so two simultaneous moves cannot both win.

**State that survives a restart.** A dictionary is fine for the exercise. With a database, keep one row per game, with a column for the state and one for the version, updated in one transaction per move. The engine does not change, because it only works on the dictionary it is handed.

**Undo, replay and an audit trail.** Store the list of moves and not the state, and the state is just the moves replayed. You get undo, replay and a history for free.

**An AI opponent.** Start with random cells that have not been fired at. Then play smarter: after a hit, try the neighbouring cells first.

**Spectators.** A third kind of view that shows only the shots, never the ships.

**Telling a player the opponent has moved.** Polling is the simplest and fine to start. Server-sent events or WebSockets are the next step.

**`POST /fire` or `POST /moves`.** A `/moves` collection is more RESTful, and `/fire` reads more naturally. Mention both and pick one.

**Tokens or real sessions.** A token per player is simple and enough here. A real system would use real authentication.

**Cheating.** The token check, and the view never containing the enemy's ships. Never trust a client to tell you whether a shot hit.

**Tic-Tac-Toe is the same skeleton.** A 3 by 3 board, two players, the same three states, and a win check on the eight lines. If they ask for it, you keep everything except the rules.

**In a pairing session.** Start with the states and the list of illegal actions, out loud, because it shows you are designing and not just typing. Write the engine and one failing test first, then make it pass. Keep the API thin, and if you catch yourself putting a rule in it, move the rule into the engine. And say what you are leaving out and why: "no persistence yet, I would add it next."
