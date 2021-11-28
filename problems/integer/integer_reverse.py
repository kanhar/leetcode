"""
Given a 32-bit signed integer, reverse digits of an integer.

Example 1:

Input: 123
Output: 321
"""
class Solution:
    def reverse(self, x: int) -> int:

        sign = -1 if x < 0 else 1

        num = abs(x)
        res = 0
        while num != 0:
            d = num %10
            res = res * 10 + d
            num = int(num /10 )

        if res > 2**31 - 1 or res < -2**31: return 0 #Cannot do this check earlier. Think why.

        return sign * res



