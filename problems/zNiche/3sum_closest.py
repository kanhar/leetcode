"""
Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

Ref: https://leetcode.com/problems/3sum-closest
"""
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        def twoSum(arr, currTarget, currVal):
            nonlocal target
            left = 0
            right = len(arr) - 1
            while left < right:
                currSum = arr[left] + arr[right]
                currDiff = abs(currTarget - currSum)

                if currDiff < abs(self.closest):
                    self.closest = currDiff
                    self.closestSum = arr[left] + arr[right] + currVal

                if currSum > currTarget:
                    right -= 1
                elif currSum < currTarget:
                    left += 1
                else:
                    left += 1
                    right -= 1

        nums.sort()
        self.closest = float('inf')
        self.closestSum = 0

        for i, n in enumerate(nums):
            twoSum(nums[i + 1:], target - n, n)

        return self.closestSum

"""
Generic. TLE
"""
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        def solve(arr, start, accum, visited):
            if len(accum) == 3:
                diff = abs(target - sum(accum))
                if diff < self.minDiff:
                    self.res = sum(accum)
                    self.minDiff = diff
            else:
                for i in range(start, len(arr)):
                    if i not in visited:
                        visited.add(i)
                        solve(arr, i + 1, accum + [arr[i]], visited)
                        visited.remove(i)

        self.res = 0
        self.minDiff = float('inf')
        solve(nums, 0, [], set())
        return self.res
