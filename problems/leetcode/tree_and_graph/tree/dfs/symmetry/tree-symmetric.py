'''
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

'''

class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        def check(a,b):
            if a is None and b is None:
                return True
            if None in [a, b] or a.val != b.val:
                return False
            else:
                return check(a.left,b.right) and check(a.right, b.left)

        return check(root,root)

