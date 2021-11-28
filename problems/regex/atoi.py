"""
Implement atoi:
Try to break it yourself before submitting. Key idea is keep processing number until valid.
If invalid char pops in return whatever you have.

Ref: https://leetcode.com/problems/string-to-integer-atoi/
"""

import re
class Solution:
    def myAtoi(self, str):
        MAX_INT =  2**31 - 1
        MIN_INT = -2**31

        #^ --> Starting of String, followed by 0 or 1 (+-), followed by 0* zeroes followed by atleast one digit
        regex = re.search('^[-+]?0*\d+', str.strip())
        if regex:
            num = int(regex[0])
            if MIN_INT <= num <= MAX_INT:
                return num
            else:
                return MIN_INT if num < MIN_INT else MAX_INT
        else:
            return 0
