"""
Given a string S and a string T, find the minimum window in S which will contain all the characters in T in complexity O(n).

Example:

Input: S = "ADOBECODEBANC", T = "ABC"
Output: "BANC"

Ref: https://leetcode.com/problems/minimum-window-substring/
"""
import collections
class Solution:
    def minWindow(self, s: str, t: str) -> str:
        need = collections.Counter(t)
        l = r = tmp_i = tmp_j = 0
        missing = len(t)

        for r in range(0,len(s)):
            if s[r] in need:
                if need[s[r]] > 0:
                    missing -=1
                need[s[r]] -=1

            while l <= r and missing==0:
                if tmp_j ==0 or r-l+1 < tmp_j-tmp_i:
                    tmp_i,tmp_j= l,r+1

                if s[l] in need:
                    need[s[l]]+=1
                    if need[s[l]]>0:
                        missing +=1

                l+=1

        return s[tmp_i:tmp_j]


s = Solution()
print(s.minWindow("ADOBECODEBANC", "ABC")=="BANC")



