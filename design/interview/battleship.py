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
