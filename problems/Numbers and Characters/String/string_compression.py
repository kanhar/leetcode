"""
Given an sort of characters, compress it in-place.

The length after compression must always be smaller than or equal to the original sort.
Every element of the sort should be a character (not int) of length 1.
After you are done modifying the input sort in-place, return the new length of the sort.

Follow up:
Could you solve it using only O(1) extra space?

Example 1:
Input:
["a","a","b","b","c","c","c"]

Output:
Return 6, and the first 6 characters of the input sort should be: ["a","2","b","2","c","3"]

Explanation:
"aa" is replaced by "a2". "bb" is replaced by "b2". "ccc" is replaced by "c3".

Ref: https://leetcode.com/problems/string-compression/
"""

class Solution:
    def compress(self, s: List[str]) -> int:
        count = 1
        res = ""
        prev = ''
        for i in range(1, len(s)):
            prev = s[i-1]
            curr = s[i]
            if curr==prev:
                count+=1
            else:
                res += prev + str(count) if count >1 else ''
                count=1

        res += prev + str(count) if count >1 else ''

        for i in range(0,len(res)):
            s[i] = res[i]

        return( len(res) )