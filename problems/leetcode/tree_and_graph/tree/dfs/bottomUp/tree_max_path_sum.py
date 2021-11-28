'''
Given a non-empty binary tree, find the maximum path sum.

For this problem, a path is defined as any sequence of nodes from some starting node to any node
in the tree along the parent-child connections. The path must contain at least one node and does not
need to go through the root.

Example 1:

Input: [1,2,3]

       -10
      / \
     9    20
        15   7

Output: 42
Ref: https://leetcode.com/problems/binary-tree-maximum-path-sum/
'''


class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def solve(node):
            if not node:
                return 0
            else:
                left = max(solve(node.left), 0)
                right = max(solve(node.right), 0)

                self.res = max(self.res, left + right + node.val)
                return max(left, right) + node.val

        self.res = float('-inf')
        solve(root)
        return self.res
