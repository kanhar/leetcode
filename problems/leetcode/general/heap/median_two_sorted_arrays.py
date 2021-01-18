'''
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

You may assume nums1 and nums2 cannot be both empty.

Example 1:

nums1 = [1, 3]
nums2 = [2]

The median is 2.0

Ref: https://leetcode.com/problems/median-of-two-sorted-arrays/
'''

class Solution(object):
    def findMedianSortedArrays(self, A, B):
        if len(A)>len(B):
            A, B = B, A

        total = len(A) + len(B)
        lo = 0
        hi = len(A)

        while lo <= hi:
            mid = (lo+hi)//2
            aL = A[mid]     if mid in range(len(A))     else float('-inf')
            aR = A[mid+1]   if mid+1 in range(len(A))   else float('inf')

            mid = total//2 - mid
            bL = B[mid]     if mid in range(len(B))     else float('-inf')
            bR = B[mid+1]   if mid+1 in range(len(B))   else float('inf')

            if aL <= bR and aR <= bL:
                if total %2 == 0:
                    return (max(aL, bL) + min( aR, bR) ) / 2.0
                else:
                    return min(aR, bR)
            elif aL > bR:
                hi = mid - 1
            else:
                lo = mid + 1
        return