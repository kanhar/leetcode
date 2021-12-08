"""
Implement int sqrt(int x).

Compute and return the square root of x, where x is guaranteed to be a non-negative integer.

Since the return type is an integer, the decimal digits are truncated and only the integer part of the result is returned.

Ref: https://leetcode.com/problems/sqrtx/
"""

class Solution:
    def mySqrt(self, x: int) -> int:
        l = 0
        r = x
        while l <= r:
            mid     = (r+l)//2
            square  = mid*mid
            next_sq = (mid+1)*(mid+1)
            if square <= x < next_sq:
                return mid
            elif square > x:
                r = mid - 1
            else:
                l = mid + 1
        return square