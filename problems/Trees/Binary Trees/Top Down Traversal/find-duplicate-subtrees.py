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
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        def tuplify(node):
            if node:
                tuple = (node.val, tuplify(node.left), tuplify(node.right))
                res[tuple].append(node)
                return tuple

        res = collections.defaultdict(list)
        tuplify(root)

        # Minor detail: v[0] cause any one parent node needs to be returned
        dupes = {k: v[0] for (k, v) in res.items() if len(v) > 1}
        return dupes.values()