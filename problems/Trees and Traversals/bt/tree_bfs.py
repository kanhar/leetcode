"""
Given a binary tree, return the level order traversal of its nodes' values.
(ie, from left to right, level by level).

Ref: https://leetcode.com/problems/binary-tree-level-order-traversal/
"""
import collections

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        q = [(root, 0)]

        res = collections.defaultdict(list)
        while q:
            tmp, d = q.pop(0)
            if tmp is None:
                continue

            res[d].append(tmp.val)
            q.append((tmp.left, d + 1))
            q.append((tmp.right, d + 1))

        return res.values()

    #Using global state
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def solve(node, d):
            if not node:
                return
            else:
                res[d].append(node.val)
                solve(node.left, d + 1)
                solve(node.right, d + 1)

        res = collections.defaultdict(list)
        solve(root, 0)
        return res.values()