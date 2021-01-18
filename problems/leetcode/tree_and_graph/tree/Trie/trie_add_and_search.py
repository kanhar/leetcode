'''
Design a data structure that supports the following two operations:

void addWord(word)
bool search(word)
search(word) can search a literal word or a regular expression string containing only letters a-z or .. A . means it can represent any one letter.

Example:

addWord("bad")
addWord("dad")
addWord("mad")
search("pad") -> false
search("bad") -> true
search(".ad") -> true
search("b..") -> true

Ref: https://leetcode.com/problems/add-and-search-word-data-structure-design/
'''

class WordDictionary:

    def __init__(self):
        def createTrie():
            return defaultdict(createTrie)

        self.root = createTrie()

    def addWord(self, word: str) -> None:
        curr = self.root
        for w in word:
            curr=curr[w]
        curr['#']

    def searchWithRegex(self, node, word):
        curr = node
        for i,w in enumerate(word):
            if w == '.':
                for k,v in curr.items():
                    if self.searchWithRegex(v, word[i+1:]):
                        return True
                return False
            if w not in curr:
                return False
            else:
                curr = curr[w]

        return '#' in curr

    #A word can contain the dot character '.' to represent any one letter.
    def search(self, word: str) -> bool:
        return self.searchWithRegex(self.root, word)

