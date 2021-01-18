'''
Implement int sqrt(int x).

Compute and return the square root of x, where x is guaranteed to be a non-negative integer.

Since the return type is an integer, the decimal digits are truncated and only the integer part of the result is returned.

Ref: https://leetcode.com/problems/sqrtx/
'''

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

'''
Implement pow(x, n), which calculates x raised to the power n (xn).

Example 1:
Input: 2.00000, 10
Output: 1024.00000
Example 2:

Input: 2.00000, -2
Output: 0.25000
Explanation: 2-2 = 1/22 = 1/4 = 0.25

Ref: https://leetcode.com/problems/powx-n/
'''

class Solution:
    def myPow(self, num, power):
        if not power:
            return 1
        elif power < 0:
            return 1 / self.myPow(num, -power)
        elif power % 2 == 1:
            return num * self.myPow(num, power-1)
        else:
            return self.myPow(num*num, power/2)