'''
Given an array of integers and an integer k, you need to find the total number of continuous subarrays whose sum equals to k.

Example 1:
Input:nums = [1,1,1], k = 2
Output: 2
Ref: https://leetcode.com/problems/subarray-sum-equals-k/
'''

from collections import defaultdict
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        h = defaultdict(int)
        total = count = 0

        for n in nums:
            total += n
            if total == k:
                count += 1
            if total - k in h:
                count += h[total - k]
            h[total] += 1
        return count
