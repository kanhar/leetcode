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

TLE - Because they want to remove word from trie after found.
"""
import collections
class Solution:
    def findWords(self, board, words):

        def _createTrie():
            return collections.defaultdict(_createTrie)

        def createTrie(words):
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
                dfs(r, c + 1, trie[b], visited, accum + [b])
                dfs(r, c - 1, trie[b], visited, accum + [b])
                dfs(r + 1, c, trie[b], visited, accum + [b])
                dfs(r - 1, c, trie[b], visited, accum + [b])
                visited[r][c] = False

        self.res = set()

        trie = createTrie(words)

        for i in range(len(board)):
            for j in range(len(board[i])):
                visited = [[False] * len(board[r]) for r in range(len(board))]
                dfs(i, j, trie, visited)

        return self.res

