"""
Given a non-empty string s and a dictionary wordDict containing a list of non-empty words, determine if s can be segmented into a space-separated sequence of one or more dictionary words.

Note:

The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words.
Example 1:

Input: s = "leetcode", wordDict = ["leet", "code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".

Ref: https://leetcode.com/problems/word-break/
"""
import collections

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        def createTrie(wordDict):
            def _createTrie():
                return collections.defaultdict(_createTrie)

            t = _createTrie()
            for word in wordDict:
                curr = t
                for w in word:
                    curr = curr[w]
                curr['#']
            return t

        def solve(curr, s):
            if len(s) == 0:
                return '#' in curr
            else:
                for i in range(0, len(s)):
                    if '#' in curr:
                        return solve(curr[s[i]], s[i + 1:]) or solve(t[s[i]], s[i + 1:])
                    else:
                        if s[i] in curr:
                            return solve(curr[s[i]], s[i + 1:])
                        else:
                            return False

        t = createTrie(wordDict)
        return solve(t, s)