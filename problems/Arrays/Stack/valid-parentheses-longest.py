"""
Given a string containing just the characters '(' and ')', find the length of the
longest valid (well-formed) parentheses substring.

Example 1:

Input: "(()"
Output: 2
Explanation: The longest valid parentheses substring is "()"

Ref: https://leetcode.com/problems/longest-valid-parentheses/
"""
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        def isValid(arr):
            stk = []
            for a in arr:
                if a == '(':
                    stk.append('(')
                elif a == ')':
                    if len(stk) == 0 or stk.pop() != '(':
                        return 0

            return len(arr) if len(stk) == 0 else 0

        if s == '':
            return 0
        elif isValid(s):
            return len(s)
        else:
            return max(self.longestValidParentheses(s[1:]), self.longestValidParentheses(s[:-1]))


