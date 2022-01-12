{: .no_toc}
# Ternary Search Tries
Practise here: [Leetcode]()

These are different from Ternary Search Tries.

- TOC
{:toc}

```python
class TSTNode(object):
    def __init__(self, ch):
        self.key = ch
        self.left = None
        self.mid = None
        self.right = None
        
class Trie:
   
    def __init__(self):
        self.root = None
        
    def insert(self, string: str) -> None:       
        
        def create(node, word):
            if word is None or len(word) == 0:
                return

            ch = word[0]
            if node is None:
                node = TSTNode(ch)

            if ch < node.key:
                node.left = create(node.left, word[1:])
            elif ch > node.key:
                node.right = create(node.right, word[1:])
            else:
                node.mid = create(node.mid, word[1:])
            
            return node
        
        def printTree(node, depth = 0):
            if node:
                print("\t" * depth, node.key)
                printTree(node.left,  depth+1)
                printTree(node.mid,   depth+1)
                printTree(node.right, depth+1)               
                
            
        self.root = create(None, string)           
        printTree(self.root)
                 

    def search(self, word: str) -> bool:
        print("")
        

    def startsWith(self, prefix: str) -> bool:
        print("")


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)
```