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
        def dfs(r,c, arr):
            if len(arr) == 0:
                return True

            if r in range(len(board)) and c in range(len(board[r])) and board[r][c] == arr[0]:
                board[r][c] = ''
                if dfs(r+1, c, arr[1:]):
                    return True
                if dfs(r-1, c, arr[1:]):
                    return True
                if dfs(r, c+1, arr[1:]):
                    return True
                if dfs(r, c-1, arr[1:]):
                    return True
                board[r][c] = arr[0]

            return False

        if word == '':
            return False
        else:
            count = 0
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if dfs(i,j, word):
                        return True

            return False