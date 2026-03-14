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

### [Implement Search (Trie)](https://leetcode.com/problems/implement-trie-prefix-tree/) <BR>

While a Ternary Search Tree (TST) is more space-efficient for large character sets, a standard Trie is much faster O(L) where `L` is the length of the word) because it uses a hash map or an array to jump directly to the next character node.In a standard Trie, each node represents a character, and its children are stored in a dictionary (mapping characters to nodes).

<details><summary markdown="span">Execute!</summary>
    
```python
class TrieNode:
    def __init__(self):
        # A dictionary where keys are characters and values are TrieNodes
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            # If the character isn't there, create a new branch
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        
        # Mark the end of the word
        curr.is_end_of_word = True

    def _find_node(self, word: str):
        """Helper to navigate to the node representing the end of the string."""
        curr = self.root
        for char in word:
            if char not in curr.children:
                return None
            curr = curr.children[char]
        return curr

    def search(self, word: str) -> bool:
        node = self._find_node(word)
        # It's a match only if the node exists AND it was marked as a word end
        return node is not None and node.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        # For a prefix, we only care if the path exists
        return self._find_node(prefix) is not None
```

</details>
<BR>

### [Implement Search (TST)](https://leetcode.com/problems/implement-trie-prefix-tree/) <BR>

In a regular Trie, every node typically contains a full array of pointers for every possible character in the alphabet (e.g., an array of 26 for English, or 256 for ASCII). If you are storing a limited number of words, most of those pointers are null, wasting significant memory.
TST Advantage: Each node only ever has three pointers (left, mid, right), regardless of how large the alphabet is.
Best For: Large character sets like Unicode, where a regular Trie node would require thousands of potential child pointers.

Because TST nodes are smaller (only three pointers), they are more likely to stay in the CPU's L1/L2 cache.
In a regular Trie, a node with a 256-slot array might exceed the size of a cache line, forcing the CPU to fetch from slower RAM more frequently.

Near-Neighbor Search: TSTs are excellent for spell-checking or "fuzzy matching" (finding words within a certain Hamming distance) because you can prune the left/right branches of the search tree more effectively than you can in a standard Trie's flat dictionary.

Ref: [Masters SuffixTriePresentation](https://kanhar.github.io/pdf/SuffixTriePresentation.pdf)

<details><summary markdown="span">Execute!</summary>
```python
class TSTNode(object):
    def __init__(self, ch, val=0):
        self.key = ch
        self.val = val
        self.left = None
        self.mid = None
        self.right = None

class Trie:
    def __init__(self):
        self.root = None
        
    def insert(self, key: str) -> None:
        if not key:
            return

        def create(node, word, val):
            ch = word[0]
            if node is None:
                node = TSTNode(ch)

            if ch < node.key:
                # Still looking for the SAME ch, so don't slice word
                node.left = create(node.left, word, val)
            elif ch > node.key:
                # Still looking for the SAME ch
                node.right = create(node.right, word, val)
            else:
                # Character matches! 
                if len(word) > 1:
                    # Move to next char and go down the middle
                    node.mid = create(node.mid, word[1:], val)
                else:
                    # End of word
                    node.val = val
            return node
                    
        self.root = create(self.root, key, 1)

    def _get_node(self, word: str):
        """Helper to find the node corresponding to the last char of word."""
        curr = self.root
        i = 0
        while curr and i < len(word):
            ch = word[i]
            if ch < curr.key:
                curr = curr.left
            elif ch > curr.key:
                curr = curr.right
            else:
                if i == len(word) - 1:
                    return curr
                curr = curr.mid
                i += 1
        return None

    def search(self, word: str) -> bool:
        node = self._get_node(word)
        return node is not None and node.val != 0

    def startsWith(self, prefix: str) -> bool:
        return self._get_node(prefix) is not None
```

</details>
<BR>

