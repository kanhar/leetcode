"""
Reverse bits of a given 32 bits unsigned integer.
Example 1:

Input: 00000010100101000001111010011100
Output: 00111001011110000010100101000000
"""
class Solution:
    def reverseBits(self, n):
        res = 0
        pow = 31

        while n:
            tmp = (n&1) << pow
            res += tmp

            n = n >> 1
            pow -=1

        return res
