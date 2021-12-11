"""
Serialize and de-transform a generic N-ary Tree

(Can it also work for a graph?)

Ref: https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/
"""

class Codec:
    def serialize(self, root):
        def preorder(node):
            if node:
                res.append(str(node.val))
                for child in node.children:
                    preorder(child)
                res.append("#")

        res = []
        preorder(root)
        return ",".join(res)

    def deserialize(self, data):
        def preorder():
            if not arr:
                return None

            parent = Node(int(arr.pop(0)), [])

            while arr[0] != "#":
                parent.children.append(preorder())

            arr.pop(0)

            return parent

        if data:
            arr = data.split(",")
            return preorder()

class Codec:
    def serialize(self, root):
        def tuplify(root):
            if root:
                tuple = (root.val, [tuplify(x) for x in root.children])
                return tuple

        return json.dumps(tuplify(root))

    def deserialize(self, data):
        def detuplify(arr):
            if arr:
                root = Node(arr[0], [])
                for c in arr[1]:
                    root.children.append(detuplify(c))
                return root
            return None
        return detuplify(json.loads(data))