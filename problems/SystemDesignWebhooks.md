{: .no_toc}
# Webhook Delivery and Back Pressure

> Design a system that can reliably and concurrently dispatch millions of third-party webhooks, for example alerting an external CI server whenever code is pushed to a repository, with strict retry policies and back pressure.

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

When someone pushes code, other people's servers want to know. A CI server wants to start a build, a chat room wants to post a message. They tell us a URL in advance, and every time something happens we send that URL a small JSON message. That is a **webhook**.

The hard part is that we do not control the other side. Their server might be slow, down, overloaded, or simply broken. We send millions of these a day, and a push must never be slowed down or lost because somebody else's server is having a bad afternoon.

This is also the best question for learning **back pressure**, because the whole problem is a fast sender (pushes) feeding slow, unreliable receivers (other people's servers). Back pressure means the slow side pushes back, so the fast side slows down, instead of work piling up without limit. Think of a kitchen that stops taking orders when the line is full.

I measured it. A sender with 30 events and an endpoint that takes 20 ms per event: with no limit on the queue, the sender finished instantly and all 30 events sat in memory at once. With a limit of 5, the sender was slowed to the endpoint's pace (half a second), and never more than 5 were waiting. With no limit, memory grows without bound, and in production that crashes you. With a limit, the sender is held back.

When a bounded queue is full you have three choices. You can make the sender **wait** until there is room. You can **reject** the new work, so the caller knows and can try later or answer 429 or 503. Or you can **spill** it into something bigger and durable, such as a disk-backed queue, and only slow down when that fills too. The code below shows the first two, and section 5 shows how the third one works.

### 2. The simplest version

A push happened, so call every URL that asked to hear about it, once.

<details><summary markdown="span">Execute! (the simplest version)</summary>

```python
subscribers = defaultdict(list) # repo -> the URLs that asked to hear about it
post = None # post(url, event) sends the request and returns the HTTP status


def on_push(repo, event):
    for url in subscribers[repo]:
        post(url, event)
```

</details>
<BR>


That is the whole idea, and it is wrong in four ways. A slow endpoint holds up every endpoint after it in the loop, and holds up the push itself. A failure is simply forgotten. A dead endpoint is called again and again forever. And if we crash halfway, some subscribers never hear about the push. The next sections fix these one at a time.

### 3. Retrying, the way a polite client does

The first fix is to retry, but only for failures that can get better. A `2xx` answer means delivered. A timeout, a `5xx`, a `408` or a `429` might work next time, so try again. Anything else, such as a `404` or a `401`, means the endpoint is set up wrongly, and no number of retries will fix that, so stop and tell the owner.

Between tries we wait, and the wait doubles each time: one second, two, four, eight, up to a cap. The wait is also **random**, anywhere between zero and that limit. This matters more than it looks. If an endpoint goes down with 10,000 events queued, and they all retry on the same schedule, they hit it together every time, and knock it over again. Random waits spread them out. If the endpoint sends a `Retry-After`, believe it over our own schedule. After a fixed number of tries the event goes to a **dead-letter** list, and somebody is told.

<details><summary markdown="span">Execute! (deliver with retries)</summary>

```python
post = None # post(url, event) returns (status, retry_after); status 0 means no answer at all
sleep = time.sleep
jitter = random.uniform

MAX_TRIES = 8
BASE = 1.0
CAP = 3600.0

dead_letters = []


def deliver(url, event):
    for attempt in range(MAX_TRIES):
        status, retry_after = post(url, event)

        if 200 <= status < 300:
            return True # delivered

        if not worth_retrying(status):
            break # the endpoint is set up wrongly, trying again will not help

        if attempt < MAX_TRIES - 1:
            sleep(wait_time(attempt, retry_after))

    dead_letters.append((url, event))
    return False


def worth_retrying(status):
    return status == 0 or status in (408, 429) or status >= 500


def wait_time(attempt, retry_after):
    if retry_after:
        return retry_after # the endpoint told us how long to wait

    ceiling = min(CAP, BASE * 2 ** attempt)
    return jitter(0, ceiling)
```

</details>
<BR>


`post` returns the status and the `Retry-After` value, and a status of 0 means no answer at all. `deliver` is the loop from above, with the three outcomes in order: delivered, not worth retrying, or wait and try again. `worth_retrying` and `wait_time` are separate functions so each rule is easy to see and to change.

### 4. One slow endpoint must not delay the others

The next problem is that a single slow endpoint holds up everyone. The fix is to give **each endpoint its own queue and its own worker**. A slow customer then fills only their own queue.

<details><summary markdown="span">Execute! (one bounded queue and one worker per endpoint)</summary>

```python
QUEUE_SIZE = 100

queues = {}
lock = threading.Lock()


def submit(url, event):
    queue_for(url).put(event) # waits here while this endpoint's queue is full


def try_submit(url, event):
    try:
        queue_for(url).put_nowait(event)
        return True # accepted
    except queue.Full:
        return False # full: the caller keeps the event and tries later


def queue_for(url):
    with lock:
        if url not in queues:
            queues[url] = queue.Queue(maxsize=QUEUE_SIZE)
            threading.Thread(target=worker, args=(url, queues[url]), daemon=True).start()

        return queues[url]


def worker(url, events):
    while True:
        event = events.get()
        deliver(url, event)
        events.task_done()
```

</details>
<BR>


How it reads. `queue_for` makes the queue for an endpoint the first time we see it, with a size limit, and starts a worker that takes events off that queue and delivers them with the retry loop from section 3. Because the queue has a limit, the sender has to deal with a full queue, and `submit` and `try_submit` are the two choices from the story. `submit` **waits** until there is room, which holds the sender back. `try_submit` **refuses** and says so, so the caller decides what to do. One worker per endpoint also keeps that endpoint's events in order.

### 5. Do not hold back the push itself

We said a push must never wait for somebody else's server. So the push itself does not call `submit`. It writes the event into an **outbox**, in the same database transaction as the push, and returns. A small relay moves events from the outbox into the endpoint queues.

<details><summary markdown="span">Execute! (the relay: take from the outbox only when there is room)</summary>

```python
outbox = [] # (url, event) pairs written by the push, in the same transaction as the push


def relay():
    for item in list(outbox):
        url, event = item

        if try_submit(url, event):
            outbox.remove(item)
        # otherwise it stays in the outbox, and the next pass tries again
```

</details>
<BR>


This is back pressure all the way back. If an endpoint's queue is full, `try_submit` says no, the event simply stays in the outbox, and the relay tries it again on the next pass. The memory queues stay small. The backlog builds up in the outbox, which is durable, and nothing is lost. This is also the third choice from the story: the outbox is the bigger place the overflow spills into. Events for a healthy endpoint are not held back by a full queue for a stuck one.

### 6. A dead endpoint should stop costing us anything

Retries with backoff already slow down, but an endpoint that has been dead for an hour still gets a request every time. A **circuit breaker** fixes that. After a number of failures in a row we pause the endpoint for a while and do not call it at all. Then we try once, and if it answers, we carry on.

<details><summary markdown="span">Execute! (a circuit breaker around post)</summary>

```python
real_post = None # the real post(url, event) returning (status, retry_after)
clock = time.time

FAILS_TO_PAUSE = 5
PAUSE_SECONDS = 60

fails  = defaultdict(int)
paused = {} # url -> when it may be tried again


def post(url, event):
    if clock() < paused.get(url, 0):
        return 503, None # paused: skip the call, so a dead endpoint costs nothing

    status, retry_after = real_post(url, event)

    if status == 0 or status >= 500:
        fails[url] += 1
    else:
        fails[url] = 0

    if fails[url] >= FAILS_TO_PAUSE:
        paused[url] = clock() + PAUSE_SECONDS
        fails[url] = 0

    return status, retry_after
```

</details>
<BR>


How it reads. It wraps `post`. While an endpoint is paused it answers "503" without making the call, which makes the retry loop wait, so a dead endpoint costs us nothing. A timeout or a `5xx` counts as a failure. A `4xx` does not, because that is a mistake in the setup and not a sign that the endpoint is down. A success resets the count. After a day or two of this, the hook should be disabled and the owner told.

I tested each of these pieces, including the cases that go wrong: a stuck endpoint with a full queue, a retry that gives up, a paused endpoint, and a relay that finds a full queue. Every piece was checked against a deliberately broken copy to see that the tests notice.

### 7. Edge cases and what to watch for

**Delivery is at least once.** If we send a webhook and then crash before we record that it worked, we send it again. So every delivery carries an ID, and the receiver is expected to ignore an ID it has already seen. Exactly once is not possible over HTTP, because we can never be sure whether a timed-out request arrived.

**Order.** Within one endpoint, events go out in order with one worker, but a retry can overtake a later event if you send them in parallel. Promise nothing beyond "best effort per endpoint", and never promise a global order, since that would force everything through one place.

**An endpoint is down for six hours.** The breaker stops us wasting calls, the events wait safely in the outbox, and at the end of the retry window they go to the dead-letter list. The customer can replay them from a dashboard, so keep a record of every attempt.

**The endpoint comes back.** Everything wants to retry at once. The random waits spread the retries out, and the replay should be rate limited so we do not knock it over again.

**One huge customer.** With a queue per endpoint they only fill their own, and a limit on how many requests one endpoint may have in flight at a time keeps them from using all of our capacity.

**Security.** Customers choose the URL, so never call internal addresses, or an attacker can aim us at our own network (this is called SSRF). Sign every payload, for example with an HMAC of the body using a secret the customer knows, so receivers can check it came from us. Use TLS only, and keep secrets out of the logs.

**Push or pull.** Webhooks push to the customer. An events API they poll is simpler for us and puts the back pressure on them, at the cost of some delay. Many systems offer both.

**Threads, async or processes.** Delivery spends its time waiting on the network, so threads or async fit. The code here uses threads for readability. Processes help only for CPU work such as signing at huge scale.

**Knowing it is healthy.** Watch queue depth, how far behind the workers are, success rate, retry rate and delivery time per endpoint, and alert when the lag grows.

Sources:

* [Webhook retry best practices (Hookdeck)](https://hookdeck.com/webhooks/guides/webhook-retry-best-practices)
* [Design webhook delivery (Exponent)](https://www.tryexponent.com/courses/system-design-interviews/design-webhook-delivery)
