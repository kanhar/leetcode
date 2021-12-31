"""

Ref: https://leetcode.com/problems/sparse-matrix-multiplication/
"""

class Solution:
    def multiply(self, A, B):
        def dotProduct(x, y):
            return sum(a * b for a, b in zip(x, y))

        # To multiply an m×n matrix by an n×p matrix, the n's must be the same,
        # and the result is an m×p matrix.

        # Inner expression is column, outside rows
        res = [[0 for x in range(len(B[0]))] for y in range(len(A))]

        for i in range(len(A)):
            for j in range(len(B[0])):
                res[i][j] = dotProduct(A[i], [x[j] for x in B])

        return res