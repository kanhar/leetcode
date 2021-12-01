"""
Given an array of n positive integers and a positive integer s, find the minimal length of a
contiguous subarray of which the sum ≥ s. If there isn't one, return 0 instead.

Example:

Input: s = 7, nums = [2,3,1,2,4,3]
Output: 2
Explanation: the subarray [4,3] has the minimal length under the problem constraint.

Ref: https://leetcode.com/problems/minimum-size-subarray-sum/

TLE ( but simple )
"""

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        minres = float('inf')
        currSum = 0
        for i in range(len(nums)):
            currSum += nums[i]
            while currSum >= target:
                minres = min(minres, i + 1 - left)  # or Get full array via nums[left:i + 1]
                currSum -= nums[left]
                left += 1

        if minres == float('inf'):
            return 0
        else:
            return minres
