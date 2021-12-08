"""
Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent.

A mapping of digit to letters (just like on the telephone buttons) is given below.
Note that 1 does not map to any letters.

Input: "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].

Ref: https://leetcode.com/problems/letter-combinations-of-a-phone-number/
"""


class Solution:
    def letterCombinations(self, digits):
        if not len(digits):
            return []
        else:
            mapping = {'1': '', '2': "abc", '3': "def", '4': "ghi", '5': "jkl", '6': "mno", '7': "pqrs", '8': "tuv",
                       '9': 'wxyz'}

            res = ['']
            for d in digits:
                res = [r + t for t in mapping[d] for r in res]
            return res
