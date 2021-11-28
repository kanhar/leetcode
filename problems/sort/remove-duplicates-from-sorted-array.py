"""
Given a sorted sort nums, remove the duplicates in-place such that each element appear only once and return the new length.

Do not allocate extra space for another sort, you must do this by modifying the input sort in-place with O(1) extra memory.

Example 1:

Given nums = [1,1,2],

Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively.

It doesn't matter what you leave beyond the returned length.

Ref: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
"""

class Solution:
    def removeDuplicatesSlow(self, nums: List[int]) -> int:
        deleted = 0
        for i in range(0,len(nums)-deleted-1):
            while nums[i]==nums[i+1] and i < len(nums)-deleted-1:
                deleted +=1
                for k in range(i+1, len(nums)-deleted):
                    nums[k] = nums[k+1]

        return len(nums)-deleted

    def removeDuplicates(self, nums):
        if len(nums)==0:
            return 0
        else:
            idx = 1
            for i in range(1, len(nums)):
                if i != 0 and nums[i] != nums[i-1]: #if equal continue i
                    nums[idx] = nums[i]
                    idx +=1
            return idx