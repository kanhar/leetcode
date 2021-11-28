'''
Convert
    [['E', 'C'],['E', 'P'],['C', 'R'], ['P', 'J']]
to:
    {
      "E": {
        "C": {
          "R": {}
        },
        "P": {
          "J": {}
        }
      }
    }


Ref: https://leetcode.com/discuss/interview-question/416929/googlephone-screenconstruct-tree-from-given-edges
'''

import collections
import json

data=[['E', 'C'],['E', 'P'],['C', 'R'], ['P', 'J']]

# The idea being, do a BFS to ensure that parent does not exist, before adding.
def solve(edges):
    trie = collections.defaultdict(dict)

    for a, b in edges:
        insert = False
        q = [trie]
        while q:
            curr = q.pop(0)
            if a in curr:
                curr[a][b] = {}
                insert = True
                break
            else:
                for c in curr.values():
                    q.append(c)

        if insert == False:
            trie[a][b] = {}
    return trie

print(json.dumps(solve(data), indent=2))

