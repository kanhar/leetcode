'''
Given a binary tree, return the vertical order traversal of its nodes values.
For each node at position (X, Y), its left and right children respectively will be at positions (X-1, Y-1) and (X+1, Y-1).
Running a vertical line from X = -infinity to X = +infinity, whenever the vertical line touches some nodes, we report the values of the nodes in order from top to bottom (decreasing Y coordinates).
If two nodes have the same position, then the value of the node that is reported first is the value that is smaller.
Return an list of non-empty reports in order of X coordinate.  Every report will have a list of values of nodes.

Ref: https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/
'''

class Solution:
    def verticalTraversal(self, root: TreeNode) -> List[List[int]]:
        mapping = collections.defaultdict(lambda: collections.defaultdict(list))
        self.dfs(root, 0, 0, mapping)

        res = []
        for x in sorted(mapping):
            tmp = []
            for y in sorted(mapping[x]):
                tmp += sorted(mapping[x][y])
            res.append(tmp)
        return res

    def dfs(self, node, x, y, mapping):
        if not node:
            return

        mapping[x][y].append(node.val)
        self.dfs(node.left, x-1, y+1, mapping)
        self.dfs(node.right, x+1, y+1, mapping)