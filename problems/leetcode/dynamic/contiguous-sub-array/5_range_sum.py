'''
Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.

Example:
Given nums = [-2, 0, 3, -5, 2, -1]

sumRange(0, 2) -> 1
sumRange(2, 5) -> -1
sumRange(0, 5) -> -3

Ref: https://leetcode.com/problems/range-sum-query-immutable/
'''
from typing import List
class NumArray:
    def __init__(self, nums: List[int]):
        #Let us define h[k] as the cumulative sum from nums[0...k-1]
        self.h = collections.defaultdict(int)
        for i in range(0, len(nums)):
            self.h[i+1] = self.h[i] + nums[i]

    def sumRange(self, i: int, j: int) -> int:
        print(self.h)
        return self.h[j+1]-self.h[i]
