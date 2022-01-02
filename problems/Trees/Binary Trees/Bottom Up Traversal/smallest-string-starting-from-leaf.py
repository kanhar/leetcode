"""
Find the lexicographically smallest string that starts at a leaf of this tree and ends at the root.

Ref: https://leetcode.com/problems/smallest-string-starting-from-leaf/
"""

class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:
        def solve(node, accum=[]):
            if node:
                if node and node.left is None and node.right is None:  # i.e. if leaf
                    res.append(''.join([chr(x + 97) for x in reversed(accum + [node.val])]))
                else:
                    solve(node.left, accum + [node.val])
                    solve(node.right, accum + [node.val])

        res = []
        solve(root)
        res = sorted(res)
        return res[0]
