'''
Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

For example, given n = 3, a solution set is:

[
  "((()))",
  "(()())",
  "(())()",
  "()(())",
  "()()()"
]

Ref: https://leetcode.com/problems/generate-parentheses/
'''

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def solve(n):
            one='()'
            if n==1:
                return {one}
            else:
                return {res[:i]+one+res[i:] for res in solve(n-1) for i in range(len(res))}
                # For n = 2:
                #   Res = "()"
                #   For i in range(0,2)
                #       Ans = Res[:0] + () + Res[0:]
                #       Ans = None    + () + ()
                #       Ans = Res[:1] + () + Res[1:]
                #       Ans =    (    + () +    )
        return list(solve(n))

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def solve(n):
            one='()'
            if n==1:
                return {one}
            else:
                tmp = []
                for r in solve(n-1):
                    for i in range(len(r)):
                        tmp.append(  r[:i] + one + r[i:]  )
                return set(tmp)
        return list(solve(n))