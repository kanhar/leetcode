"""
Serialize and de-transform any generic Binary Tree

Ref: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/

Intuition: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/discuss/74430/tuplify-json-python/77502
"""

import collections
import json

class Codec:
    def serialize(self, root):
        def tuplify(root):
            if root:
                tuple = root.val, tuplify(root.left), tuplify(root.right)
                trees[tuple].append(root)
                return tuple

        trees = collections.defaultdict(list)
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