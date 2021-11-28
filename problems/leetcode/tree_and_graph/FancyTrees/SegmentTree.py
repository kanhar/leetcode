'''
Given an integer array nums, find the sum of the elements between indices i and j (i ≤ j), inclusive.

The update(i, val) function modifies nums by updating the element at index i to val.

Example:

Given nums = [1, 3, 5]

sumRange(0, 2) -> 9
update(1, 2)
sumRange(0, 2) -> 8
'''

#Segment tree node
class Node(object):
    def __init__(self, start, end):
        self.left  = None
        self.right = None

        self.start = start
        self.end = end
        self.total = 0

class NumArray(object):
    def __init__(self, nums):
        def createTree(nums, l, r):
            if l <=r:
                if l == r:  #leaf node
                    n = Node(l, r)
                    n.total = nums[l]
                    return n
                else:
                    mid = (l + r) // 2
                    root = Node(l, r)
                    root.left = createTree(nums, l, mid)
                    root.right = createTree(nums, mid+1, r)
                    root.total = root.left.total + root.right.total #Total stores the sum of all leaves under root i.e. between (start, end)
                    return root

        self.root = createTree(nums, 0, len(nums)-1)

    def update(self, i, val):
        def updateVal(root, i, val):
            if root.start == root.end:                          #Base case. The actual value will be updated in a leaf.
                root.total = val
                return val
            mid = (root.start + root.end) // 2
            if i <= mid:
                updateVal(root.left, i, val)
            else:
                updateVal(root.right, i, val)
            root.total = root.left.total + root.right.total     #Propogate the changes after recursive call returns
            return root.total

        return updateVal(self.root, i, val)

    def sumRange(self, i, j):
        def rangeSum(root, i, j):
            if root.start == i and root.end == j:
                return root.total

            mid = (root.start + root.end) // 2
            if j <= mid:
                return rangeSum(root.left, i, j)
            elif i >= mid + 1:
                return rangeSum(root.right, i, j)
            else:
                return rangeSum(root.left, i, mid) + rangeSum(root.right, mid+1, j)

        return rangeSum(self.root, i, j)

