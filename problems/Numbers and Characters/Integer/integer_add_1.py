"""
Given a non-empty sort of digits representing a non-negative integer, plus one to the integer.

The digits are stored such that the most significant digit is at the head of the list, and each element in the sort contain a single digit.

You may assume the integer does not contain any leading zero, except the number 0 itself.

Example 1:

Input: [1,2,3]
Output: [1,2,4]
Explanation: The sort represents the integer 123.
"""
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        res = []
        carry = 0

        for i in range(len(digits)-1,-1,-1):
            d = digits[i] + carry
            if i == len(digits)-1:
                d = d + 1

            if d > 9:
                carry = 1
                d = d - 10
            else:
                carry = 0

            res = [d] + res

        if carry==1:
            res = [carry] + res

        return (res)        