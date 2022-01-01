"""
Given an integer matrix, find the length of the longest increasing path.

From each cell, you can either move to four directions: left, right, up or down.
You may NOT move diagonally or move outside of the boundary (i.e. wrap-around is not allowed).

Example 1:

Input: nums =
[
  [9,9,4],
  [6,6,8],
  [2,1,1]
]
Output: 4
Explanation: The longest increasing path is [1, 2, 6, 9].

Ref: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
"""

import collections

class Solution:
    def longestIncreasingPath(self, m):
        edges = collections.defaultdict(list)
        indeg = collections.defaultdict(int)

        for i in range(len(m)):
            for j in range(len(m[0])):
                neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                for x, y in neighbors:
                    if x in range(len(m)) and y in range(len(m[i])) and m[x][y] > m[i][j]:
                        edges[(i, j)].append((x, y))
                        indeg[(x, y)] += 1

        # Step 2: Topological sorting with Kahn's algorithm. Notice that we move BFS Level by Level.
        q = [(i, j) for i in range(len(m)) for j in range(len(m[0])) if (i, j) not in indeg]
        max_path_len = 0
        res = []
        while q:
            max_path_len += 1
            q_tmp = []
            while q:
                node = q.pop(0)
                for neighbor in edges[node]:
                    indeg[neighbor] -= 1
                    if indeg[neighbor] == 0:
                        q_tmp.append(neighbor)

            q = q_tmp

        return max_path_len


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        def solve(r, c, accum):
            if r not in range(len(matrix)) or c not in range(len(matrix[0])):
                return
            else:
                self.max = max(self.max, len(accum))
                if len(accum) != 0 and matrix[r][c] <= accum[-1]:
                    return

                tmp = matrix[r][c]
                matrix[r][c] = float('-inf')
                solve(r + 1, c, accum + [tmp])
                solve(r - 1, c, accum + [tmp])
                solve(r, c + 1, accum + [tmp])
                solve(r, c - 1, accum + [tmp])
                matrix[r][c] = tmp

        self.max = 1
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                solve(i, j, [])

        return self.max


