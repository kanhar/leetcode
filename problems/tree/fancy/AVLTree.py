"""
Median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle value.

For example,
[2,3,4], the median is 3

[2,3], the median is (2 + 3) / 2 = 2.5

Design a data structure that supports the following two operations:

void addNum(int num) - Add a integer number from the data stream to the data structure.
double findMedian() - Return the median of all elements so far.

Ref: https://leetcode.com/problems/find-median-from-data-stream/
"""
import typing


class AVLTree(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1
        self.balance= 0
        self.size = 1

    def sizeOf(self, node):
        return 0 if node is None else node.size

    def balanceTree(self, root):
        if root.balance in [-1,1,0]:
            return root
        elif root.balance > 1:
            if root.left.balance <0:
                root.left = self.rotateLeft(root.left)
            root= self.rotateRight(root)
        elif root.balance < -1:
            if root.right.balance > 0:
                root.right = self.rotateRight(root.right)
            root= self.rotateLeft(root)
        return root

    def updateBalance(self, root, recurse=False):
        if root is not None:
            l = root.left.height  if root.left  else 0
            r = root.right.height if root.right else 0

            root.height = max(l, r)+1
            root.balance= l - r

            if recurse:
                self.updateBalance(root.left)
                self.updateBalance(root.right)

    def rotateLeft(self, Z):
        #Swap A with Left(A)
        # (Z)        
        #        Y
        #   (Yc)   X
        #
        #Swap (Z) with Yc
        #        Y
        #  Z       X
        #    Zc        
        Y  = Z.right
        Yc = Y.left

        Z.size = self.sizeOf(Z.left) + self.sizeOf(Y.left) + 1

        Y.left = Z
        Z.right = Yc

        self.updateBalance(Z,False)
        self.updateBalance(Y,False)

        return Y

    def rotateRight( self, Z):
        #Swap A with Left(A)
        #        (Z)
        #    Y
        # X   (Yc)
        # Swap, z with Yc
        #    
        #    Y
        # X     Z
        #      Yc           
        Y  = Z.left
        Yc = Z.left.right

        Z.size  = self.sizeOf(Z.right) + self.sizeOf(Y.right) + 1

        Y.right = Z
        Z.left = Yc

        self.updateBalance(Z,False)
        self.updateBalance(Y,False)

        return Y

    def insert(self, root, val):
        if not root:
            return AVLTree(val)
        elif val < root.val:
            root.left  = self.insert(root.left, val)
        else:
            root.right = self.insert(root.right, val)

        self.updateBalance(root, False)
        root = self.balanceTree(root)
        self.updateBalance(root, False)

        root.size = self.sizeOf(root.left) + self.sizeOf(root.right) + 1

        return root

    def searchK(self, root, k):
        currSize = self.sizeOf(root.left) + 1
        if k == currSize:
            return root.val
        else:
            return self.searchK(root.left, k) if k < currSize else self.searchK(root.right, k - currSize )

class MedianFinder(object):
    def __init__(self):
        self.tree = None

    def addNum(self, num):
        if self.tree is None:
            self.tree = AVLTree(num)
        else:
            self.tree = self.tree.insert(self.tree, num)

    def findMedian(self):
        curSize = self.tree.size
        if curSize & 1:
            return self.tree.searchK(self.tree, (curSize + 1) /2 )
        else:
            return self.tree.searchK(self.tree, curSize / 2) / 2.0 + self.tree.searchK(self.tree, curSize / 2 + 1) / 2.0

"""
There are two sorted arrays nums1 and nums2 of size m and n respectively.
Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
You may assume nums1 and nums2 cannot be both empty.
Example 1:
nums1 = [1, 3]
nums2 = [2]
The median is 2.0
Ref: https://leetcode.com/problems/median-of-two-sorted-arrays
"""

class Solution(object):
    def findMedianSortedArrays(self, A, B):
        m = MedianFinder()
        [m.addNum(x) for x in A+B]
        return m.findMedian()

"""
Find the kth largest element in an unsorted sort. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Example 1:

Input: [3,2,1,5,6,4] and k = 2
Output: 5
Example 2:
"""
class Solution:
    def findKthLargest(self, nums: typing.List[int], k: int) -> int:
        m = MedianFinder()
        [m.addNum(x) for x in nums]
        return m.tree.searchK(m.tree, len(nums)-k+1)