"""
You are given an n x n 2D matrix representing an image.

Ref: https://leetcode.com/problems/diagonal-traverse/
"""

class Solution:
    def findDiagonalOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix and matrix[0])

        res = []
        count = 0

        # get top row + right col ( rightmost edge is counted twice, hence --> for i in range(n-1))
        indices = [(0, i) for i in range(n - 1)] + [(j, n - 1) for j in range(m)]
        while indices:
            (r, c) = indices.pop(0)

            tmp = []
            while r < m and c >= 0:
                tmp.append(matrix[r][c])
                r += 1
                c -= 1

            if count % 2 == 0:
                tmp.reverse()

            count += 1
            res += tmp

        return res