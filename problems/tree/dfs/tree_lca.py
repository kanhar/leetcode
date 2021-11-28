"""
Given a binary Search tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
Ref: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
"""

class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is not None:
            if root.val < min(p.val, q.val):
                return self.lowestCommonAncestor(root.right, p,q)
            elif root.val > max(p.val, q.val):
                return self.lowestCommonAncestor(root.left, p,q)
            else:
                return root
"""
Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
Ref: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
"""
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        if not root:
            return None
        elif p == root or q == root:
            return root
        else:
            left  = self.lowestCommonAncestor(root.left,  p , q)
            right = self.lowestCommonAncestor(root.right, p , q)

            if left and right:
                return root
            elif not left:
                return right
            elif not right:
                return left