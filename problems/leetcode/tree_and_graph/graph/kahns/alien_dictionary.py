'''
There is a new alien language that uses the English alphabet. However, the order among the letters is unknown.

You are given a list of strings words from the alien language's dictionary, where the strings in words
are sorted lexicographically by the rules of this new language.

Return a string of the unique letters in the new alien language sorted in lexicographically increasing
order by the new language's rules. If there is no solution, return "". If there are multiple solutions,
return any of them.

A string s is lexicographically smaller than a string t if at the first letter where they differ,
the letter in s comes before the letter in t in the alien language.
If the first min(s.length, t.length) letters are the same,
then s is smaller if and only if s.length < t.length.

Example 1:

Input: words = ["wrt","wrf","er","ett","rftt"]
Output: "wertf"

Ref: https://en.wikipedia.org/wiki/Topological_sorting
Ref: https://leetcode.com/problems/alien-dictionary/
'''

"""
    Loop like so:
    zip:
    -> "wrt",  "wrf",  "er",   "ett",  "rftt"
    -> "wrf",  "er",   "ett",  "rftt"
    results in:
    --> wrt wrf
    --> wrf er
    --> er ett
    --> ett rftt

    Then zip (wrf er):
        w --> e (w comes before e)
        <Hard Break after first find, since no further inference can be made>
"""

import collections
import typing

class Solution:
    def alienOrder(self, words: typing.List[str]) -> str:
        adj = collections.defaultdict(set)
        indeg = {x: 0 for word in words for x in word}  # Or: { x:0 for x in ''.join(words)}

        for w1, w2 in zip(words, words[1:]):
            for a, b in zip(w1, w2):
                orderingFound = False
                if a != b:
                    if b not in adj[a]:
                        adj[a].add(b)
                        indeg[b] += 1
                    orderingFound = True
                    break

            if orderingFound == False and len(w1) > len(w2):  # Invalid Dict order.
                return ""

        q = [x for x in indeg if indeg[x] == 0]
        res = []
        while q:
            curr = q.pop()
            res.append(curr)
            for d in adj[curr]:
                indeg[d] -= 1
                if indeg[d] == 0:
                    q.append(d)

        if len(res) < len(indeg):
            return ""  # indicates cycle
        else:
            return ''.join(res)