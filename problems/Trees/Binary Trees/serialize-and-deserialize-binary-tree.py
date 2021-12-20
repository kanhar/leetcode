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


import collections
import json

class Codec:
    def serialize(self, root):
        def tuplify(root):
            if root:
                tuple = root.val, tuplify(root.left), tuplify(root.right)
                return tuple

        res = tuplify(root)
        return json.dumps(res)

    def deserialize(self, data):
        def detuplify(arr):
            if arr:
                root = TreeNode(arr[0])
                root.left = detuplify(arr[1])
                root.right = detuplify(arr[2])
                return root
        return detuplify(json.loads(data))