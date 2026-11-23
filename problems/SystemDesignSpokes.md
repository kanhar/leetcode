{: .no_toc}
# Git Storage (Spokes)

> How would you design the backend to store, replicate and manage millions of Git repositories globally, with strong consistency on writes and low latency on reads?

You are interviewing at the company that built an answer to this, and published it. The best preparation is to know their design well, and to say clearly which parts come from their posts and which parts are your own reasoning.

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

Every repository on GitHub is a Git repository sitting on some server's disk. Tens of millions of them: GitHub reports over 38 million repositories and 36 million gists on Spokes. A push must never be lost once it has been acknowledged. Any read after that push must see it. Two pushes at the same moment must never leave the copies disagreeing. Reads should keep working through failures, and it is acceptable to refuse a write that cannot be made safe. In the words you would say aloud: this is a CP system for writes. When I have to choose between accepting a write and keeping the replicas consistent, I choose consistency.

The older design copied whole disks (RAID and DRBD), with servers in pairs and a spare. When a server failed, a human had to confirm the fault before failing over, and that meant downtime. Spokes keeps each repository as **ordinary Git repositories on at least three servers, and makes every write win a vote of a majority.** Everything else is detail on top of that: how the vote works, how reads find a good copy, and how the system heals when a server dies.

Copying at the application level, one repository at a time, has real benefits. Each repository can live on any three servers and move independently. Any up-to-date copy can serve a read. One bad repository does not take a whole disk's worth of others with it. The price is that you must build your own locking, ordering, failure detection and re-copying, which block-level mirroring used to give you for free. Copies live on local SSDs and not on a network filesystem, because Git is very sensitive to latency.

To keep the code small, a repository here is just its **head**, the commit its main branch points at. A write is "move the head from `old` to `new`", and it only works if the head really is `old`. That is exactly the rule Git applies when you push, and it is what stops two people from silently overwriting each other.

### 2. The simplest version: one server

<details><summary markdown="span">Execute! (one copy of every repository)</summary>

```python
heads = {} # repo -> the commit its main branch points at


def write(repo, old, new):
    if heads.get(repo) != old:
        return False # somebody else moved it first

    heads[repo] = new
    return True


def read(repo):
    return heads.get(repo)
```

</details>
<BR>


`write` refuses unless the caller started from the current head, and `read` returns it. This is correct, and it is as far as one machine can go. When that machine dies, the repository is unavailable, and if its disk dies, the repository is gone. We need more than one copy.

### 3. Three copies, and a vote

The obvious next step is three copies and writing to all of them. But that is not enough. Two people pushing at the same moment can leave the copies disagreeing. A copy that was switched off during a push comes back with old data and quietly serves it. And a push that reached only one copy must not count as saved.

GitHub's own post gives the answer. A write takes an **exclusive lock on a majority** of the copies, so two writers can never both hold a majority, and concurrent writes to the same repository are serialized. The write is applied on the copies, and it is accepted only if a **strict majority** produce the same result, which with three copies means two of three. If a majority cannot agree, the write is reverted everywhere it was applied.

<details><summary markdown="span">Execute! (three copies, and a vote on every write)</summary>

```python
copies = [{}, {}, {}]          # three replicas, each: repo -> head commit
down   = set()                 # replicas we cannot reach right now
stale  = [set(), set(), set()] # per replica: the repos it missed a write for
locks  = defaultdict(threading.Lock)


def write(repo, old, new):
    with locks[repo]: # one write per repo at a time
        voters = [i for i in range(3) if i not in down and repo not in stale[i]]

        if len(voters) < 2:
            return False # no majority is reachable, so refuse the write

        applied = []
        for i in voters:
            if copies[i].get(repo) == old:
                copies[i][repo] = new
                applied.append(i)

        if len(applied) < 2:
            for i in applied:
                copies[i][repo] = old # no majority agreed: undo it everywhere
            return False

        for i in range(3):
            if i not in applied:
                stale[i].add(repo) # it missed this write: unhealthy until repaired

        return True
```

</details>
<BR>


How it reads. The lock on the repository stands in for the majority lock. The **voters** are the copies that are reachable and up to date, and if fewer than two are left the write is refused: that is the "consistency over availability" choice, in one line. Each voter applies the write only if its head is the `old` one the caller expected. If fewer than two applied it, the ones that did are put back, so a half-done write never survives. When the write succeeds, any copy that did not take part, because it was down or behind, is marked **stale** for that repository: unhealthy, and not allowed to vote or serve reads until it is repaired. GitHub reports that only a few dozen writes a day are non-unanimous, and that lagging copies usually recover within a minute or two. A later GitHub post adds two details: Git reference updates are transactional, so each copy either commits the whole update or rolls it back, and a checksum is computed after every update to confirm the copies match.

### 4. Reading, and healing

A read only comes from a copy that is up to date. In GitHub's design a routing query returns the up-to-date copies for the repository, about three, in order of preference. The application server tries the first one, and if that refuses, times out or errors, it tries the next. A server that has been marked offline moves to the end of the list but is still tried as a last resort. The result is that reads stay available as long as one up-to-date copy answers, even when writes are being refused. That asymmetry is deliberate.

