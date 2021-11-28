'''
In English, we have a concept called root, which can be followed by some other words to form another longer word - let's call this word successor. For example, the root an, followed by other, which can form another word another.

Now, given a dictionary consisting of many roots and a sentence. You need to replace all the successor in the sentence with the root forming it. If a successor has many roots can form it, replace it with the root with the shortest length.

You need to output the sentence after the replacement.

Example 1:

Input: dict = ["cat", "bat", "rat"]
sentence = "the cattle was rattled by the battery"
Output: "the cat was rat by the bat"

Ref: https://leetcode.com/problems/replace-words/
'''
import collections

def createTrie(words):
    def _createTrie(): return collections.defaultdict(_createTrie)

    t = _createTrie()
    for word in words:
        root = t
        for w in word:
            root = root[w]
        root['#']
    return t

class Solution:
    def replaceWords(self, words: List[str], sentence: str) -> str:
        trie = createTrie(words)
        wordList = sentence.split()

        res = []
        for word in wordList:
            curr = trie
            tmp  = ''
            for i, w in enumerate(word):
                if w not in curr:
                    res += [word]
                    break
                else:
                    tmp += w
                    curr = curr[w]
                    if '#' in curr:
                        res += [tmp]
                        break
                    elif i == len(word)-1:
                        res += [tmp]
                        break

        return ' '.join(res)