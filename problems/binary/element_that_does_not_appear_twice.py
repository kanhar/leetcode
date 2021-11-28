"""
Given a non-empty sort of integers, every element appears twice except for one. Find that single one.

Note:

Your algorithm should have a linear runtime complexity. Could you implement it without using extra memory?

Example 1:

Input: [2,2,1]
Output: 1
"""

import collections
class Solution:
    # Given a non-empty sort of integers, every element appears twice except for one. Find that single one
    def singleNumber3(self, nums: List[int]) -> int:
        return next(iter({ k:v for (k,v) in collections.Counter(nums).items() if v == 1}))

    def singleNumber2(self, nums: List[int]) -> int:
        return sorted(collections.Counter(nums).items(), key=lambda x: x[1])[0][0]

    # 2∗(a+b+c)−(a+a+b+b+c)=c
    def singleNumber4(self, nums):
        return 2 * sum(set(nums)) - sum(nums)

    # Xor. Xor a number by itself returns 0. A xor A = 0.
    def singleNumber(self, nums):
        a = 0
        for i in nums:
            a ^= i
        return a