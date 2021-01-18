'''
Given a binary tree, return the level order traversal of its nodes' values. (ie, from left to right, level by level).

Ref: https://leetcode.com/problems/binary-tree-level-order-traversal/
'''

class Solution:
    def levelOrder(self, root: TreeNode) -> List[List[int]]:
        res = collections.defaultdict(list)
        ds = [(1, root)]
        while ds:
            (level, node) = ds.pop(0)
            if node:
                res[level].append(node.val)
                ds.append( (level+1, node.left))
                ds.append( (level+1, node.right))

        return [ x for x in res.values()]

    def levelOrderRecursive(self, root: TreeNode) -> List[List[int]]:
        def tree_to_list(tree, lists=collections.defaultdict(list), d=1):
            if tree is not None:
                lists[d].append(tree.val)
                lists = tree_to_list(tree.left,  lists, d+1)
                lists = tree_to_list(tree.right, lists, d+1)
            return lists
        x = tree_to_list(root)
        return x.values()

    #Using global state
    def levelOrderGlobal(self, root: TreeNode) -> List[List[int]]:
        def solve(root, d= 0):
            if root is not None:
                self.res[d].append(root.val)
                solve(root.left, d+1)
                solve(root.right, d+1)
        self.res = collections.defaultdict(list)
        solve(root)
        return self.res.values()
