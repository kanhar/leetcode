"""
Invert a binary tree.

Example:

Input:

     4
   /   \
  2     7
 / \   / \
1   3 6   9
Output:

     4
   /   \
  7     2
 / \   / \
9   6 3   1
Ref: #https://leetcode.com/problems/invert-binary-tree/
"""

def invertTree(root):
    if root is not None:
        return TreeNode(root.val, invertTree(root.right), invertTree(root.left))
