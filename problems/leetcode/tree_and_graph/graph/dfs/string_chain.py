'''
Given a list of words, each word consists of English lowercase letters.
Let's say word1 is a predecessor of word2 if and only if we can add exactly one letter anywhere in word1 to make it equal to word2.  For example, "abc" is a predecessor of "abac".
A word chain is a sequence of words [word_1, word_2, ..., word_k] with k >= 1, where word_1 is a predecessor of word_2, word_2 is a predecessor of word_3, and so on.

Return the longest possible length of a word chain with words chosen from the given list of words.

Input: ["a","b","ba","bca","bda","bdca"]
Output: 4
Explanation: one of the longest word chain is "a","ba","bda","bdca".

ReF: https://leetcode.com/problems/longest-string-chain/
'''

from typing import List
class Solution:
    def longestStrChain(self, words: List[str]) -> int:
        def longest(word_set, cache, word):
            if word not in cache:
                ret = 1
                for i in range(len(word)):
                    w = word[:i] + word[i+1:]
                    if w and w in word_set:
                        ret = max(ret, 1 + longest(word_set, cache, w))

                cache[word] = ret

            return cache[word]

        cache = {}
        return max( longest(set(words), cache, x) for x in words)

words = ["a", "b", "ba", "bca", "bda", "bdca"]
print(Solution().longestStrChain(words)==4)
