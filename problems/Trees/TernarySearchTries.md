{: .no_toc}
# Ternary Search Tries
[Ternary Search Tries](https://en.wikipedia.org/wiki/Ternary_search_tree) or Prefix Tries are cool. My impl. below generally works, 
but has a few bugs, (4/15 test cases fail) that I will shortly fix. 

Ref: [Masters SuffixTriePresentation](https://kanhar.github.io/pdf/SuffixTriePresentation.pdf)

They are lightning fast (and low-memory footprint) at spell-checks and auto-complete. Below is a basic trie implementation

- TOC
{:toc}

### (Implement Trie)[https://leetcode.com/problems/implement-trie-prefix-tree/]

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
