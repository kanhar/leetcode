'''
Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).

Ref: https://leetcode.com/problems/binary-tree-level-order-traversal/
'''

class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        h = [(root, 0)]
        res = collections.defaultdict(list)
        while h:
            (curr, d) = h.pop(0)
            if curr:
                res[d].append(curr.val)
                h.append((curr.left, d + 1))
                h.append((curr.right, d + 1))

        return [x for x in res.values()]

    #Using global state
    def levelOrderGlobal(self, root: TreeNode) -> List[List[int]]:
        def solve(root, d=0):
            if root:
                res[d].append(root.val)
                solve(root.left, d + 1)
                solve(root.right, d + 1)

        res = collections.defaultdict(list)
        solve(root)
        return res.values()