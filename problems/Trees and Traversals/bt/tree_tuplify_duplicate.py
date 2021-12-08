"""
Given a binary tree, return all duplicate subtrees. For each kind of duplicate subtrees, you only need to return the root node of any one of them.

Two trees are duplicate if they have the same structure with same node values.

Example 1:

        1
       / \
      2   3
     /   / \
    4   2   4
       /
      4
The following are the two duplicate subtrees:

      2
     /
    4
and

    4
Therefore, you need to return above trees' root in the form of a list.

Ref: https://leetcode.com/problems/find-duplicate-subtrees/
"""
import collections

class Solution:
    def findDuplicateSubtrees(self, root: TreeNode) -> List[TreeNode]:
        def tuplify(root):
            if root:
                tuple = root.val, tuplify(root.left), tuplify(root.right)
                trees[tuple].append(root)
                return tuple

        trees = collections.defaultdict(list)
        tuplify(root)
        res = []
        for k,v in trees.items():
            if len(v) > 1:
                res.append(v[0])
        return res