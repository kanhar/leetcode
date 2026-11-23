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
