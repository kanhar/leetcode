"""
In a binary tree, the root node is at depth 0, and children of each depth k node are at depth k+1.

Two nodes of a binary tree are cousins if they have the same depth, but have different parents.

We are given the root of a binary tree with unique values, and the values x and y of two different nodes in the tree.

Return true if and only if the nodes corresponding to the values x and y are cousins.

Example 1:

Input: root = [1,2,3,4], x = 4, y = 3
Output: false
Ref: https://leetcode.com/problems/cousins-in-binary-tree/
"""
class Solution(object):
    def isCousins(self, root, x, y):
        def getDepth(root, num, d=0):
            if root is None:
                return -1
            if root.val == num:
                return d
            else:
                return max( getDepth(root.left, num,d+1),  getDepth(root.right, num,d+1) )

        def getParent(root, num, parent = None):
            if root is None:
                return None
            else:
                if root.val == num:
                    return parent
                else:
                    return getParent(root.left, num, root) or getParent(root.right, num, root)

        dx = getDepth(root,x)
        dy = getDepth(root,y)

        px = getParent(root,x)
        py = getParent(root,y)

        if dx==dy and px!=py:
            return True
        else:
            return False
