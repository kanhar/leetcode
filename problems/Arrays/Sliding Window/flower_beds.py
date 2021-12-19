"""
You have a long flowerbed in which some of the plots are planted, and some are not.
However, flowers cannot be planted in adjacent plots.

Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty,
and an integer n, return if n new flowers can be planted in the flowerbed without violating the no-adjacent-flowers rule.


Example 1:

Input: flowerbed = [1,0,0,0,1], n = 1
Output: true
Ref: https://leetcode.com/problems/can-place-flowers/
"""

class Solution:
    def canPlaceFlowers(self, f: List[int], n: int) -> bool:
        for i in range(0, len(f)):
            a = 0 if i == 0 else f[i - 1]
            b = f[i]
            c = 0 if i == len(f) - 1 else f[i + 1]

            if a == b == c == 0:
                f[i] = 1
                n -= 1

        return n <= 0

