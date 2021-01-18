'''
Write a function that takes an unsigned integer and return the number of '1' bits it has (also known as the Hamming weight).
Ex:
Input: 00000000000000000000000000001011
Output: 3
Explanation: The input binary string 00000000000000000000000000001011 has a total of three '1' bits.
'''
class Solution:
    def hammingWeight(self, num: int) -> int:
        count = 0
        while(num):
            if num & 1:
                count+=1
            num = num>>1
        return count