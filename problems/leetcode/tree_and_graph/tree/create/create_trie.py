'''
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
'''
from collections import defaultdict
class Solution:
    def findWords(self, board, words):
        def dfs(r,c,trie,accum=''):
            if '#' in trie:
                self.res.add(accum)
            if r in range(len(board)) and c in range(len(board[r])) and board[r][c] in trie and not self.visited[r][c]:
                self.visited[r][c]=True

                b = board[r][c]

                dfs(r+1,c,  trie[b],accum+b)
                dfs(r-1,c,  trie[b],accum+b)
                dfs(r,  c+1,trie[b],accum+b)
                dfs(r,  c-1,trie[b],accum+b)

                self.visited[r][c]=False

        trie = self.buildTrie(words)
        self.res=set()
        self.visited=[[False]*len(board[0]) for _ in range(len(board))]

        for i in range(len(board)):
            for j in range(len(board[0])):
                dfs(i,j,trie)

        return list(self.res)

    def buildTrie(self, words):
        def _trie():
            return defaultdict(_trie)
        trie = _trie()
        for w in words:
            root = trie
            for c in w:
                root=root[c]
            root['#']='#'
        return trie



