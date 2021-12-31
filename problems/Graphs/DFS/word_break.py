"""

Input: s = "leetcode", wordDict = ["leet","code"]
Output: true

Explanation: Return true because "leetcode" can be segmented as "leet code".

Ref: https://leetcode.com/problems/word-break/
"""
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        def solve(s, d, memo={}):
            if len(s) == 0:
                return True

            if s in memo:
                return memo[s]

            for i in range(1, len(s) + 1):
                if s[:i] in d:
                    if solve(s[i:], d):
                        memo[s[i:]] = True
                        return memo[s[i:]]

            memo[s] = False
            return memo[s]

        return solve(s, wordDict)