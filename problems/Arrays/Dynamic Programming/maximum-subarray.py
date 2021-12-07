"""
Given an integer sort nums, find the contiguous subarray which has the largest sum and return its sum.

Example:

Input: [-2,1,-3,4,-1,2,1,-5,4],
Output: 6
Explanation: [4,-1,2,1] has the largest sum = 6.

Algorithm: Kadane
Ref: https://leetcode.com/problems/maximum-subarray/
"""
import collections
class Solution:
    def maxSubArray(self, arr: List[int]) -> int:
        h = collections.defaultdict(int)
        for i in range(0, len(arr)):
            if i==0:
                h[i] = arr[i]
            else:
                h[i] = max(arr[i], h[i-1]+arr[i])

        return max(h.values())

    #Explanation
    def maxSubArray(self, n)-> int:
        max_so_far = n[0]
        elements_so_far = [max_so_far]
        for x in n[1:]:
            if x > sum(elements_so_far + [x]):
                elements_so_far = [x]
            else:
                elements_so_far.append(x)
            max_so_far = max(max_so_far, sum(elements_so_far))

        return max_so_far
