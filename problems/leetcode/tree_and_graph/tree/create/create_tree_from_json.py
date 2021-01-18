import collections
import json

def createTree(edges):
    t = collections.defaultdict(dict)

    for parent, child in edges:
        t[parent][child] = t[child]
    parents, children = zip(*edges)
    roots = set(parents).difference(children)

    return {x: t[x] for x in roots}

data=[['E1', 'C1'],['E1', 'P1'],['C1', 'R1'], ['K1', 'J1']]
print(json.dumps(createTree(data), indent=1))