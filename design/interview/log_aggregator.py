from collections import defaultdict
from sortedcontainers import SortedList

logs = defaultdict(SortedList)
seen = set()


def upload_batch(tenant, server_id, batch_id, lines):
    if (tenant, server_id, batch_id) in seen:
        return 200 # OK

    seen.add((tenant, server_id, batch_id))

    for line in lines:
        time, seq, level, message = unpack(line)
        logs[tenant].add((time, server_id, seq, level, message))

    return 202 # accepted


def get_logs(tenant, start, end):
    first = logs[tenant].bisect_left((start,))
    last  = logs[tenant].bisect_left((end,))

    lines = []
    for time, server, seq, level, message in logs[tenant][first:last]:
        lines.append({"time": time,   "server": server,
                      "level": level, "message": message})

    return lines # Or json.dumps(lines) if you want to return JSON


def unpack(line):
    return line["time"], line["seq"], line["level"], line["message"]
