heads = {} # repo -> the commit its main branch points at


def write(repo, old, new):
    if heads.get(repo) != old:
        return False # somebody else moved it first

    heads[repo] = new
    return True


def read(repo):
    return heads.get(repo)
