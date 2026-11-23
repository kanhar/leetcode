from drone_booking import place_order

# orders(order_id TEXT PRIMARY KEY, state TEXT, drone TEXT, start INTEGER)


def create(db, order_id):
    with db:
        done = db.execute("INSERT OR IGNORE INTO orders VALUES (?, 'PLACED', NULL, NULL)", (order_id,))

    return done.rowcount == 1 # False: we already had this order, so a retry changes nothing


def move(db, order_id, old, new):
    with db:
        done = db.execute("UPDATE orders SET state = ? WHERE order_id = ? AND state = ?", (new, order_id, old))

    return done.rowcount == 1 # only one caller can make this particular move


def current(db, order_id):
    return db.execute("SELECT state, drone, start FROM orders WHERE order_id = ?", (order_id,)).fetchone()


def place(db, drones, order_id, km, t1, t2):
    if not create(db, order_id):
        return current(db, order_id) # a retry: answer exactly as before

    drone, detail = place_order(db, drones, order_id, km, t1, t2) # detail: the start slot, or the reason for saying no

    if drone is None:
        move(db, order_id, "PLACED", "REJECTED")
        return "REJECTED", None, detail

    with db:
        db.execute("UPDATE orders SET state = 'ASSIGNED', drone = ?, start = ? WHERE order_id = ?", (drone, detail, order_id))

    return "ASSIGNED", drone, detail


def delivered(db, order_id, drone, notify):
    with db:
        done = db.execute("UPDATE orders SET state = 'DELIVERED' WHERE order_id = ? AND state = 'DELIVERING' AND drone = ?", (order_id, drone))

    if done.rowcount == 1: # only the drone that holds the order can finish it
        notify(order_id) # runs once, however many times that drone reports it
