'''
You are given an integer array nums and you have to return a new counts array. The counts array has the property where counts[i] is the number of smaller elements to the right of nums[i].

Example:

Input: [5,2,6,1]
Output: [2,1,1,0]
Explanation:
To the right of 5 there are 2 smaller elements (2 and 1).
To the right of 2 there is only 1 smaller element (1).
To the right of 6 there is 1 smaller element (1).
To the right of 1 there is 0 smaller element.
'''

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        self.rank = 0

class RankTree(object):
    def __init__(self):
        self.root = None

    def insert(self, val):
        def _insert(root, val):
            if not root:
                return TreeNode(val)
            if val <= root.val:
                root.left = _insert(root.left, val)
                root.rank += 1
            if val > root.val:
                root.right = _insert(root.right, val)
            return root
        self.root = _insert(self.root, val)

    def get_rank(self, val):
        def _get_rank(root, val):
            if not root:
                return 0
            if val <= root.val:
                return _get_rank(root.left, val)
            else:
                return 1 + root.rank + _get_rank(root.right, val)
        return _get_rank(self.root, val)

class Solution(object):
    def countSmaller(self, nums):
        res = []
        r = RankTree()
        for elem in nums[::-1]:
            r.insert(elem)
            res.insert(0, r.get_rank(elem))
        return res