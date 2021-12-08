"""
Given an n-ary tree, return the level order traversal of its nodes' values.

Nary-Tree input serialization is represented in their level order traversal,
each group of children is separated by the null value (See examples).

Ref: https://leetcode.com/problems/n-ary-tree-level-order-traversal/
"""
import collections

class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        def solve(node, d):
            if not node:
                return
            else:
                if d == 0:
                    res[d].append(node.val)
                    d += 1

                for child in node.children:
                    res[d].append(child.val)
                    solve(child, d + 1)

        res = collections.defaultdict(list)
        solve(root, 0)
        return res.values()