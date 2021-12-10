"""
Remove the minimum number of invalid parentheses in order to make the input string valid. Return all possible results.

Note: The input string may contain letters other than the parentheses ( and ).

Example 1:

Input: "()())()"
Output: ["()()()", "(())()"]
Example 2:

Input: "(a)())()"
Output: ["(a)()()", "(a())()"]
Example 3:

Input: ")("
Output: [""]

Ref: https://leetcode.com/problems/remove-invalid-parentheses/
"""
def isValidParenthesis(s):
    ctr = 0
    for c in s:
        if c == '(':
            ctr += 1
        elif c == ')':
            ctr -= 1
            if ctr < 0:
                return False
    return ctr == 0

class Solution:
    #TBD: What is complexity?
    #This is a BFS surprisingly: The idea is straightforward, with the input string s,
    # we generate all possible states by removing one ( or ),
    # check if they are valid, if found valid ones on the current level,
    # put them to the final result list and we are done, otherwise, add them to a queue and
    # carry on to the next level.
    def removeInvalidParentheses(self, s):
        l = len(s)
        res = set([s])
        while True:
            valid = list(filter(isValidParenthesis, res))
            if valid:
                return valid
            else:
                res = set([ s[:i] + s[i+1:] for s in res for i in range(l) if s[i] in '()' ])
                l-=1