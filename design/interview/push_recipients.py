from collections import defaultdict

RANK = {"watching": 1, "participating": 2, "mention": 3, "review_request": 3}

watchers     = defaultdict(set) # repo -> users who watch it
participants = defaultdict(set) # thread -> users who took part in it
prefs        = defaultdict(lambda: {"watching": True, "muted": set(), "quiet": (22, 7)})


def recipients(event):
    reasons = {}

    for user in watchers[event["repo"]]:
        reasons[user] = "watching"

    for user in participants[event["thread"]]:
        reasons[user] = strongest(reasons.get(user), "participating")

    for user in event.get("mentions", []):
        reasons[user] = strongest(reasons.get(user), "mention")

    for user in event.get("reviewers", []):
        reasons[user] = strongest(reasons.get(user), "review_request")

    if event["kind"] == "security":
        for user in event["admins"]:
            reasons[user] = "security"

    reasons.pop(event["actor"], None) # nobody is told about their own action
    return reasons


def channels(user, reason, thread, hour):
    p = prefs[user]

    if thread in p["muted"] and reason != "security":
        return [] # muted: nothing at all

    if reason == "watching" and not p["watching"]:
        return []

    where = ["inbox"] # the inbox is the source of truth, so it always gets it

    if reason == "security" or not in_quiet(hour, *p["quiet"]):
        where.append("push")

    return where


def strongest(old, new):
    return new if old is None or RANK[new] > RANK[old] else old


def in_quiet(hour, start, end):
    if start <= end:
        return start <= hour < end

    return hour >= start or hour < end # quiet hours that cross midnight
