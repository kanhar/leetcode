{: .no_toc}
# Push Notifications

> Design a push notification system for GitHub.

Related: [Audit Log System](SystemDesignAuditLog.md) and [The Binary SMS Tickle](SystemDesignSmsTickle.md).

<style>
/* Code on this page wraps instead of scrolling sideways, and the column is a little wider on desktop. */
pre, code { white-space: pre-wrap; overflow-wrap: anywhere; }
pre code { font-size: 12px; line-height: 1.45; }
@media (min-width: 961px) {
  .wrapper { width: 940px; }
  section { width: 640px; }
}
</style>

- TOC
{:toc}

### 1. What we are building

Somebody @mentions you in a pull request. A moment later your phone buzzes, the page you have open shows a red dot, and the notification is waiting in your inbox. One event, three places. And the same system also has to decide, for every event, **who** should hear about it, and **how loudly**. A comment on a repo with 100,000 watchers is one event and a hundred thousand recipients. A security alert has to arrive in seconds. Most of the rest can wait a minute, and most of it should not buzz anyone's phone at all.

Before designing, I would settle what is being asked. The channels are mobile push, desktop browser push, and the in-app inbox with its live red dot, and email and others can plug in later. The events are mentions, review requests, assignments, CI results, security alerts, and activity on repos you watch. The scale is about 100 million a day, around 1,200 a second on average, with bursts of 10 to 50 times when one event fans out to a big repo. The user decides what they get: watch levels per repo, per-channel settings, mute and quiet hours. Seconds are needed for security and direct notifications, and a minute or more is fine for "watching". Private repos matter: payloads are minimal, and nothing is sent about a repo the user cannot access.

Then two assumptions to confirm out loud. **A push is best-effort, and the in-app inbox is the source of truth**: a late or missed push is tolerable, but losing the inbox entry is not. And **the product action must never fail or slow down because a notification cannot be sent**, which is the opposite of an audit log, where the action would fail. Given those, I would also say that I would rather send a duplicate than lose a notification, and rather delay a push than send a flood.

The sentence to anchor on: a push notification system is a fan-out, filter and deliver pipeline, and timeliness and not annoying the user matter more than completeness.

### 2. The simplest version

An event happened, so for every user watching the repo, put it in their inbox and send a push to each of their devices.

<details><summary markdown="span">Execute! (the simplest version)</summary>

```python
watchers = defaultdict(set)  # repo -> the users who watch it
devices  = defaultdict(list) # user -> their phones and browsers
inbox    = defaultdict(list) # user -> the notifications waiting for them

send = None # send(device, notification) hands it to Apple or Google


def on_event(event):
    for user in watchers[event["repo"]]:
        inbox[user].append(event)

        for device in devices[user]:
            send(device, event)
```

</details>
<BR>


It is a start, and it is wrong in several ways. It ignores what people asked for: their preferences, muted threads, quiet hours. A person who both watches the repo and is @mentioned would get two notifications. It tells you about your own actions. One slow push provider holds up the whole loop, and a crash halfway through leaves some people notified and some not. And for a big repo the loop is one enormous piece of work. The next sections fix these one at a time.

### 3. Deciding who hears about it

First, who. The recipients of an event come from several places: the people watching the repo, the people who took part in the thread, the people @mentioned, the people asked to review, and for a security event the admins. Many people appear more than once, and each should get **one** notification, for their **strongest reason**: a mention beats participating, which beats watching, and a security alert beats everything. Nobody is told about their own action.

Then, what they get. Each person's settings decide it. A muted thread produces nothing, except a security alert. Someone who stopped watching hears nothing from "watching". And the inbox always gets the entry, because it is the source of truth, but the **push** is held back during the person's quiet hours, unless it is a security alert.

<details><summary markdown="span">Execute! (recipients with their strongest reason, and the channels each one gets)</summary>

```python
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
```

</details>
<BR>


`recipients` builds a dictionary of user to reason, letting a stronger reason replace a weaker one, and removes the actor. `channels` answers "which of inbox and push does this person get?", and `in_quiet` handles hours that cross midnight, such as 22 to 7.

### 4. Fan-out in chunks that can restart

One event can mean one recipient or a million, and push needs one message per recipient. Doing that in one loop is fragile, so a **coordinator** reads the recipients in pages of about a thousand and queues one task per page. It saves how far it got, so a crash resumes from there and not from the start. Each **chunk worker** then applies the filters, writes the inbox entries and creates the push tasks.

<details><summary markdown="span">Execute! (a coordinator that resumes, and chunks that can safely run twice)</summary>

```python
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
```

</details>
<BR>


The important detail is the **deterministic ID**. Every notification has an ID made from the event, the user and the channel, and a chunk skips any ID it has already written. That means a chunk can run twice, or a coordinator can queue the same chunk twice after a crash, and nothing is sent twice. I tested it the hard way: a coordinator that crashes at random, before and after queueing, a whole run repeated, and chunks run again, and every person still got exactly one inbox entry and one push.

