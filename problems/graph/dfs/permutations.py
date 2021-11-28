"""
Given a collection of distinct integers, return all possible permutations.
Example:

Input: [1,2,3]
Output:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]

#Ref: https://leetcode.com/problems/permutations/

Note: Solution is position dependent, hence value independent. Also works if there are duplicates like below:
Ref: https://leetcode.com/problems/permutations-ii/
"""

class Solution(object):
    def permute(self, arr: List[int]) -> List[List[int]]:
        def perm(arr, accum = [], visited = set()):
            if len(accum) == len(arr):
                self.res.add(tuple(accum))
            else:
                for i in range(len(arr)):
                    if i not in visited:
                        perm(arr, accum + [arr[i]], visited | set([i]))

        self.res = set()
        perm(arr)
        return self.res

"""
Implement next permutation, which rearranges numbers into the lexicographically next greater permutation of numbers.

If such arrangement is not possible, it must rearrange it as the lowest possible order (ie, sorted in ascending order).

The replacement must be in-place and use only constant extra memory.

Here are some examples. Inputs are in the left-hand column and its corresponding outputs are in the right-hand column.

1,2,3 → 1,3,2 (and not 2,1,3 )
3,2,1 → 1,2,3
1,1,5 → 1,5,1

Next permutation: https://leetcode.com/problems/next-permutation/
"""
class Solution:
    def nextPermutation(self, nums: List[int]) -> None:
        pivot = None
        for i in range(len(nums)-1, 0, -1):
            if nums[i] > nums[i-1]:
                pivot = i-1
                break

        if pivot is None:
            nums[:] = nums[::-1]
        else:
            for i in range(len(nums)-1, pivot, -1):
                if nums[i] > nums[pivot]:
                    nums[i], nums[pivot] = nums[pivot], nums[i]
                    break
            nums[:]=nums[:pivot+1]+nums[pivot+1:][::-1]

    # Much simpler than above, but does not get strictly greater permutation.
    # Ex: [1,3,2] returns [3,1,2] and not [2,1,3]
    def getAnyGreaterPermutation(self, nums: List[int]) -> None:
        i = len(nums)-1

        while i >= 1:
            if nums[i] > nums[i-1]:
                nums[i-1], nums[i] = nums[i], nums[i-1]
                return
            else:
                i-=1

        nums.reverse()
