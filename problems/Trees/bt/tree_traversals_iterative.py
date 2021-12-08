"""
Given a binary tree, return the inorder traversal of its nodes' values.

Example:

Input: [1,null,2,3]
   1
    \
     2
    /
   3

Output: [1,3,2]

Ref: https://leetcode.com/problems/binary-tree-inorder-traversal/
"""

class Solution:
    def inorderTraversal(self, root: TreeNode):
        def inOrder(a):
            if a is not None:
                inOrder(a.left)
                self.res.append(a.val)
                inOrder(a.right)

        def inOrderIterative(a):
            res   = []

            stack = []
            curr  = a
            while stack or curr:
                if curr:
                    stack.append(curr)
                    curr = curr.left
                else:
                    curr = stack.pop()
                    res.append(curr.val)
                    curr = curr.right
            return res

        self.res = []
        inOrder(root)
        return self.res

        return inOrderIterative(root)

"""
https://leetcode.com/problems/binary-tree-preorder-traversal/
"""
class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        if root is None:
            return []
        else:
            res = []
            stk = [root]
            while stk:
                root = stk.pop()
                res.append(root.val)
                if root.left:  stk.append(root.left)
                if root.right: stk.append(root.right)
            return res

"""
Ref: https://leetcode.com/problems/binary-tree-postorder-traversal/
"""
class Solution(object):
    def postorderTraversal(self, root):
        res = []
        stack = [(root, False)]
        while stack:
            (node, visited) = stack.pop()
            if not node:
                continue

            if visited:
                res.append(node.val)
            else:
                stack.append((node, True))
                stack.append((node.right, False))
                stack.append((node.left, False))
        return res