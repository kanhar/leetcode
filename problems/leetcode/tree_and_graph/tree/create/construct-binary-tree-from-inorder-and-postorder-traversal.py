'''
Given inorder and postorder traversal of a tree, construct the binary tree.

Note:
You may assume that duplicates do not exist in the tree.

For example, given

inorder = [9,3,15,20,7]
postorder = [9,15,7,20,3]
Return the following binary tree:

    3
   / \
  9  20
    /  \
   15   7
   
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/   
'''
class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> TreeNode:
        def solve(ino, post):
            if ino and post:
                i = ino.index(post.pop())
                #Order here is important, r before l. Can you guess why?
                r = solve(ino[i+1:], post )
                l = solve(ino[:i], post )
                return TreeNode(ino[i], l, r)

        return solve(inorder, postorder)