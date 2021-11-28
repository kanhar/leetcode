"""
Given an input string (s) and a pattern (p), implement wildcard pattern matching with support for '?' and '*'.

'?' Matches any single character.
'*' Matches any sequence of characters (including the empty sequence).
The matching should cover the entire input string (not partial).

Note:

s could be empty and contains only lowercase letters a-z.
p could be empty and contains only lowercase letters a-z, and characters like ? or *.
"""

import functools
class Solution:
    def isMatch(self, s, p):
        def remove_dupes(p):
            while p.find("**") != -1:
                p = p.replace("**", "*")
            return p

        @functools.lru_cache(maxsize=1024)
        def solve( s, p):
            if p == s or p == '*':
                return True
            elif not p or not s:
                return False
            elif p[0] in ['?', s[0] ]:
                return solve(s[1:], p[1:])
            elif p[0] == '*':
                return solve(s[1:], p) or solve(s, p[1:])
            else:
                return False

        return solve(s, remove_dupes(p) )