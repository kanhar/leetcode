{: .no_toc}
# Ternary Search Tries
[Ternary Search Tries](https://en.wikipedia.org/wiki/Ternary_search_tree) or Prefix Tries are cool. My impl. below generally works, 
but has a few bugs, (4/15 test cases fail) that I will shortly fix. 

Ref: [Masters SuffixTriePresentation](https://kanhar.github.io/pdf/SuffixTriePresentation.pdf)

They are lightning fast (and low-memory footprint) at spell-checks and auto-complete. Below is a basic trie implementation

- TOC
{:toc}

```python
class TSTNode(object):
    def __init__(self, ch, val=0):
        self.key = ch
        self.val = val
        self.left = None
        self.mid = None
        self.right = None

def printTree(node, depth = 0):
    if node:
        print("\t" * depth, node.key, node.val)
        printTree(node.left,  depth+1)
        printTree(node.mid,   depth+1)
        printTree(node.right, depth+1)               
        
class Trie:
   
    def __init__(self):
        self.root = None
        
    def insert(self, key: str) -> None:       
        
        def create(node, word, val):
            if len(word) == 0:
                return None

            ch = word[0]
            if node is None:
                node = TSTNode(ch)

            if ch < node.key:
                node.left = create(node.left, word[1:], val)
            elif ch > node.key:
                node.right = create(node.right, word[1:], val)
            else:
                # If last character
                if len(word) == 1:
                    node.key = ch
                    node.val = val
                else:
                    node.mid = create(node.mid, word[1:], val)
            
            return node
                    
        self.root = create(self.root, key, 1)           
        printTree(self.root)
                 

    def search(self, word: str) -> bool:
        curr = self.root        
        
        for i,w in enumerate(word):
            if curr is None:
                return False
            
            if w == curr.key:                
                # last char check
                if curr is not None and i == len(word)-1:
                    return curr.val != 0
                else:
                    curr = curr.mid
            elif w < curr.key:
                curr = curr.left
                if i == len(word)-1:
                    return curr is not None and curr.val != 0                
                elif curr is not None and curr.key != w:
                    return False
            else:
                curr = curr.right
                if i == len(word)-1:
                    return curr is not None and curr.val != 0 
                elif curr is not None and curr.key != w:
                    return False

        return True

    def startsWith(self, word: str) -> bool:
        curr = self.root        
        
        for i,w in enumerate(word):
            if curr is None:
                return False
            
            if w == curr.key:
                curr = curr.mid
                # last char check not necessary
            elif w < curr.key:
                curr = curr.left
                if i == len(word)-1:
                    return curr is not None             
                elif curr is not None and curr.key != w:
                    return False
            else:
                curr = curr.right
                if i == len(word)-1:
                    return curr is not None
                elif curr is not None and curr.key != w:
                    return False

        return True
```