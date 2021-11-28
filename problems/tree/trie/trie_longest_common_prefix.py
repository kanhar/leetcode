"""
Write a function to find the longest common prefix string amongst an sort of strings.
If there is no common prefix, return an empty string "".

Input: ["flower","flow","flight"]
Output: "fl"

Ref: https://leetcode.com/problems/longest-common-prefix/
"""
def createTrie(words):
    def _createTrie(): return collections.defaultdict(_createTrie)

    t = _createTrie()
    for word in words:
        root = t
        for w in word:
            root = root[w]
        root['#']
    return t

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        def solve(root, accum = ""):
            curr = root
            if len(curr.values()) == 1 and '#' not in curr:
                key = next(iter(curr))
                return solve(curr[key], accum + key)
            else:
                return accum
        return solve(createTrie(strs))
