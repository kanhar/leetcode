from webhooks_isolated import try_submit

outbox = [] # (url, event) pairs written by the push, in the same transaction as the push


def relay():
    for item in list(outbox):
        url, event = item

        if try_submit(url, event):
            outbox.remove(item)
        # otherwise it stays in the outbox, and the next pass tries again
