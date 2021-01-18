'''
Given two integers dividend and divisor, divide two integers without using multiplication, division and mod operator.

Return the quotient after dividing dividend by divisor.

The integer division should truncate toward zero, which means losing its fractional part. For example, truncate(8.345) = 8 and truncate(-2.7335) = -2.

Example 1:

Input: dividend = 10, divisor = 3
Output: 3
Explanation: 10/3 = truncate(3.33333..) = 3.

Note:
    This algorithm is known as exponential search and is commonly used for searching sorted spaces of unknown size for the first value that past a particular condition.
    It it a lot like binary search, having the same time complexity of O(\log \, n)O(logn).
'''
class Solution:
    def divide(self, dividend, divisor):
        sign = (dividend < 0) == (divisor < 0)
        res = 0
        dividend, divisor = abs(dividend), abs(divisor)
        while dividend >= divisor:
            tmp = divisor
            val = 1
            while dividend >= tmp:
                dividend -= tmp
                res += val

                tmp = tmp << 1
                val = val << 1

        return min(2147483647, res) if sign == 1 else max(-2147483648, 0-res)

