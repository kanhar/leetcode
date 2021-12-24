"""
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Ref: https://leetcode.com/problems/3sum/
"""
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        def twoSum(arr, target):
            left = 0
            right = len(arr) - 1

            res = []
            while left < right:
                total = arr[left] + arr[right]
                if total > target:
                    right -= 1
                elif total < target:
                    left += 1
                else:
                    res.append([arr[left], arr[right]])
                    left += 1
                    right -= 1
            return res

        nums.sort()
        pairs = []
        target = 0
        for i, n in enumerate(nums):
            tmp = twoSum(nums[i + 1:], target - n)
            for t in tmp:
                pairs.append([n] + t)

        return set([tuple(sorted(x)) for x in pairs])