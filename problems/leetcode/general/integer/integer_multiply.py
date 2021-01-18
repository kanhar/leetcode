'''
Given two non-negative integers num1 and num2 represented as strings, return the product of num1 and num2, also represented as a string.

Example 1:

Input: num1 = "2", num2 = "3"
Output: "6"
Example 2:

Input: num1 = "123", num2 = "456"
Output: "56088"

Ref: https://leetcode.com/problems/multiply-strings/
'''

#Input:  [1,2,4,5]
#Output: [1000, 200, 40, 5]
def splitNum(num):
    num = [int(d) for d in str(num)]
    pow = len(num)-1
    res = []
    for n in num:
        res.append(n*10**pow)
        pow -= 1
    return res

class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        n1 = splitNum(num1)
        n2 = splitNum(num2)

        # Because (a+b)*(c+d) = ac + ad + bc + bd
        return str(sum([x*y for x in n1 for y in n2]))
