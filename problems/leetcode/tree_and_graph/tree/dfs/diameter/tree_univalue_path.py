'''
Given a binary tree, find the length of the longest path where each node in the path has the same value. This path may or may not pass through the root.

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
class Solution(object):
    def longestUnivaluePath(self, root):

        def solve(root, parent_val = None):
            if root is None:
                return 0
            else:
                left  = solve(root.left, root.val)
                right = solve(root.right, root.val)
                self.res = max(self.res, left + right)

                return max(left, right) + 1 if root.val == parent_val else 0

        self.res = 0
        solve(root)
        return self.res