Healing is its own small job. A periodic check compares each repository's number of healthy copies with the number we want, and re-copies from a good one. In the model that is `repair`.

<details><summary markdown="span">Execute! (reads from good copies, and repair)</summary>

```python
class Unavailable(Exception):
    pass


def read(repo):
    for i in range(3):
        if i not in down and repo not in stale[i]:
            return copies[i].get(repo)

    raise Unavailable(repo) # better an error than an old answer


def repair(repo):
    good = [i for i in range(3) if i not in down and repo not in stale[i]]

    if not good:
        return False # nobody to copy from

    for i in range(3):
        if i not in down and repo in stale[i]:
            copies[i][repo] = copies[good[0]][repo] # copy from a good replica
            stale[i].discard(repo)

    return True
```

</details>
<BR>


`read` skips copies that are down or stale, and if none is left it raises an error. An error is better than an old answer. `repair` copies the latest head from a good copy to each stale one that is reachable, and then the copy is allowed to vote again. In GitHub's system every server is both a source and a destination for these copies, so recovery gets faster as the cluster gets bigger, because many servers share the work.

I ran this model with random failures: copies going up and down, writes from out-of-date views, repairs and reads, many hundreds of times. Every copy that was not marked stale always held the latest acknowledged write, every read was either that value or a refusal, and many writers overlapping on one repository always produced exactly one winner. It is a teaching model, not GitHub's code.

### 5. Where the copies live

GitHub places at least three copies of each repository, and no two in the same rack, with a rack treated as an availability zone. In the model that is `place`.

<details><summary markdown="span">Execute! (choose servers in different racks)</summary>

```python
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
```

</details>
<BR>


It walks the servers from least loaded to most loaded, skips dead ones, and never takes two from one rack, so one rack failing costs at most one copy.

Adding servers needs no planning in GitHub's design: existing repositories are moved onto the new ones until the load evens out, and busy repositories can be moved to spread the load. To reboot a server for maintenance, it is marked offline for new reads while the reads already in progress, such as long clones, are allowed to finish. It keeps receiving writes so it stays close, and racks are rolled through a few servers at a time.

Failures are noticed from **real traffic**, not only from heartbeats. A server that fails three requests in a row is marked offline, and a successful heartbeat marks it online again. Each application server keeps its own view. If many application servers mark one file server offline, that file server is probably broken. If one application server marks many file servers offline, that application server is probably the problem. This detection is advisory: it speeds things up, but correctness never depends on it.

### 6. Going global

**What GitHub's "Stretching Spokes" post says.** It describes replicas at widely separated sites for **GitHub Enterprise Server**. Those remote replicas are configured as **non-voting**, so pushes to the main hosts keep working even if a remote site is temporarily unreachable. Reads go to the **nearest replica that is in sync**. A write that has to reach distant replicas costs about **four round trips**. The post says nearby replicas also speed up clones and fetches for many github.com users. It does **not** say whether github.com's own remote replicas vote, or how many voters there are.

**My reasoning for a global design** (this part is mine, not GitHub's). A write needs a majority, and a majority across continents is slow, so keep the voting copies close together, in or near the region where most of a repository's writers are. Add extra copies in other regions that do not vote. They receive updates, and their failure never blocks a write, and they serve fast local reads. A distant copy may lag, so use the routing information, and the checksum idea, to know whether it is up to date, and send a user who just pushed to a copy that has their push. And say the trade-off aloud: distant copies give fast reads, but a write still pays the latency of its majority. You cannot have fast distant writes and strong consistency at once.

### 7. What GitHub's posts do not say

Say this honestly if you are asked. As I read their posts, they **do not describe a leader or a proxy** for writes (a third-party summary mentioned a proxy, and I could not find it in GitHub's own text). They do not give the number of voting replicas in a global setup, they do not say whether github.com's remote replicas vote, and they do not describe how fork networks share objects. If asked, explain how *you* would design it, and say that you do not know their exact internals.

### 8. Edge cases and what to watch for

**A repository is extremely popular.** Move it to less loaded servers, and let more copies serve reads. Writes still use the three voters.

**A repository is huge.** Place it by size as well as by count, and treat very large ones separately, since repair copies the whole thing.

**Forks.** You would want forks to share objects with their parent to save space, but I do not know GitHub's exact approach, and I would say so.

**Replication is not a backup.** A deletion or a corruption replicates too. You also need independent backups, kept separately.

**Detecting corruption.** Checksums and periodic verification, then repair from a good copy.

**Upgrading servers.** Quiesce, reboot a rack at a time, and let repair handle anything that falls behind.

**One copy comes back after a long outage.** It is stale for every repository that changed while it was away, so it must be repaired before it votes or serves reads. This is why "stale" is tracked per repository, and not as one flag per server.

**Why not one leader per repository.** A leader (as in Raft or Paxos) is a fine design too, but it needs a leader election and failover for every repository. A majority lock on every write is simpler, and has no leader to fail over.

Sources:

* [Building resilience in Spokes (GitHub Engineering)](https://github.blog/engineering/infrastructure/building-resilience-in-spokes/)
* [Introducing DGit (GitHub Blog)](https://github.blog/news-insights/the-library/introducing-dgit/)
* [Stretching Spokes (GitHub Engineering)](https://github.blog/engineering/stretching-spokes)
