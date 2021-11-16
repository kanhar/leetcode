'''
Given a string, find the length of the longest substring without repeating characters.

Example 1:

Input: "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.
Example 2:

Ref: https://leetcode.com/problems/longest-substring-without-repeating-characters/
Ref: https://leetcode.com/problems/longest-substring-with-at-most-k-distinct-characters/

'''
import collections


# Length of Longest Substring with all distinct characters.  Ex: "eceba" -> "ceba" (i.e. no repeating characters)
# Length of Longest Substring with K distinct characters.    Ex: "eceba", k=2 -> "ece"
class Solution(object):
    def lengthOfLongestSubstring(self, s: str) -> int:
        r, l, distinctChars, res = 0, 0, 0, 0
        hsh = collections.defaultdict(int)

        for r in range(0, len(s)):
            hsh[s[r]] += 1
            if hsh[s[r]] == 1:
                distinctChars += 1

            # Essentially this is code to re-balance hash. Pigeon Hole principle distinct Char less than total char,
            # means duplicate
            while l <= r and r - l + 1 > distinctChars:  # Change above to distinctChars > k for k distinct characters.
                hsh[s[l]] -= 1
                if hsh[s[l]] == 0:
                    distinctChars -= 1
                l += 1

            res = max(res, r - l + 1)

        return res


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        l, r, distinctChars, res = 0, 0, 0, 0
        hsh = collections.defaultdict(int)

        for r in range(0, len(s)):
            if s[r] in hsh:
                hsh[s[r]] += 1
                while hsh[s[r]] > 1:  # Note: here we are checking on hsh[s[r]] vs Pigeon Hole Way where it is hsh[s[l]]
                    hsh[s[l]] -= 1
                    l += 1
            else:
                hsh[s[r]] = 1

            res = max(res, r - l + 1)

        return res
