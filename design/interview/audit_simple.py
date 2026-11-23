repos  = {"r1", "r2"} # the product's data
events = []           # the audit log


def delete_repo(org, actor, repo):
    repos.discard(repo) # the action

    events.append({"org": org, "actor": actor, "action": "repo.delete", "target": repo})
