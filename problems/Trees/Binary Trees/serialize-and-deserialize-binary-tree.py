"""
Serialize and de-transform any generic Binary Tree

Ref: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
"""

class Codec:
    def serialize(self, root):
        if root is None:
            return 'None'
        else:
            return str(root.val) + "," + self.serialize(root.left) + "," + self.serialize(root.right)

    def deserialize(self, data):
        def solve(l):
            if l:
                tmp = l.pop(0)
                if tmp == 'None':
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