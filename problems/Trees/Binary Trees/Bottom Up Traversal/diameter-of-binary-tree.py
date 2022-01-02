"""
Diameter

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