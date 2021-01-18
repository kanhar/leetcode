'''
Given preorder and inorder traversal of a tree, construct the binary tree.

Note:
You may assume that duplicates do not exist in the tree.

For example, given

preorder = [3,9,20,15,7]
inorder = [9,3,15,20,7]
Return the following binary tree:

    3
   / \
  9  20
    /  \
   15   7

Ref: #https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
'''

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        def solve(ino, pre):
            if ino and pre:
                i = ino.index(pre.pop(0))
                l = solve(ino[:i], pre )
                r = solve(ino[i+1:], pre )
                return TreeNode( ino[i], l, r  )

        return solve(inorder, preorder)
