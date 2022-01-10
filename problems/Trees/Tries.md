{: .no_toc}
# K-Ary Search Tries
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9db74ov1)

These are different from Ternary Search Tries.

- TOC
{:toc}

### [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) 

> Find the longest common prefix in a set of words 
<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        def createTrie(words):
            def _createTrie(): return collections.defaultdict(_createTrie)

            t = _createTrie()
            for word in words:
                curr = t
                for w in word:
                    curr = curr[w]
                curr['#']
            return t
        
        def solve(root, accum = ""):
            curr = root
            if len(curr.values()) == 1 and '#' not in curr:
                for k,v in curr.items():
                    return solve(curr[k], accum + k)
            else:
                return accum
            
        t = createTrie(strs)
        return solve(t)
```

</details>
<BR>

### [Word Break](https://leetcode.com/problems/word-break/) 

> Given a non-empty string s and a dictionary wordDict containing a list of non-empty words, determine if s can be segmented into a space-separated sequence of one or more dictionary words.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        def createTrie(wordDict):
            def _createTrie():
                return collections.defaultdict(_createTrie)

            t = _createTrie()
            for word in wordDict:
                curr = t
                for w in word:
                    curr = curr[w]
                curr['#']
            return t

        def solve(curr, s):
            if len(s) == 0:
                return '#' in curr
            else:
                for i in range(0, len(s)):
                    if '#' in curr:
                        return solve(curr[s[i]], s[i + 1:]) or solve(t[s[i]], s[i + 1:])
                    else:
                        if s[i] in curr:
                            return solve(curr[s[i]], s[i + 1:])
                        else:
                            return False

        t = createTrie(wordDict)
        return solve(t, s)
```

</details>
<BR>

### [Word Search](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/)

> Given a 2D board and a list of words from the dictionary, find all words in the board. 
<details><summary markdown="span">Let's see some code!</summary>

```python
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
```

</details>
<BR>

