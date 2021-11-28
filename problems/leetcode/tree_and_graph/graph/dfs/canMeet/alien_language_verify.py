'''
In an alien language, surprisingly they also use english lowercase letters, but possibly in a different
 order. The order of the alphabet is some permutation of lowercase letters.

Given a sequence of words written in the alien language, and the order of the alphabet, return true
if and only if the given words are sorted lexicographicaly in this alien language.

Example 1:

Input: words = ["hello","leetcode"], order = "hlabcdefgijkmnopqrstuvwxyz"
Output: true
Explanation: As 'h' comes before 'l' in this language, then the sequence is sorted.

Ref: https://leetcode.com/problems/verifying-an-alien-dictionary/
'''
import collections

class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        adj   = collections.defaultdict(set)
        for i in range(len(order)):
            adj[order[i]] = set(list(order[i+1:]))

        indeg = { c:0 for word in words for c in word }
        for w1,w2 in zip(words, words[1:]):
            for a,b in zip(w1,w2):
                if a != b:
                    if b not in adj[a]:
                        return False
                    break
            else:
                if len(w1) > len(w2):
                    return False
        return True