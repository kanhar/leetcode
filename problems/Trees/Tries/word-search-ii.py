"""
Given a 2D board and a list of words from the dictionary, find all words in the board.

Each word must be constructed from letters of sequentially adjacent cell, where "adjacent" cells are those horizontally or vertically neighboring. The same letter cell may not be used more than once in a word.

Example:

Input:
board = [
  ['o','a','a','n'],
  ['e','t','a','e'],
  ['i','h','k','r'],
  ['i','f','l','v']
]
words = ["oath","pea","eat","rain"]

Output: ["eat","oath"]

Ref: https://leetcode.com/problems/word-search-ii/
"""
from collections import defaultdict
class Solution:
    def findWords(self, board, words):

        def createTrie(words):
            def _createTrie():
                return collections.defaultdict(_createTrie)

            t = _createTrie()
            for word in words:
                root = t
                for w in word:
                    root = root[w]
                root['#']
            return t

        def dfs(r, c, trie, visited, accum=[]):
            if '#' in trie:
                self.res.add(''.join(accum))

            if r in range(len(board)) and c in range(len(board[r])) and board[r][c] in trie and not visited[r][c]:
                visited[r][c] = True

                b = board[r][c]
                trie = trie[b]
                dfs(r, c + 1, trie, visited, accum + [b])
                dfs(r, c - 1, trie, visited, accum + [b])
                dfs(r + 1, c, trie, visited, accum + [b])
                dfs(r - 1, c, trie, visited, accum + [b])

                visited[r][c] = False

        self.res = set()
        visited = [[False] * len(board[r]) for r in range(len(board))]
        rootTrie = createTrie(words)

        for i in range(len(board)):
            for j in range(len(board[i])):
                dfs(i, j, rootTrie, visited)

        return self.res



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