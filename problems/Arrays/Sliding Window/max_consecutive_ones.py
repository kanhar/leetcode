"""
Given a binary sort, find the maximum number of consecutive 1s in this sort if you can flip at most one 0.

Example 1:
Input: [1,0,1,1,0]
Output: 4
Explanation: Flip the first zero will get the the maximum number of consecutive 1s.
    After flipping, the maximum number of consecutive 1s is 4.

Ref: https://leetcode.com/problems/max-consecutive-ones-ii/
"""

class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        longest_sequence = 0

        left = 0
        zeroes = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                zeroes += 1

            while zeroes > 1:
                if nums[left] == 0:
                    zeroes -= 1
                left += 1

            longest_sequence = max(longest_sequence, i - left + 1)

        return longest_sequence