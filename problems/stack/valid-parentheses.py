"""
Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

An input string is valid if:

Open brackets must be closed by the same type of brackets.
Open brackets must be closed in the correct order.
Note that an empty string is also considered valid.

Example 1:

Input: "()"
Output: true
Example 2:

Input: "()[]{}"
Output: true

Ref: https://leetcode.com/problems/valid-parentheses/
"""
class Solution(object):
    def isValid(self, s):
        d = dict(zip("([{",")]}" ) )
        stk = []
        for b in s:
            if b in d.keys():
                stk.append(b)
            elif b in d.values():
                if stk == [] or b != d[stk.pop()]:
                    return False
        return len(stk)==0