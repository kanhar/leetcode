"""
Given a binary tree, you need to compute the length of the bottomUp of the tree.
The bottomUp of a binary tree is the length of the longest path between any two nodes in a tree.
This path may or may not pass through the root.

Example:
Given a binary tree
          1
         / \
        2   3
       / \
      4   5
Return 3, which is the length of the path [4,2,1,3] or [5,2,1,3].

https://leetcode.com/problems/diameter-of-binary-tree/
"""

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode, max_d=0) -> int:
        def solve(root):
            if root is None:
                return 0
            else:
                left  = solve(root.left)
                right = solve(root.right)
                self.res = max(self.res, left + right)      # Calculates Diameter
                return max(left, right) + 1                 # Calculates Depth
        self.res = 0
        solve(root)
        return self.res

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode, max_d=0) -> int:
        def depth(root):
            if root is None:
                return 0

            return max(depth(root.left), depth(root.right)) + 1

        def diam_at(root):
            if root is None:
                return 0

            return depth(root.left) + depth(root.right)

        if root is None:
            return 0

        return max(max_d, diam_at(root), self.diameterOfBinaryTree(root.left), self.diameterOfBinaryTree(root.right))