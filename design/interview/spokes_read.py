from spokes_vote import copies, down, stale


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
