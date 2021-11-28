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

        # Step 1: build a directed acyclic graph
        graph = collections.defaultdict(list)
        indegree = collections.defaultdict(int)
        for i in range(len(m)):
            for j in range(len(m[0])):
                neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
                for x, y in neighbors:
                    if x in range(len(m)) and y in range(len(m[i])) and m[x][y] > m[i][j] :
                        graph[(i,j)].append((x,y))
                        indegree[(x,y)]+=1

        # Step 2: Topological sorting with Kahn's algorithm. Notice that we move BFS Level by Level. Interesting.
        queue = collections.deque([(i, j) for i in range(len(m)) for j in range(len(m[0])) if (i,j) not in indegree])
        max_path_len = 0
        while queue:
            max_path_len += 1
            for _ in range(len(queue)):
                node = queue.pop(0)
                for neighbor in graph[node]:
                    indegree[neighbor] -= 1
                    if not indegree[neighbor]:
                        queue.append(neighbor)
        return max_path_len