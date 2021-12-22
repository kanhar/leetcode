"""
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Ref: https://leetcode.com/problems/3sum/
"""

class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        def twoSum(arr, target, ignore):
            left = ignore + 1
            right = len(arr) - 1
            res = []
            while left < right:
                if arr[left] + arr[right] == target:
                    tmp = [arr[ignore], arr[left], arr[right]]
                    res = res + [tmp]
                    left += 1
                    right -= 1
                elif arr[left] + arr[right] > target:
                    right -= 1
                else:
                    left += 1

            return res

        nums.sort()
        res = []

        for i, n in enumerate(nums):
            # If Sorted, and first number is > 0, subsequent numbers cannot add to zero.
            if n > 0:
                break
            # Leetcode specific optimizations. Not really relevant in an interview.
            if i > 0 and nums[i - 1] == nums[i]:
                continue

            res += twoSum(nums, -n, i)

        # remove duplicates
        return set([tuple(sorted(x)) for x in res])