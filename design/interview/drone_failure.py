from drone_booking import place_order


def reassign(db, drones, order_id, failed, km, now, t2):
    with db:
        db.execute("DELETE FROM booked WHERE order_id = ?", (order_id,)) # give the failed drone's slots back

    others = [drone for drone in drones if drone != failed]
    drone, start = place_order(db, others, order_id, km, now, t2) # book again inside what is left of the window

    if drone is not None:
        with db:
            db.execute("UPDATE orders SET state = 'ASSIGNED', drone = ?, start = ? WHERE order_id = ?", (drone, start, order_id))

    return drone, start
