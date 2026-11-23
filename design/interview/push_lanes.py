from collections import deque

lanes = {"security": deque(), "direct": deque(), "watching": deque()}

ORDER = ["security"] * 6 + ["direct"] * 3 + ["watching"] # how many turns each lane gets out of ten
turn  = {"i": 0}


def put(lane, item):
    lanes[lane].append(item)


def take():
    for _ in range(len(ORDER)):
        lane = ORDER[turn["i"] % len(ORDER)]
        turn["i"] += 1

        if lanes[lane]:
            return lanes[lane].popleft()

    return None # all three lanes are empty
