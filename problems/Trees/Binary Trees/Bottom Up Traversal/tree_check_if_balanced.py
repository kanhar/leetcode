"""
Given a binary tree, determine if it is height-balanced.
For this problem, a height-balanced binary tree is defined as:
a binary tree in which the left and right subtrees of every node differ in height by no more than 1.

Example 1:

Given the following tree [3,9,20,null,null,15,7]:

    3
   / \
  9  20
    /  \
   15   7
Return true.

Ref: https://leetcode.com/problems/balanced-binary-tree/
"""

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def depth(node):
            if not node:
                return 0
            else:
                ls = depth(node.left)
                rs = depth(node.right)

                if abs(ls - rs) > 1:
                    self.isBalanced = False

                return 1 + max(ls, rs)

        self.isBalanced = True
        depth(root)
        return self.isBalanced

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def depth(node):
            if not node:
                return 0
            else:
                return max(depth(node.left), depth(node.right)) + 1

        def isBalanced(node):
            if not node:
                return True
            elif abs(depth(node.left) - depth(node.right)) > 1:
                return False
            else:
                return isBalanced(node.left) and isBalanced(node.right)

        return isBalanced(root)