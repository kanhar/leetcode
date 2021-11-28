'''
Given a non-empty string s and a dictionary wordDict containing a list of non-empty words, determine if s can be segmented into a space-separated sequence of one or more dictionary words.

Note:

The same word in the dictionary may be reused multiple times in the segmentation.
You may assume the dictionary does not contain duplicate words.
Example 1:

Input: s = "leetcode", wordDict = ["leet", "code"]
Output: true
Explanation: Return true because "leetcode" can be segmented as "leet code".

Ref: https://leetcode.com/problems/word-break/
'''

class Solution(object):
    def wordBreak(self, s, wordDict, accum = []):
        def solve(arr, accum = []):
            if len(arr)==0 and len(s) == sum([len(x) for x in accum]):
                self.res.append(accum)
                return
            for i in range(len(arr)+1):
                curr = arr[:i]
                if curr in set(wordDict):
                    solve(arr[i:], accum + [curr])
        self.res = []
        solve(s)
        return len(self.res)!=0

def createTrie(words):
    def _createTrie(): return collections.defaultdict(_createTrie)

    t = _createTrie()
    for word in words:
        root = t
        for w in word:
            root = root[w]
        root['#']
    return t

class Solution(object):
    def wordBreak(self, s, wordDict):
        def search(t,s):
            root = t

            for i,c in enumerate(s):
                if c not in t:
                    return False
                else:
                    if '#' in t[c] and search(root, s[i+1:]):
                        return True
                    t = t[c]

            return '#' in t

        t = createTrie(wordDict)
        return search(t, s)