### 5. Urgent things must not wait behind a broadcast

Imagine a 100,000-person broadcast is already queued, and then someone @mentions you. In one shared queue, your mention waits behind a hundred thousand others. So there are **three lanes**: security, direct (mentions, review requests), and watching. A worker takes from them in a weighted rotation, six turns for security, three for direct and one for watching in every ten.

<details><summary markdown="span">Execute! (three priority lanes with weighted turns)</summary>

```python
lanes = {"security": deque(), "direct": deque(), "watching": deque()}

ORDER = ["security"] * 6 + ["direct"] * 3 + ["watching"] # how many turns each lane gets out of ten
turn  = {"i": 0}


def put(lane, item):
    lanes[lane].append(item)


def take():
    for _ in range(len(ORDER)):
        lane = ORDER[turn["i"] % len(ORDER)]
        turn["i"] += 1

        if lanes[lane]:
            return lanes[lane].popleft()

    return None # all three lanes are empty
```

</details>
<BR>


I measured it. With 100,000 broadcast notifications queued and then one mention, the mention came out within the first ten takes. In a single shared queue it would have waited behind all 100,000. And the broadcast does not starve: while urgent traffic keeps coming, the broadcast still gets its turns, and a lane with nothing in it gives its turns to the next one. Spread huge fan-outs over a minute or so with a little jitter, to protect the queue and the providers.

### 6. Delivery without losing a notification

The order of one small step matters more than it looks. When a worker delivers a notification, it has to send it and also remember that it did. A common design **claims a key first** and then sends, so a retry sees the claim and does nothing. But if the worker crashes between the claim and the send, the retry sees the claim and gives up, and the notification is **silently lost**. The other order is to **send first and then write it down**. Now a crash between the two means the retry sends it again, so you get a **duplicate**, but never a loss.

<details><summary markdown="span">Execute! (send first, then mark it as sent)</summary>

```python
sent = set() # ids of the notifications that went out
send = None  # send(note) returns once Apple or Google has accepted it


def deliver(note):
    if note["id"] in sent:
        return # already delivered

    send(note) # send first ...
    sent.add(note["id"]) # ... then write it down
```

</details>
<BR>


I simulated both with a worker that crashes with a 2 percent chance before each step, and whose message is redelivered after every crash, on 200,000 notifications. Claiming first lost 4,034 of them and sent none twice. Sending first lost none and sent 4,044 twice. Given my assumption, a duplicate over a loss, I send first, and I make the duplicates harmless with the deterministic ID plus a **collapse key**, also called a tag, so the phone shows one notification and not two.

Around that step: one adapter and one queue per provider, so an outage at Apple cannot block Google. Retries with exponential backoff and jitter, as in [Webhook Delivery and Back Pressure](SystemDesignWebhooks.md), and a dead-letter queue for what never works. Dead tokens and browser subscriptions are removed when the provider says "gone". After an outage, drain gradually and do not flood. And the **inbox is the backstop**: if a push is dropped, the notification is still there when the user opens the app.

### 7. Edge cases and what to watch for

**Apple or Google is down.** Retries with backoff, the queue grows, and the inbox still shows everything.

**The queue backs up.** The priority lanes keep important notifications moving.

**A duplicate event.** The deterministic ID, and the collapse key on the device, drop or merge it.

**The preference service is down.** Send only high-priority notifications, with a cached or default set of preferences.

**The live gateway is down.** The red dot falls back to polling the unread count.

**Getting the events in.** Services write an outbox and a durable queue, so an event is never lost between "it happened" and "it was queued". The alternative, calling a notification API directly, ties the product's availability to ours.

**Fan-out on write or on read.** On write, as here, is simple and fast to read. For enormous repos a hybrid is possible: fan out to the active people now, and compute the rest when they look.

**The live red dot.** A per-user unread counter pushed over server-sent events, with polling as a fallback.

**Browser push.** A service worker, a stored subscription, and an encrypted request signed with our key. Delete the subscription when the person logs out.

**Read state must sync everywhere**, so marking a notification read on the web clears the badge on the phone and the dot.

**Access checks** at send time and again at open time, with minimal payloads, so a notification never reveals a repo someone can no longer see.

**The APIs.** Internal: `POST /notifications` with a type, a target, an idempotency key and a payload. For people: `GET /me/notifications?cursor=` and `POST /me/notifications/{id}/read`, plus an unread count; `PUT /me/preferences`; and `POST /me/devices` to register a token or a browser subscription.

I tested every piece, including the cases that go wrong: a coordinator that crashes at random, a chunk that runs twice, quiet hours across midnight, a muted thread that still lets a security alert through, a broadcast ahead of a mention, and both orders of the delivery step. Each rule was also broken on purpose to see that the tests notice.
