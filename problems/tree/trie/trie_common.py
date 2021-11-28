"""
Implement a trie with insert, search, and startsWith methods.

Example:

trie trie = new trie();

trie.insert("apple");
trie.search("apple");   // returns true
trie.search("app");     // returns false
trie.startsWith("app"); // returns true
trie.insert("app");
trie.search("app");     // returns true

Ref: https://leetcode.com/problems/implement-trie-prefix-tree/
"""

class Trie:

    def __init__(self):
        def createTrie(): return defaultdict(createTrie)
        self.root =  createTrie()

    def insert(self, word: str) -> None:
        def addWord(trie, word):
            root = trie
            for w in word:
                root=root[w]
            root['#']
            return trie
        self.root = addWord(self.root, word)

    def search(self, word: str) -> bool:
        curr = self.root

        for w in word:
            if w not in curr:
                return False
            else:
                curr = curr[w]

        return '#' in curr

    def startsWith(self, prefix: str) -> bool:
        curr = self.root

        for w in prefix:
            if w not in curr:
                return False
            else:
                curr = curr[w]
        return True

    def _printTrie(self, t,tab=0):
        for k,v in t.items():
            print( " " *tab, k,len(t.values()))
            self._printTrie(v,tab+2)

