"""
Given two integer arrays, preorder and postorder where preorder is the preorder traversal of a binary
tree of distinct values and postorder is the postorder traversal of the same tree.

If there exist multiple answers, you can return any of them.

preorder = [3,9,20,15,7]
postorder = [9,15,7,20,3]
Return the following binary tree:

    3
   / \
  9  20
    /  \
   15   7

Ref: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-postorder-traversal/
"""

class Solution(object):
    def constructFromPrePost(self, pre, post):
        if len(pre) == 0:
            return None

        root = TreeNode(pre[0])
        if len(pre) == 1:
            return root
        else:
            P = post.index(pre[1])
            root.left  = self.constructFromPrePost(pre[1:P+2], post[:P+1])
            root.right = self.constructFromPrePost(pre[P+2:], post[P+1:-1])
            return root