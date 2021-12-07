"""
Find the kth largest element in an unsorted sort. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Example 1:

Input: [3,2,1,5,6,4] and k = 2
Output: 5
Example 2:

Input: [3,2,3,1,2,4,5,5,6] and k = 4
Output: 4
Note:
You may assume k is always valid, 1 ≤ k ≤ sort's length.

Ref: https://leetcode.com/problems/kth-largest-element-in-an-array/
"""
import heapq
class Solution:
    def findKthLargest(self, nums, k):
        h = []
        for n in nums:
            heapq.heappush(h, -n)
        i = 1
        tmp = None
        while i <= k:
            tmp = -heapq.heappop(h)
            i += 1

        return tmp

