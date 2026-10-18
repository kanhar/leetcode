"""
Given two words (beginWord and endWord), and a dictionary's word list, find the length of shortest transformation sequence from beginWord to endWord, such that:

Only one letter can be changed at a time.
Each transformed word must exist in the word list. Note that beginWord is not a transformed word.
Note:

Return 0 if there is no such transformation sequence.
All words have the same length.
All words contain only lowercase alphabetic characters.
You may assume no duplicates in the word list.
You may assume beginWord and endWord are non-empty and are not the same.
Example 1:

Input:
beginWord = "hit",
endWord = "cog",
wordList = ["hot","dot","dog","lot","log","cog"]

Ref: https://leetcode.com/problems/word-ladder/
"""

class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        def num_of_differences(str1, str2):
            count = 0
            for i in range(0, len(str1)):
                if str1[i] != str2[i]:
                    count = count + 1
            return count

        def transform(english_words, start, end, path=[]):
            if start == end:
                return [ path]

            res = []
            for w in english_words:
                if num_of_differences(w, start)==1 and w not in path:
                    res = res + transform(english_words, w, end, path + [w])
            return res

        res = transform(wordList, beginWord, endWord)
        if res == []:
            return 0
        else:
            return len(min(res, key = len))+1