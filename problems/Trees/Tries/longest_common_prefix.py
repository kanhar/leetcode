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
        curr = t
        for w in word:
            curr = curr[w]
        curr['#']
    return t

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        def solve(root, accum = ""):
            curr = root
            if len(curr.values()) == 1 and '#' not in curr:
                for k,v in curr.items():
                    return solve(curr[k], accum + k)
            else:
                return accum
        t = createTrie(strs)
        return solve(t)
