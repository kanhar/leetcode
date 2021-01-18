'''
There is a new alien language which uses the latin alphabet. However, the order among letters are unknown to you.
You receive a list of non-empty words from the dictionary, where words are sorted lexicographically by the rules of this new language.
Derive the order of letters in this language.

Example 1:

Input:
[
  "wrt",
  "wrf",
  "er",
  "ett",
  "rftt"
]

Output: "wertf"
Example 2:

Input:
[
  "z",
  "x"
]

Output: "zx"
Example 3:

Input:
[
  "z",
  "x",
  "z"
]

Output: ""

Explanation: The order is invalid, so return "".

Ref: https://en.wikipedia.org/wiki/Topological_sorting
'''
class Solution:
    def alienOrder(self, words: List[str]) -> str:
        adj   = collections.defaultdict(set)
        indeg = { c:0 for word in words for c in word }

        for w1,w2 in zip(words, words[1:]):
            for a,b in zip(w1,w2):
                if a != b:
                    if b not in adj[a]:
                        adj[a].add(b)
                        indeg[b]+=1
                    break
            else:
                if len(w1) > len(w2):               # Invalid Dict order.
                    return ""

        q = [ x for x in indeg if indeg[x] == 0]
        res = ''
        while q:
            curr = q.pop()
            res += curr
            for d in adj[curr]:                     # Remove curr from graph.
                indeg[d]-=1
                if indeg[d]==0:
                    q.append(d)

        return "" if len(res) < len(indeg) else res # Indicates cycle

'''
In an alien language, surprisingly they also use english lowercase letters, but possibly in a different order. The order of the alphabet is some permutation of lowercase letters.

Given a sequence of words written in the alien language, and the order of the alphabet, return true if and only if the given words are sorted lexicographicaly in this alien language.

Example 1:

Input: words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"
Output: true
Explanation: As 'h' comes before 'l' in this language, then the sequence is sorted.
'''

class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        adj   = collections.defaultdict(set)
        for i in range(len(order)):
            adj[order[i]] = set(list(order[i+1:]))

        indeg = { c:0 for word in words for c in word }
        for w1,w2 in zip(words, words[1:]):
            for a,b in zip(w1,w2):
                if a != b:
                    if b not in adj[a]:
                        return False
                    break
            else:
                if len(w1) > len(w2):
                    return False
        return True

