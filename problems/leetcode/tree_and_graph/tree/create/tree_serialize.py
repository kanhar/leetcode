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
        vals = []
        preorder(root)
        return ','.join(vals)

    def deserialize(self, data):
        def solve(ino, pre):
            if ino and pre:
                mid = ino.index(pre.pop(0))
                return TreeNode( ino[mid], solve(ino[:mid], pre ), solve(ino[mid+1:], pre )  )

        if data == '':
            return None
        else:
            preorder = [int(x) for x in data.split(',')]
            inorder = sorted(preorder)
            return solve(inorder, preorder)

'''
Serialize and de-serialize a generic Binary Tree
'''

class Codec:
    def serialize(self, root):
        if not root:
            return ""
        else:
            return str(root.val) + ',' + self.serialize(root.left) + ',' + self.serialize(root.right)

    def deserialize(self, data):
        def solve(l):
            if len(l) > 0:
                tmp = l.pop(0)
                if tmp == '':
                    return None
                else:
                    return TreeNode(tmp, solve(l), solve(l))

        return solve(data.split(','))
