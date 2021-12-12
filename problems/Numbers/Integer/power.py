"""
Implement pow(x, n), which calculates x raised to the power n (xn).

Example 1:
Input: 2.00000, 10
Output: 1024.00000
Example 2:

Input: 2.00000, -2
Output: 0.25000
Explanation: 2-2 = 1/22 = 1/4 = 0.25

Ref: https://leetcode.com/problems/powx-n/
"""

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