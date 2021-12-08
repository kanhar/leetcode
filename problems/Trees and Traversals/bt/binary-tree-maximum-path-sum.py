"""
Given a non-empty binary tree, find the maximum path sum.

For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the parent-child connections. The path must contain at least one node and does not need to go through the root.

Example 1:

Input: [1,2,3]

       1
      / \
     2   3

Output: 6
Ref: https://leetcode.com/problems/binary-tree-maximum-path-sum/
"""

class Solution(object):
    def maxPathSum(self, root):

        def get_sum(root):
            if root is None:
                return 0
            else:
                ls = max(get_sum(root.left), 0)
                rs = max(get_sum(root.right), 0)

                self.max = max(self.max, ls + rs + root.val)
                return max(ls, rs) + root.val

        self.max = float('-inf')
        get_sum(root)
        return self.max
