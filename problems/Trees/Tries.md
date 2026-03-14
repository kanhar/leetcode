{: .no_toc}
# Prefix Tree (Trie)
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9db74ov1)

These are different from Ternary Search Tries.

- TOC
{:toc}

### [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/) 

> Find the longest common prefix in a set of words 
<details><summary markdown="span">Execute!</summary>

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

<details><summary markdown="span">Execute!</summary>

```python
import collections
from functools import lru_cache
from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        # 1. Build the Trie using a nested defaultdict
        def trie_node():
            return collections.defaultdict(trie_node)
        
        root = trie_node()
        for word in wordDict:
            curr = root
            for char in word:
                curr = curr[char]
            curr['#'] = True # Mark the end of a word

        # 2. Define the recursive solver with lru_cache
        @lru_cache(None)
        def solve(index: int) -> bool:
            # Base case: we've matched the entire string
            if index == len(s):
                return True
            
            curr = root
            # Traverse the Trie starting from the current character in 's'
            for i in range(index, len(s)):
                char = s[i]
                
                # If the character isn't in the current Trie node, 
                # no more words can be formed from this prefix.
                if char not in curr:
                    break
                
                curr = curr[char]
                
                # If we hit a word boundary ('#'), try to solve the rest of the string
                if '#' in curr:
                    if solve(i + 1):
                        return True
            
            # If no combination of words starting at this index works
            return False

        return solve(0)
```

</details>
<BR>

### [Word Search](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/)

> Given a 2D board and a list of words from the dictionary, find all words in the board. 
<details><summary markdown="span">Execute!</summary>

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

