{: .no_toc}
# Binary Trees - Tuplify Method
Practise here: [Leetcode]()

- TOC
{:toc}

### [Find Duplicate Subtrees](https://leetcode.com/problems/find-duplicate-subtrees/) 

> Given a binary tree, return the roots of all duplicate subtrees. 

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        def tuplify(node):
            if node:
                tuple = (node.val, tuplify(node.left), tuplify(node.right))
                res[tuple].append(node)
                return tuple

        res = collections.defaultdict(list)
        tuplify(root)

        # Minor detail: v[0] cause any one parent node needs to be returned
        dupes = {k: v[0] for (k, v) in res.items() if len(v) > 1}
        return dupes.values()
```

</details>
<BR>


### [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) 

> Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values with a subtree of s.
<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def isSubtree(self, s, t):
        def tuplify(root, updateCache):
            if root:
                tuple = (root.val, tuplify(root.left, updateCache), tuplify(root.right, updateCache))
                if updateCache:
                    self.res[tuple].append(root)
                return tuple

        self.res = collections.defaultdict(list)
        tuplify(s, updateCache = True)
        return tuplify(t, updateCache = False) in self.res

```

</details>
<BR>

### [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

> Serialize and de-transform any generic Binary Tree

<details><summary markdown="span">Execute!</summary>

```python
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
```

</details>
<BR>


### [Serialize and Deserialize N-ary Tree](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/) <BR>

> Given an integer array nums where the elements are sorted in ascending order,
convert it to a height-balanced binary search tree.
> (Can it also work for a graph?)
<details><summary markdown="span">Execute!</summary>

```python
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
```

</details>
<BR>

