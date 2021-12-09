"""
Given inorder and postorder traversal of a tree, construct the binary tree. No duplicates in tree.
For example, given:
inorder = [9,3,15,20,7]
postorder = [9,15,7,20,3]
Return the following binary tree:

    3
   / \
  9  20
    /  \
   15   7
   
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/
"""
class Solution:
    def buildTree(self, ino: List[int], pos: List[int]) -> Optional[TreeNode]:
        if ino and pos:
            root = pos.pop()
            idx  = ino.index(root)
            # Order here is important, r before l.
            # Because we are reading from back of postorder sort, Left, Root, Right
            # Hence Right needs to be done first.
            r = self.buildTree(ino[idx+1:], pos)
            l = self.buildTree(ino[:idx], pos)
            return TreeNode(root,l, r)