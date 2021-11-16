'''
Serialize and de-serialize a generic Binary Search Tree

Ref: https://leetcode.com/problems/serialize-and-deserialize-bst/
'''

class Codec:
    def serialize(self, root):
        def preorder(node):
            if node:
                vals.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
            else:
                vals.append(None)

        vals = []
        preorder(root)
        return ','.join(x for x in vals if x)

    def deserialize(self, data):
        def solve(ino, pre):
            if ino and pre:
                mid = ino.index(pre.pop(0))
                return TreeNode(ino[mid], solve(ino[:mid], pre), solve(ino[mid + 1:], pre))

        if data == '':
            return None
        else:
            preorder = [int(x) for x in data.split(',')]
            inorder = sorted(preorder)
            return solve(inorder, preorder)