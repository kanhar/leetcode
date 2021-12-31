"""
Implement a basic calculator to evaluate a simple expression string.

The expression string may contain open ( and closing parentheses ),
the plus + or minus sign -,
non-negative integers and empty spaces .

Input: "(1+(4+5+2)-3)+(6+8)"
Output: 23

Ref: https://leetcode.com/problems/basic-calculator/
"""
class Solution:
    def calculate(self, s: str) -> int:
        res = num = 0
        sign = 1

        s = s + "+"
        stk = [sign]
        for a in s:
            if a.isdigit():
                num = num * 10 + (ord(a)-48)        # Create Number
            elif a in ['+', '-']:
                res += num * sign * stk[-1]         # +- Number ( & adjust for if in bracket sign)
                sign = 1 if a == '+' else -1        # Number complete
                num = 0
            elif a == '(':                          # Add previous sign to Stack. Reset sign
                stk.append(sign * stk[-1])
                sign = 1
            elif a == ')':                          # Add number and sign to result. Reset number.
                res += num * sign * stk[-1]
                num = 0
                stk.pop()
        return res

