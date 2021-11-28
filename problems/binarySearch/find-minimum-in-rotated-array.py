"""
Suppose an sort sorted in ascending order is rotated at some pivot unknown to you beforehand.

(i.e.,  [0,1,2,4,5,6,7] might become  [4,5,6,7,0,1,2]).

Find the minimum element.

You may assume no duplicate exists in the sort.

Example 1:

Input: [3,4,5,1,2] 
Output: 1

Ref:https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
"""

class Solution:
    def find_rotate_index(self, nums, left, right):
        if nums[left] <= nums[right]:
            return 0

        while left <= right:
            mid = (left + right) // 2

            if nums[mid+1] < nums[mid]:
                return mid + 1
            else:
                if nums[left] > nums[mid]: #Left side is unsorted. This condition cannot be reversed (i.e. zone into where the problem is, not opposite )
                    right = mid - 1
                else:
                    left = mid + 1

    def findMin(self, nums: List[int]) -> int:
        pivot = self.find_rotate_index(nums, 0, len(nums)-1)
        return nums[pivot]


"""
Same as above with duplicate

Ref: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/
"""
class Solution:
    def find_rotate_index(self, nums, left, right):
        if nums[left] < nums[right] or len(nums)==1:
            return 0

        while left <= right:
            mid = (left + right) // 2
            if nums[mid+1] < nums[mid]:
                return mid + 1
            elif nums[mid] < nums[mid-1]:   #Additional Condition (when duplicate, sorted doesnt imply order)
                return mid
            else:
                if nums[left] > nums[mid]:
                    right = mid - 1
                elif nums[right] < nums[mid]:
                    left = mid + 1
                else:                       #Additional Condition (when they are equal)
                    right -=1
        return mid

    def findMin(self, nums: List[int]) -> int:
        pivot = self.find_rotate_index(nums, 0, len(nums)-1)
        return nums[pivot]