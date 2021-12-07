"""
Given a string s, find the longest palindromic substring in s.
You may assume that the maximum length of s is 1000.

Example 1:

Input: "babad"
Output: "bab"
Note: "aba" is also a valid answer.
"""
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def palindromeAt(w,l,r):
            while l>=0 and r < len(w) and w[l]==w[r]:
                l-=1; r+=1
            return w[l+1:r]

        res = ""
        for i in range(0, len(s)):
            odd  = palindromeAt(s,i,i)
            even = palindromeAt(s,i,i+1)
            res = max([res,odd,even], key=len)
        return res

"""
Is Valid Palindrome
"""
def isPalindrome(self, s: str) -> bool:
    def isValid(w):
        return True if len(w) <= 1 else w[0]==w[-1] and isValid(w[1:len(w)-1])
    return isValid([ x for x in s.lower() if x.isdigit() or x.isalpha()])




