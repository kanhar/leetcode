from audit_outbox import connect


def query(org, start, end, cursor=None, limit=50):
    db     = connect()
    cursor = cursor or (end, "")

    rows = db.execute("""SELECT ts, event_id, actor, action, target FROM archive
                         WHERE org = ? AND ts >= ? AND ts < ? AND (ts, event_id) < (?, ?)
                         ORDER BY ts DESC, event_id DESC LIMIT ?""",
                      (org, start, end, cursor[0], cursor[1], limit + 1)).fetchall()
    db.close()

    events      = rows[:limit]
    next_cursor = None
    if len(rows) > limit:
        next_cursor = (events[-1][0], events[-1][1])

    return {"events": events, "next_cursor": next_cursor}
