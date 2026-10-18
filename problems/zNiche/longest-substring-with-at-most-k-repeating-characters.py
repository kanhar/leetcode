"""
Given a string, find the length of the longest substring without repeating characters.

Example 1:

Input: "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
Example 2:

Ref: https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/

"""
import collections

class Solution(object):
    def lengthOfLongestSubstringKDistinct(self, s,k):
        r,l,distinctChars,res = 0,0,0,0
        hsh = collections.defaultdict(int)

        while r<len(s):
            hsh[s[r]] += 1
            if hsh[s[r]]== 1:
                distinctChars +=1

            while l<=r and distinctChars > k:   # Change above to distinctChars > k for k distinct characters.
                hsh[s[l]] -=1
                if hsh[s[l]] == 0:
                    distinctChars -=1
                l +=1

            res = max(res, r-l+1)
            r+=1
        return res
