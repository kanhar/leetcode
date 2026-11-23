"""Tests for the Battleship files: the simple version, the rules engine and the REST layer. Run: python -m unittest"""
import random
import threading
import time
import unittest

import battleship as bs
import battleship_api as api
import battleship_simple as simple

FLEET_A = [("carrier", 0, 0, "H"), ("battleship", 1, 0, "H"), ("cruiser", 2, 0, "H"), ("submarine", 3, 0, "H"), ("destroyer", 4, 0, "H")]
FLEET_B = [("carrier", 5, 0, "V"), ("battleship", 5, 1, "V"), ("cruiser", 5, 2, "V"), ("submarine", 5, 3, "V"), ("destroyer", 5, 4, "V")]


def place_fleet(game, player, fleet):
    for name, row, col, direction in fleet:
        bs.place(game, player, name, row, col, direction)


def started_game():
    game = bs.new_game()
    place_fleet(game, "A", FLEET_A)
    place_fleet(game, "B", FLEET_B)
    return game


def cells_of(fleet):
    cells = []
    for name, row, col, direction in fleet:
        for i in range(bs.FLEET[name]):
            cells.append((row, col + i) if direction == "H" else (row + i, col))
    return cells


class SimpleTests(unittest.TestCase):
    def setUp(self):
        simple.ships["A"] = {(0, 0), (0, 1)}
        simple.ships["B"] = {(5, 5)}
        simple.shots["A"] = set()
        simple.shots["B"] = set()

    def test_hit_and_miss(self):
        self.assertEqual(simple.fire("A", (5, 5)), "hit")
        self.assertEqual(simple.fire("A", (1, 1)), "miss")

    def test_the_winner_is_whoever_hit_every_enemy_cell(self):
        self.assertIsNone(simple.winner())
        simple.fire("B", (0, 0))
        self.assertIsNone(simple.winner())
        simple.fire("B", (0, 1))
        self.assertEqual(simple.winner(), "B")


class PlacementTests(unittest.TestCase):
    def test_a_ship_covers_the_right_cells(self):
        game = bs.new_game()
        bs.place(game, "A", "destroyer", 3, 4, "V")
        self.assertEqual(game["fleet"]["A"]["destroyer"], [(3, 4), (4, 4)])

    def test_bad_placements_are_bad_input_and_change_nothing(self):
        game = bs.new_game()
        bs.place(game, "A", "cruiser", 0, 0, "H")
        bad = [
            ("sloop", 5, 5, "H"), ("cruiser", 5, 5, "H"), ("carrier", 0, 8, "H"), ("carrier", 8, 0, "V"),
            ("carrier", 0, 0, "H"), ("carrier", 0, 2, "V"), ("carrier", 5, 5, "X"), ("carrier", -1, 0, "H"),
            ("carrier", None, 0, "H"), ("carrier", "a", 0, "H"), ("carrier", 0, 10, "H"),
        ]
        for name, row, col, direction in bad:
            with self.subTest(name=name, row=row, col=col, direction=direction):
                with self.assertRaises(bs.BadInput):
                    bs.place(game, "A", name, row, col, direction)
        self.assertEqual(list(game["fleet"]["A"]), ["cruiser"])
        self.assertEqual(len(game["ships"]["A"]), 3)

    def test_the_two_players_boards_are_separate(self):
        game = bs.new_game()
        bs.place(game, "A", "carrier", 0, 0, "H")
        bs.place(game, "B", "carrier", 0, 0, "H")
        self.assertEqual(len(game["ships"]["B"]), 5)

    def test_the_game_starts_when_both_fleets_are_placed_and_a_moves_first(self):
        game = bs.new_game()
        place_fleet(game, "A", FLEET_A)
        self.assertEqual((game["phase"], game["turn"]), ("setup", None))
        place_fleet(game, "B", FLEET_B)
        self.assertEqual((game["phase"], game["turn"]), ("playing", "A"))

    def test_ships_cannot_be_placed_once_the_game_has_started(self):
        game = started_game()
        with self.assertRaises(bs.NotAllowed):
            bs.place(game, "A", "carrier", 9, 0, "H")


