'''
Given an array of strings, group anagrams together.

Example:

Input: ["eat", "tea", "tan", "ate", "nat", "bat"],
Output:
[
  ["ate","eat","tea"],
  ["nat","tan"],
  ["bat"]
]
Note:

All inputs will be in lowercase.
'''

class Solution:
    def groupAnagrams(self, wordList):
        ans = collections.defaultdict(list)
        for word in wordList:
            count = [0] * 26
            for c in word:
                count[ord(c) - ord('a')] += 1
            ans[tuple(count)].append(word)
        return ans.values()

import collections
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = collections.defaultdict(list)
        for s in strs:
            d[frozenset(collections.Counter(s).items())].append(s)
        res = []
        for k,v in d.items():
            res.append(v)
        return res