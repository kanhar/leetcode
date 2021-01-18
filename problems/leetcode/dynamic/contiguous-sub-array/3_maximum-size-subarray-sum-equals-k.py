'''
Given an array nums and a target value k, find the maximum length of a subarray that sums to k. If there isn't one, return 0 instead.

Note:
The sum of the entire nums array is guaranteed to fit within the 32-bit signed integer range.

Example 1:

Input: nums = [1, -1, 5, -2, 3], k = 3
Output: 4
Explanation: The subarray [1, -1, 5, -2] sums to 3 and is the longest.

Ref: https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/
'''
class Solution:
    def maxSubArrayLen(self, nums, k):
        res = total = 0
        h = collections.defaultdict(int)

        for i in range(len(nums)):
            total += nums[i]
            if total not in h:
                h[total] = i

            if total == k:    #everything from 0, to i has been aggregated to add up to k. Length = i-0+1 or i+1
                res = max(res, i-0+1)
            elif total-k in h:
                res = max(res, i-h[total-k])

        return res