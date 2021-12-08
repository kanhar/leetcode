"""
Given a binary search tree and a node in it, find the in-order successor of that node in the BST.
The successor of a node p is the node with the smallest key greater than p.val.
Example 1:
Input: root = [2,1,3], p = 1
Output: 2
Explanation: 1's in-order successor node is 2. Note that both p and the return value is of TreeNode type.

Ref: https://leetcode.com/problems/inorder-successor-in-bst/
"""
class Solution:
    def inorderSuccessor(self, root, p):
        if not root:
            return None
        if p.val < root.val:
            return self.inorderSuccessor(root.left,p) or root       #cause the successor will be by definition one up
        else:
            return self.inorderSuccessor(root.right,p)              #cause the successor will always be down. No need to go up here.
