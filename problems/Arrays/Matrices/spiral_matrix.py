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
        def add(t1):
            nonlocal r, c
            r, c = r + t1[0], c + t1[1]

        def sub(t1):
            nonlocal r, c
            r, c = r - t1[0], c - t1[1]

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        res = []
        count = 0
        total = len(m) * len(m[0])

        curr = 0
        r, c = 0, 0
        while count < total:
            res.append(m[r][c])
            m[r][c] = 'z'
            count += 1
            add(directions[curr])

            if r not in range(len(m)) or c not in range(len(m[0])) or m[r][c] == 'z':
                sub(directions[curr])
                curr = (curr + 1) % 4
                add(directions[curr])

        return res

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