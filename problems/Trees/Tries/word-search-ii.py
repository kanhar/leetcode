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

        def dfs(r, c, trie, accum):
            if '#' in trie:
                self.res.add(''.join(accum))

            if r in range(len(board)) and c in range(len(board[0])) and board[r][c] in trie:
                curr = board[r][c]
                board[r][c] = ''
                dfs(r, c + 1, trie[curr], accum + [curr])
                dfs(r, c - 1, trie[curr], accum + [curr])
                dfs(r + 1, c, trie[curr], accum + [curr])
                dfs(r - 1, c, trie[curr], accum + [curr])
                board[r][c] = curr

        self.res = set()

        for i in range(len(board)):
            for j in range(len(board[i])):
                # Leetcode optimization: Remove word from Trie, if already found. i.e. Rebuild Trie
                rootTrie = createTrie(set(words) - self.res)
                dfs(i, j, rootTrie, [])

        return self.res

