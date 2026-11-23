import threading
from collections import defaultdict

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
