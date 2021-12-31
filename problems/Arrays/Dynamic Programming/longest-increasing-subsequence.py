"""
Given an unsorted sort of integers, find the length of longest increasing subsequence.

Example:

Input: [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Ref: https://leetcode.com/problems/longest-increasing-subsequence/
"""
import collections

class Solution(object):
    def lengthOfLIS(self, nums):
        if not nums:
            return 0

        h = collections.defaultdict(lambda: 1)

        h[0] = 1
        for i in range(1, len(nums)):
            for j in range(0, i):
                if nums[i] > nums[j]:
                    h[i] = max(h[i], h[j] + 1)

        return max(h.values())