def place(servers, how_many=3):
    chosen = []
    racks  = set()

    for server in sorted(servers, key=lambda s: s["load"]):
        if server["down"] or server["rack"] in racks:
            continue # skip dead servers, and never two copies in one rack

        chosen.append(server["name"])
        racks.add(server["rack"])

        if len(chosen) == how_many:
            return chosen

    return None # not enough racks
