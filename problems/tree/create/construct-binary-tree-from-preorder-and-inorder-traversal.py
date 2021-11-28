"""
Given preorder and inorder traversal of a tree, construct the binary tree. No duplicates.

For example, given:
inorder = [9,3,15,20,7]
preorder = [3,9,20,15,7]
Return the following binary tree:

    3
   / \
  9  20
    /  \
   15   7
Ref: #https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
"""

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> TreeNode:
        def solve(ino, pre):
            if ino and pre:
                i = ino.index(pre.pop(0))
                #Order here is important, l before r.
                # Because we are reading from front of postorder sort, Left, Root, Right
                # Hence Left needs to be done first.
                l = solve(ino[:i], pre )
                r = solve(ino[i+1:], pre )
                return TreeNode( ino[i], l, r  )

        return solve(inorder, preorder)
