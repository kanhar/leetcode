"""
You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed, the only constraint stopping you from robbing each
of them is that adjacent houses have security system connected and it will automatically contact the
 police if two adjacent houses were broken into on the same night.

Given a list of non-negative integers representing the amount of money of each house,
determine the maximum amount of money you can rob tonight without alerting the police.

Example 1:

Input: [1,2,3,1]
Output: 4
Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

Ref: https://leetcode.com/problems/house-robber/
"""
import collections

class Solution:
    def rob(self, nums: List[int]) -> int:
        h = collections.defaultdict(int)
        if len(nums) == 0:
            return 0
        elif len(nums) == 1:
            return nums[0]
        elif len(nums) == 2:
            return max(nums[0], nums[1])

        h[0] = nums[0]
        h[1] = max(nums[0], nums[1])
        for i in range(1, len(nums)):
            h[i] = max(nums[i] + h[i - 2], h[i - 1])

        return max(h.values())

class Solution:
    def rob(self, nums: List[int]) -> int:
        def solve(nums, i):
            if i < 0:
                return 0
            else:
                return max(nums[i] + solve(nums, i - 2), solve(nums, i - 1))

        return solve(nums, len(nums) - 1)

class Solution:
    def rob(self, nums: List[int]) -> int:
        def solve(nums, i):
            if i < 0:
                return 0
            elif i in memo:
                return memo[i]
            else:
                memo[i] = max( nums[i] + solve(nums, i-2), solve(nums, i-1) )
                return memo[i]

        memo = {}
        return solve(nums, len(nums)-1)

