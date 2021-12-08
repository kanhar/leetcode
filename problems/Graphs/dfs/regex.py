"""
Given an input string (s) and a pattern (p), implement regular expression matching with support for '.' and '*'.

'.' Matches any single character.
'*' Matches zero or more of the preceding element.
The matching should cover the entire input string (not partial).

Note:

s could be empty and contains only lowercase letters a-z.
p could be empty and contains only lowercase letters a-z, and characters like . or *.
Example 1:

Input:
s = "aa"
p = "a"
Output: false
Ref: https://leetcode.com/problems/regular-expression-matching/
"""
import functools

class Solution(object):
    @functools.lru_cache(maxsize=1024)
    def isMatch(self, t, p):
        if not p and not t:
            return True
        elif t and not p:
            return False
        elif p and not t and p[-1] != '*':
            return False
        else:
            firstCharMatches  = len(t)> 0 and p[0] in [t[0],'.']

            if len(p) >= 2 and p[1]=='*':
                zeroOccurrences = self.isMatch(t,p[2:])                     #move pattern up
                oneOrMore  = (firstCharMatches and self.isMatch(t[1:],p) )  #move string up. Must check firstCharMatches before self.isMatch. Can you guess why?
                return zeroOccurrences or oneOrMore
            else:
                return (firstCharMatches and self.isMatch(t[1:],p[1:]))