class FiringTests(unittest.TestCase):
    def test_firing_before_the_game_starts_is_not_allowed(self):
        game = bs.new_game()
        with self.assertRaises(bs.NotAllowed):
            bs.fire(game, "A", 0, 0)

    def test_hit_miss_and_sunk(self):
        game = started_game()
        self.assertEqual(bs.fire(game, "A", 9, 9)["result"], "miss")
        self.assertEqual(bs.fire(game, "B", 0, 0)["result"], "hit")
        self.assertEqual(bs.fire(game, "A", 9, 8)["result"], "miss")
        bs.fire(game, "B", 0, 1)
        bs.fire(game, "A", 9, 7)
        bs.fire(game, "B", 0, 2)
        bs.fire(game, "A", 9, 6)
        bs.fire(game, "B", 0, 3)
        bs.fire(game, "A", 9, 5)
        answer = bs.fire(game, "B", 0, 4)
        self.assertEqual((answer["result"], answer["ship"]), ("sunk", "carrier"))

    def test_turns_alternate_and_the_wrong_player_is_refused(self):
        game = started_game()
        with self.assertRaises(bs.NotAllowed):
            bs.fire(game, "B", 0, 0)
        bs.fire(game, "A", 9, 9)
        self.assertEqual(game["turn"], "B")
        with self.assertRaises(bs.NotAllowed):
            bs.fire(game, "A", 9, 8)

    def test_a_refused_shot_does_not_cost_the_turn(self):
        game = started_game()
        bs.fire(game, "A", 9, 9)
        bs.fire(game, "B", 9, 9)
        for bad in [(9, 9), (10, 0), (-1, 0), (None, 0), ("a", "b")]:
            with self.assertRaises(bs.BadInput):
                bs.fire(game, "A", *bad)
            self.assertEqual(game["turn"], "A")

    def test_a_whole_game_plays_through_to_a_winner(self):
        game = started_game()
        targets_a = cells_of(FLEET_B)
        targets_b = cells_of(FLEET_A)
        spare = [(9, c) for c in range(10)] + [(8, c) for c in range(10)]
        step = 0
        while game["phase"] == "playing":
            if game["turn"] == "A":
                answer = bs.fire(game, "A", *targets_a.pop(0))
            else:
                answer = bs.fire(game, "B", *spare[step % len(spare)])
                step += 1
        self.assertEqual((game["phase"], game["winner"], game["turn"]), ("finished", "A", None))
        self.assertEqual(answer["winner"], "A")
        with self.assertRaises(bs.NotAllowed):
            bs.fire(game, "B", 0, 0)

    def test_random_games_always_end_with_a_winner_after_at_most_all_cells(self):
        rng = random.Random(4)
        for trial in range(60):
            game = bs.new_game()
            for player in "AB":
                for name in bs.FLEET:
                    while name not in game["fleet"][player]:
                        try:
                            bs.place(game, player, name, rng.randrange(10), rng.randrange(10), rng.choice("HV"))
                        except bs.BadInput:
                            pass
            order = {p: [(r, c) for r in range(10) for c in range(10)] for p in "AB"}
            for p in "AB":
                rng.shuffle(order[p])
            moves = 0
            while game["phase"] == "playing":
                player = game["turn"]
                bs.fire(game, player, *order[player].pop())
                moves += 1
                self.assertLessEqual(moves, 200)
            enemy = bs.other(game["winner"])
            self.assertTrue(set(game["ships"][enemy]) <= game["shots"][game["winner"]])


class ViewTests(unittest.TestCase):
    def test_a_player_never_sees_the_enemy_ships(self):
        game = started_game()
        bs.fire(game, "A", 5, 0)
        bs.fire(game, "B", 9, 9)
        shown = bs.view(game, "A")
        self.assertEqual(len(shown["my_ships"]), 17)
        self.assertEqual(shown["my_shots"], [{"row": 5, "col": 0, "hit": True}])
        enemy_cells = {cell for cell in game["ships"]["B"]}
        flat = str(shown)
        for row, col in enemy_cells - {(5, 0)}:
            self.assertNotIn("'row': %d, 'col': %d, 'ship'" % (row, col), flat)

    def test_my_ships_show_where_the_enemy_has_hit_them(self):
        game = started_game()
        bs.fire(game, "A", 5, 0)
        bs.fire(game, "B", 0, 0)
        shown = bs.view(game, "A")
        hit = [s for s in shown["my_ships"] if s["hit"]]
        self.assertEqual([(s["row"], s["col"]) for s in hit], [(0, 0)])


