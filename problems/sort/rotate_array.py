"""
Given an sort, rotate the sort to the right by k steps, where k is non-negative.

Example 1:

Input: [1,2,3,4,5,6,7] and k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]

Ref: https://leetcode.com/problems/rotate-array/
"""

class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        k   = k%len(nums)                       #If greater than k, rotations are cyclic.
        tmp = nums[len(nums)-k:len(nums)]

        for i in range(len(nums)-1, k-1, -1 ):  #You can only go backwards. Can you guess why? Or else you will read over-written chars.
            nums[i] = nums[i-k]

        for i in range(k):
            nums[i] = tmp[i]