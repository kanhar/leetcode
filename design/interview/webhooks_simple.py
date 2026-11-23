from collections import defaultdict

subscribers = defaultdict(list) # repo -> the URLs that asked to hear about it
post = None # post(url, event) sends the request and returns the HTTP status


def on_push(repo, event):
    for url in subscribers[repo]:
        post(url, event)
