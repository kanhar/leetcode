"""
Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order.

Example 1:

Input:
[
 [ 1, 2, 3 ],
 [ 4, 5, 6 ],
 [ 7, 8, 9 ]
]
Output: [1,2,3,6,9,8,7,4,5]

Ref: https://leetcode.com/problems/spiral-matrix/
"""

class Solution:
    def spiralOrder(self, m: List[List[int]]) -> List[int]:

        def solve(m, accum = [] ):
            if len(m)==0:
                return accum
            else:
                accum += list(m.pop(0))
                m = list(zip(*m))[::-1]
                return solve(m, accum)

        return solve(m)