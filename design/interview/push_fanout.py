from push_recipients import recipients, channels

PAGE = 1000

cursors  = {} # event id -> how far the coordinator got
notes    = {} # notification id -> the notification
outgoing = [] # ids of the notifications that still need a push


def fan_out(event, enqueue):
    reasons = recipients(event)
    users   = sorted(reasons)

    for i in range(cursors.get(event["id"], 0), len(users), PAGE):
        enqueue({"event": event, "reasons": {u: reasons[u] for u in users[i:i + PAGE]}})
        cursors[event["id"]] = i + PAGE # saved, so a crash resumes from here


def notify_chunk(task, hour):
    event = task["event"]

    for user, reason in task["reasons"].items():
        for channel in channels(user, reason, event["thread"], hour):
            note_id = f"{event['id']}/{user}/{channel}"

            if note_id in notes:
                continue # this chunk ran before: do nothing twice

            notes[note_id] = {"id": note_id, "user": user, "channel": channel, "event": event}

            if channel == "push":
                outgoing.append(note_id)
