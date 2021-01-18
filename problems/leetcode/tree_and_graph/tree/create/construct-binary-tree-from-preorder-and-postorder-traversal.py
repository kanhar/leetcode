'''
Return any binary tree that matches the given preorder and postorder traversals.

Values in the traversals pre and post are distinct positive integers.

Ref: #https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
'''

class Solution(object):
    def constructFromPrePost(self, pre, post):
        if not pre:
            return None

        root = TreeNode(pre[0])
        if len(pre) == 1:
            return root
        else:
            P = post.index(pre[1])
            root.left  = self.constructFromPrePost(pre[1:P+2], post[:P+1])
            root.right = self.constructFromPrePost(pre[P+2:], post[P+1:-1])
            return root