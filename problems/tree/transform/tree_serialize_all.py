"""
Serialize and de-transform any generic Binary Tree

Ref: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
"""

class Codec:
    def serialize(self, root):
        def preorderSimple(node):
            if not node:
                return "EMPTY_NODE"
            else:
                return str(node.val) + ',' + preorderSimple(node.left) + ',' + preorderSimple(node.right)

        def preorder(node):
            if node:
                vals.append(str(node.val))
                preorder(node.left)
                preorder(node.right)
            else:
                vals.append('EMPTY_NODE')

        # Option A: Hard to control this, say if you didn't want to print "EMPTY_NODE"
        return preorderSimple(root)

        # Option B: Easier to control this, if you don't want to print "EMPTY_NODE" as required in BST serialization
        vals = []
        preorder(root)
        return ','.join(vals)

    def deserialize(self, data):
        def solve(l):
            if l:
                tmp = l.pop(0)
                if tmp == 'EMPTY_NODE':
                    return None
                else:
                    return TreeNode(tmp, solve(l), solve(l))

        arr = data.split(',')
        return solve(arr)