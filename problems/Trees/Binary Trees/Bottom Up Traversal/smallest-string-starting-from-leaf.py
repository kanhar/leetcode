"""
Given the root of a binary tree, each node has a value from 0 to 25 representing the letters 'a' to 'z': a value of 0 represents 'a', a value of 1 represents 'b', and so on.

Find the lexicographically smallest string that starts at a leaf of this tree and ends at the root.

(As a reminder, any shorter prefix of a string is lexicographically smaller: for example, "ab" is lexicographically smaller than "aba".  A leaf of a node is a node that has no children.)

Ref: https://leetcode.com/problems/smallest-string-starting-from-leaf/
"""

class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:
        def solve(node, accum=[]):
            if not node:
                return

            if node and node.left is None and node.right is None:  # i.e. if leaf
                res.append(''.join([chr(x + 97) for x in reversed(accum + [node.val])]))
            else:
                solve(node.left, accum + [node.val])
                solve(node.right, accum + [node.val])

        res = []
        solve(root)
        res = sorted(res)
        return res[0]
