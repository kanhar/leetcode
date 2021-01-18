'''
Given the root of a binary tree, each node has a value from 0 to 25 representing the letters 'a' to 'z': a value of 0 represents 'a', a value of 1 represents 'b', and so on.

Find the lexicographically smallest string that starts at a leaf of this tree and ends at the root.

(As a reminder, any shorter prefix of a string is lexicographically smaller: for example, "ab" is lexicographically smaller than "aba".  A leaf of a node is a node that has no children.)

Ref: https://leetcode.com/problems/smallest-string-starting-from-leaf/
'''
class Solution:
    def smallestFromLeaf(self, root: 'TreeNode') -> 'str':
        def p(arr):
            return ''.join([chr(x+97) for x in arr])

        def solve(a, accum = []):
            if a:
                if a.left is None and a.right is None:
                    accum = [ a.val ] + accum
                    res.append(accum)
                else:
                    solve(a.left,  [ a.val ] + accum )
                    solve(a.right, [ a.val ] + accum )

        res = []
        solve(root)
        res = sorted(res)
        return p(res[0])
