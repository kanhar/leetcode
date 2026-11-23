from log_aggregator import logs


def get_logs_page(tenant, start, end, limit=500, cursor=None):
    first = logs[tenant].bisect_left((start,))
    last  = logs[tenant].bisect_left((end,))

    if cursor:
        time, server, seq = cursor
        first = logs[tenant].bisect_left((time, server, seq + 1))

    stop = min(last, first + limit)

    lines = []
    for time, server, seq, level, message in logs[tenant][first:stop]:
        lines.append({"time": time,   "server": server,
                      "level": level, "message": message})

    next_cursor = None
    if stop < last:
        time, server, seq, level, message = logs[tenant][stop - 1]
        next_cursor = (time, server, seq)

    return {"lines": lines, "next_cursor": next_cursor}