class ApiTests(unittest.TestCase):
    def setUp(self):
        api.games.clear()
        self.client = api.app.test_client()

    def new_game(self):
        made = self.client.post("/games")
        self.assertEqual(made.status_code, 201)
        return made.json["id"], made.json["tokens"]

    def post(self, path, token, body=None):
        headers = {"X-Player-Token": token} if token is not None else {}
        return self.client.post(path, json=body, headers=headers)

    def ready_game(self):
        game_id, tokens = self.new_game()
        for token, fleet in ((tokens["A"], FLEET_A), (tokens["B"], FLEET_B)):
            for name, row, col, direction in fleet:
                answer = self.post("/games/%s/ships" % game_id, token, {"ship": name, "row": row, "col": col, "orientation": direction})
                self.assertEqual(answer.status_code, 201)
        return game_id, tokens

    def test_create_place_fire_and_look(self):
        game_id, tokens = self.ready_game()
        shot = self.post("/games/%s/fire" % game_id, tokens["A"], {"row": 5, "col": 0})
        self.assertEqual((shot.status_code, shot.json["result"]), (200, "hit"))
        looked = self.client.get("/games/" + game_id, headers={"X-Player-Token": tokens["B"]})
        self.assertEqual(looked.status_code, 200)
        self.assertEqual(looked.json["turn"], "B")

    def test_status_codes_mean_what_they_should(self):
        game_id, tokens = self.new_game()
        base = "/games/" + game_id
        ship = {"ship": "carrier", "row": 0, "col": 8, "orientation": "H"}
        self.assertEqual(self.post(base + "/ships", tokens["A"], ship).status_code, 400)
        self.assertEqual(self.post(base + "/ships", tokens["A"], {}).status_code, 400)
        self.assertEqual(self.post(base + "/fire", tokens["A"], {"row": 0, "col": 0}).status_code, 409)
        self.assertEqual(self.post(base + "/fire", "wrong", {"row": 0, "col": 0}).status_code, 401)
        self.assertEqual(self.post(base + "/fire", None, {"row": 0, "col": 0}).status_code, 401)
        self.assertEqual(self.post("/games/nope/fire", tokens["A"], {"row": 0, "col": 0}).status_code, 404)

    def test_a_shot_out_of_turn_is_409_and_a_bad_shot_is_400(self):
        game_id, tokens = self.ready_game()
        path = "/games/%s/fire" % game_id
        self.assertEqual(self.post(path, tokens["B"], {"row": 0, "col": 0}).status_code, 409)
        self.assertEqual(self.post(path, tokens["A"], {"row": 99, "col": 0}).status_code, 400)
        self.assertEqual(self.post(path, tokens["A"], {"row": "x"}).status_code, 400)
        self.assertEqual(self.post(path, tokens["A"], {"row": 9, "col": 9}).status_code, 200)

    def test_a_non_ascii_token_is_401_not_a_crash(self):
        game_id, tokens = self.new_game()
        answer = self.client.get("/games/" + game_id, headers={"X-Player-Token": "café".encode("utf-8").decode("latin-1")})
        self.assertEqual(answer.status_code, 401)

    def test_a_player_cannot_act_as_the_other(self):
        game_id, tokens = self.ready_game()
        looked = self.client.get("/games/" + game_id, headers={"X-Player-Token": tokens["A"]})
        self.assertEqual(len(looked.json["my_ships"]), 17)
        self.assertNotIn("B", str(looked.json["ships_placed"]))

    def test_every_error_has_the_same_shape(self):
        game_id, tokens = self.new_game()
        for answer in (self.post("/games/nope/fire", "x", {}), self.post("/games/%s/fire" % game_id, "x", {}),
                       self.post("/games/%s/fire" % game_id, tokens["A"], {"row": 0, "col": 0}),
                       self.post("/games/%s/ships" % game_id, tokens["A"], {})):
            self.assertEqual(list(answer.json), ["error"])

    def test_a_whole_game_over_http(self):
        game_id, tokens = self.ready_game()
        path = "/games/%s/fire" % game_id
        targets = cells_of(FLEET_B)
        last = None
        for i, cell in enumerate(targets):
            last = self.post(path, tokens["A"], {"row": cell[0], "col": cell[1]})
            self.assertEqual(last.status_code, 200)
            if i < len(targets) - 1:
                self.assertEqual(self.post(path, tokens["B"], {"row": 9 - i // 10, "col": i % 10}).status_code, 200)
        self.assertEqual(last.json["winner"], "A")
        self.assertEqual(self.post(path, tokens["B"], {"row": 0, "col": 0}).status_code, 409)

    def test_two_simultaneous_shots_from_one_player_let_exactly_one_through(self):
        for round_number in range(20):
            game_id, tokens = self.ready_game()
            path = "/games/%s/fire" % game_id
            codes = []
            lock = threading.Lock()

            def shoot(col):
                code = self.post(path, tokens["A"], {"row": 9, "col": col}).status_code
                with lock:
                    codes.append(code)

            threads = [threading.Thread(target=shoot, args=(c,)) for c in range(4)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(sorted(codes), [200, 409, 409, 409], codes)

    def test_overlapping_shots_from_one_player_still_let_exactly_one_through(self):
        class SlowSet(set):
            def add(self, item):
                time.sleep(0.01)
                super().add(item)

        for round_number in range(5):
            game_id, tokens = self.ready_game()
            api.games[game_id]["game"]["shots"]["A"] = SlowSet()
            path = "/games/%s/fire" % game_id
            codes = []
            lock = threading.Lock()

            def shoot(col):
                code = self.post(path, tokens["A"], {"row": 9, "col": col}).status_code
                with lock:
                    codes.append(code)

            threads = [threading.Thread(target=shoot, args=(c,)) for c in range(4)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
            self.assertEqual(sorted(codes), [200, 409, 409, 409], codes)
            self.assertEqual(len(api.games[game_id]["game"]["shots"]["A"]), 1)


if __name__ == "__main__":
    unittest.main()
