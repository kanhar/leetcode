'''
Given a binary tree, find the length of the longest path where each node in the path has the same value.
This path may or may not pass through the root.

The length of path between two nodes is represented by the number of edges between them.

Example 1:

Input:

              5
             / \
            4   5
           / \   \
          1   1   5
Ref: https://leetcode.com/problems/longest-univalue-path/
'''
class Solution:
    def longestUnivaluePath(self, root: Optional[TreeNode]) -> int:
        def solve(node, parent=None):
            if not node:
                return 0
            else:
                right = solve(node.right, parent=node.val)
                left = solve(node.left, parent=node.val)

                self.res = max(self.res, left + right)

                if node.val == parent:
                    return max(left, right) + 1
                else:
                    return 0

        self.res = 0
        solve(root)
        return self.res

