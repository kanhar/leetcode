'''
Given an array of n positive integers and a positive integer s, find the minimal length of a contiguous subarray of which the sum ≥ s. If there isn't one, return 0 instead.

Example:

Input: s = 7, nums = [2,3,1,2,4,3]
Output: 2
Explanation: the subarray [4,3] has the minimal length under the problem constraint.

Ref: https://leetcode.com/problems/minimum-size-subarray-sum/
'''
class Solution:
    def minSubArrayLen(self, s, nums):

        total = 0
        left = 0
        min_r = len(nums) + 1

        for right in range(len(nums)):
            total += nums[right]
            while total >= s and left <= right:
                min_r = min(min_r, right - left + 1)
                total -= nums[left]
                left += 1

        return min_r if min_r <= len(nums) else 0