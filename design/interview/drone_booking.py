import math
import sqlite3

SLOT = 15 # minutes: time is cut into slots like this
SPEED = 0.8 # km per minute, about 48 km/h
HANDLING = 10 # minutes to load at the depot and to hand over
BUFFER = 10 # minutes of safety margin
RANGE = 20 # km: farther than this we cannot deliver

# booked(drone TEXT, slot INTEGER, order_id TEXT, PRIMARY KEY (drone, slot))


def slots_needed(km):
    minutes = 2 * km / SPEED + HANDLING + BUFFER # there and back
    return math.ceil(minutes / SLOT)


def book(db, drone, first, last, order_id):
    try:
        with db:
            for slot in range(first, last + 1):
                db.execute("INSERT INTO booked VALUES (?, ?, ?)", (drone, slot, order_id))

        return True # every slot was free and is now ours
    except sqlite3.IntegrityError:
        return False # someone holds one of them, and nothing of ours was kept


def place_order(db, drones, order_id, km, t1, t2): # t1 and t2 are slot numbers
    if km > RANGE:
        return None, "OUT_OF_RANGE"

    need = slots_needed(km)

    for start in range(t1, t2 - need + 2): # the latest start still finishes by t2
        for drone in drones:
            if book(db, drone, start, start + need - 1, order_id):
                return drone, start

    return None, "NO_DRONE_AVAILABLE"
