"""
Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).

For example, this binary tree [1,2,2,3,4,4,3] is symmetric:

    1
   / \
  2   2
 / \ / \
3  4 4  3
 

But the following [1,2,2,null,3,null,3] is not:

    1
   / \
  2   2
   \   \
   3    3
   
https://leetcode.com/problems/symmetric-tree/
"""

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        def check(a,b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            if a.val == b.val and check(a.left,b.right) and check(a.right, b.left):
                return True
            else:
                return False

        return check(root,root)

