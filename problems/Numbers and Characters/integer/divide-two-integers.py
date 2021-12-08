"""
Given two integers dividend and divisor, divide two integers without using multiplication,
division and mod operator.

Return the quotient after dividing dividend by divisor.

The integer division should truncate toward zero, which means losing its fractional part.
For example, truncate(8.345) = 8 and truncate(-2.7335) = -2.

Example 1:

Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = truncate(3.33333..) = 3.

Note:
    This algorithm is known as exponential search and is commonly used for searching sorted spaces
    of unknown size for the first value that past a particular condition.
    It it a lot like binary search, having the same time complexity of O(log(n))

Ref: https://leetcode.com/problems/divide-two-integers/
"""

class Solution:
    def divide(self, a: int, b: int) -> int:

        # Answer of -2147483648/-1 should be 2147483648
        # However 2147483648 is too big, 2^31 == 2147483648 (one more than possible 2^31-1)
        # Therefore abs(2^31) == 2147483648-1 = 2147483647
        # This is an edge case scenario. The lowest value a 32 bit can contain is -2147483648
        if a == -2147483648 and b == -1:
            return 2147483647

        sign = (a < 0) == (b < 0)
        a, b = abs(a), abs(b)
        res = 0
        while a >= b:
            tmp = b
            val = 1
            while a >= b:
                a -= b
                res += val

                b = b << 1
                val = val << 1
            b = tmp

        return res if sign == 1 else 0 - res
