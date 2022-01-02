"""
Given a non-empty binary tree, find the maximum path sum.

Ref: https://leetcode.com/problems/binary-tree-maximum-path-sum/
"""

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def solve(node):
            if not node:
                return 0
            else:
                ls = solve(node.left)
                rs = solve(node.right)

                ls = max(ls, 0)
                rs = max(rs, 0)

                self.maxSum = max(self.maxSum, node.val + ls + rs)

                return max(ls, rs) + node.val

        self.maxSum = float('-inf')
        solve(root)
        return self.maxSum


