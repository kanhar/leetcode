"""
Given a 2D board and a word, find if the word exists in the grid.

The word can be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally or vertically neighboring. The same letter cell may not be used more than once.

Example:

board =
[
  ['A','B','C','E'],
  ['S','F','C','S'],
  ['A','D','E','E']
]

Given word = "ABCCED", return true.
Given word = "SEE", return true.
Given word = "ABCB", return false.

#Uses backtracking. To pass time limit.

Ref: https://leetcode.com/problems/word-search/
"""


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:

        def dfs(r, c, curr):
            if curr == '':
                return True

            if r in range(len(board)) and c in range(len(board[r])) and board[r][c] != '#':
                if board[r][c] == curr[0]:
                    board[r][c] = '#'
                    res = dfs(r, c + 1, curr[1:]) or dfs(r, c - 1, curr[1:]) \
                          or dfs(r + 1, c, curr[1:]) or dfs(r - 1, c, curr[1:])
                    board[r][c] = curr[0]
                    return res
                else:
                    return False

        for i in range(len(board)):
            for j in range(len(board[i])):
                if dfs(i, j, word):
                    return True

        return False
