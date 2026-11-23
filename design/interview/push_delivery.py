sent = set() # ids of the notifications that went out
send = None  # send(note) returns once Apple or Google has accepted it


def deliver(note):
    if note["id"] in sent:
        return # already delivered

    send(note) # send first ...
    sent.add(note["id"]) # ... then write it down
