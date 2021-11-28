'''
You are given a perfect binary tree where all leaves are on the same level, and every parent has two children.

Populate each next pointer to point to its next right node. If there is no next right node,
the next pointer should be set to NULL. Initially, all next pointers are set to NULL.

Ref: https://leetcode.com/problems/binary-tree-level-order-traversal/
'''

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        if not root:
            return None

        if root.right:
            root.left.next = root.right
            if root.next:
                root.right.next = root.next.left

        self.connect(root.left)
        self.connect(root.right)

        return root