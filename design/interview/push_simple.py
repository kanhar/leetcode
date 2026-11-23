from collections import defaultdict

watchers = defaultdict(set)  # repo -> the users who watch it
devices  = defaultdict(list) # user -> their phones and browsers
inbox    = defaultdict(list) # user -> the notifications waiting for them

send = None # send(device, notification) hands it to Apple or Google


def on_event(event):
    for user in watchers[event["repo"]]:
        inbox[user].append(event)

        for device in devices[user]:
            send(device, event)
