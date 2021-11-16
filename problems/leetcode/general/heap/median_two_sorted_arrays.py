"""
There are two sorted arrays nums1 and nums2 of size m and n respectively.

Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

You may assume nums1 and nums2 cannot be both empty.

Example 1:

nums1 = [1, 3]
nums2 = [2]

The median is 2.0

Ref: https://leetcode.com/problems/median-of-two-sorted-arrays/
Ref: https://leetcode.com/problems/median-of-two-sorted-arrays/discuss/2755/9-lines-O(log(min(mn)))-Python/506196

Problem: Given A, B as two sorted arrays, find common median. Generally you would merge them, and find the mid-point.
Key Intuition: Focus on array A ( forget about B ). Get the Midpoint for A, and then and only then, ask the question,
for this midpoint of A, what would be an appropriate midpoint of B to make this a median for (A+B).
If the match in B breaks sorting order of A+B, adjust binary search indices, get a new Midpoint for A.
Key Formula: Median A + Median B ~= Median (A+B)/2. Use this to calculate Median B given (arbitrary) Median A.
"""

class Solution(object):
    def findMedianSortedArrays(self, A, B):
        if len(A) > len(B):
            A, B = B, A

        total = len(A) + len(B)
        lo = 0
        hi = len(A)
        while lo <= hi:
            # Find Partition in A using a regular binary search method.
            midA = (hi + lo) // 2
            A_left = A[midA - 1] if midA != 0 else float('-inf')
            A_right = A[midA] if len(A) != midA else float('inf')

            # Partition index in B derived from A, and moves in opposite direction of Partition A, we know that:
            # - midA + midB = Total // 2
            # - midB = Total // 2 - midA
            midB = total // 2 - midA
            B_left = B[midB - 1] if midB != 0 else float('-inf')
            B_right = B[midB] if len(B) != midB else float('inf')

            if A_left <= B_right and A_right >= B_left:  # Key Intuition
                leftEdge = max(A_left, B_left)
                rightEdge = min(A_right, B_right)
                if total % 2 == 0:
                    return (leftEdge + rightEdge) / 2.0
                else:
                    return rightEdge
            elif A_left > B_right:  # A is too big   --> Reduce A partition size
                hi = midA - 1
            elif A_left < B_right:  # A is too small --> Increase A partition size
                lo = midA + 1
        return None