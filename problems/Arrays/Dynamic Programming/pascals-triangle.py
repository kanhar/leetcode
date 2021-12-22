"""
Given an integer numRows, return the first numRows of Pascal's triangle.

In Pascal's triangle, each number is the sum of the two numbers directly above it as shown:
1
11
121
1331

Ref: https://leetcode.com/problems/pascals-triangle/
"""

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        dp = [[1]]
        for i in range(1, numRows):
            tmp = [1] * (i + 1)
            for j in range(1, i):  # First and last should not be overwritten in range 0..i+1 (== 1 to i)
                tmp[j] = dp[i - 1][j - 1] + dp[i - 1][j]
            dp = dp + [tmp]
        return dp
