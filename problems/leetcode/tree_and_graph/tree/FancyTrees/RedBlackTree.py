class RedBlackTree(object):
    def __init__(self, val):
        self.val = val
        self.size = 1
        self.left = None
        self.right = None
        self.isRed = True

    def sizeOf(self, node):
        return 0 if node is None else node.size

    # Example: Rotate Left
    # Z is root. Y is Z's right. and so on.
    # (Z)
    #        Y
    #   Yl       X
    #
    # Swap (Z) with Yl. Y Is the new root.
    #        Y
    #  Z         X
    #    Yl
    def rotateLeft(self, Z):
        Y = Z.right

        Z.size = self.sizeOf(Z.left) + self.sizeOf(Y.left) + 1
        Y.size = Z.size
        Y.isRed = Z.isRed
        Z.isRed = True

        Z.right = Y.left
        Y.left = Z

        return Y

    # Right Rotation: Swap Z with YRight
    #        (Z)
    #    Y
    # X   (Yr)
    # Swap, Z with YRight
    #
    #    Y
    # X     Z
    #      Yr
    def rotateRight(self, Z):
        Y = Z.left

        Z.size  = self.sizeOf(Z.right) + self.sizeOf(Y.right) + 1
        Y.size  = Z.size
        Y.isRed = Z.isRed
        Z.isRed = Y.isRed

        Z.left  = Y.right
        Y.right = Z

        Z.isRed = True
        return Y

    def insertTo(self, root, val):
        def isRed(node):
            return node.isRed if node is not None else False

        if root is None:
            return RedBlackTree(val)

        if val < root.val:
            root.left  = self.insertTo(root.left, val)
        else:
            root.right = self.insertTo(root.right, val)

        if isRed(root.right) and not isRed(root.right.right):   # If tree is right heavy, rotate Left
            root = self.rotateLeft(root)

        if isRed(root.left) and isRed(root.left.left):          # If tree is left heavy, rotate Right
            root = self.rotateRight(root)

        if isRed(root.left) and isRed(root.right):              # If children are red, root must be black
            root.left.isRed = False
            root.right.isRed = False
            root.isRed = True

        root.size = self.sizeOf(root.left) + self.sizeOf(root.right) + 1

        return root

    def searchK(self, root, k):
        currSize = self.sizeOf(root.left) + 1
        if k == currSize:
            return root.val
        else:
            return self.searchK(root.left, k) if k < currSize else self.searchK(root.right, k - currSize )


'''
Median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle value.

For example,
[2,3,4], the median is 3

[2,3], the median is (2 + 3) / 2 = 2.5

Design a data structure that supports the following two operations:

void addNum(int num) - Add a integer number from the data stream to the data structure.
double findMedian() - Return the median of all elements so far.

Ref: https://leetcode.com/problems/find-median-from-data-stream/
'''
class MedianFinder(object):
    def __init__(self):
        self.tree = None

    def addNum(self, num):
        if self.tree is None:
            self.tree = RedBlackTree(num)
        else:
            self.tree = self.tree.insertTo(self.tree, num)
        self.tree.isRed = False

    def findMedian(self):
        curSize = self.tree.size
        if curSize %2 == 1:                                            #Or if size and 1 ( thats cool trick )
            return self.tree.searchK(self.tree, (curSize + 1) /2 )
        else:
            return self.tree.searchK(self.tree, curSize / 2) / 2.0 + self.tree.searchK(self.tree, curSize / 2 + 1) / 2.0

'''
There are two sorted arrays nums1 and nums2 of size m and n respectively.
Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).
You may assume nums1 and nums2 cannot be both empty.
Example 1:
nums1 = [1, 3]
nums2 = [2]
The median is 2.0
Ref: https://leetcode.com/problems/median-of-two-sorted-arrays
'''

class Solution(object):
    def findMedianSortedArrays(self, A, B):
        m = MedianFinder()
        [m.addNum(x) for x in A+B]
        return m.findMedian()

'''
Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Example 1:

Input: [3,2,1,5,6,4] and k = 2
Output: 5
Example 2:
'''
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        m = MedianFinder()
        [m.addNum(x) for x in nums]
        return m.tree.searchK(m.tree, len(nums)-k+1)