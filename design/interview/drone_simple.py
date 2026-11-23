drones = [] # the drone ids in this zip code
busy = set() # drones that are on a delivery right now


def place_order(order_id):
    for drone in drones:
        if drone not in busy:
            busy.add(drone)
            return drone

    return None # no drone is free: say so now
