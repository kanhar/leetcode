"""
Given a binary tree, return the vertical order traversal of its nodes values.
For each node at position (X, Y), its left and right children respectively will be at positions (X-1, Y-1) and (X+1, Y-1).
Running a vertical line from X = -infinity to X = +infinity, whenever the vertical line touches some nodes, we report the values of the nodes in order from top to bottom (decreasing Y coordinates).
If two nodes have the same position, then the value of the node that is reported first is the value that is smaller.
Return an list of non-empty reports in order of X coordinate.  Every report will have a list of values of nodes.

Ref: https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/
"""
import collections

class Solution:
    def verticalTraversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        def solve(node):
            q = [(node, 0, 0)]
            while q:
                tmp, x, y = q.pop(0)
                if tmp:
                    res[x].append((y, tmp.val))
                    q.append((tmp.left,  x - 1, y + 1))
                    q.append((tmp.right, x + 1, y + 1))

        res = collections.defaultdict(list)
        solve(root)

        finalres = []
        for k, v in sorted(res.items()):
            finalres.append([x[1] for x in sorted(v)])

        return finalres
