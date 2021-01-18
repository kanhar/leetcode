'''
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
'''

class Solution:
    def isBalanced(self, t: TreeNode) -> bool:
        def depth(t):
            return 0 if t == None else max(depth(t.left), depth(t.right))+1

        if t == None:
            return True
        elif abs(depth(t.left)-depth( t.right)) > 1:
            return False
        else:
            return self.isBalanced(t.left) and self.isBalanced( t.right)
