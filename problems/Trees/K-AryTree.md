{: .no_toc}
# K-Ary Trees
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9db7pr2r)

- TOC
{:toc}

### [Tree Serialize N-Ary](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/) <BR>

> Given an integer array nums where the elements are sorted in ascending order,
convert it to a height-balanced binary search tree.
> (Can it also work for a graph?)
<details><summary markdown="span">Let's see some code!</summary>

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

### [Tree Traversal n-Ary](https://leetcode.com/problems/n-ary-tree-level-order-traversal/) <BR>

> Given an n-ary tree, return the level order traversal of its nodes' values..
<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        def solve(node, d):
            if not node:
                return
            else:
                if d == 0:
                    res[d].append(node.val)
                    d += 1

                for child in node.children:
                    res[d].append(child.val)
                    solve(child, d + 1)

        res = collections.defaultdict(list)
        solve(root, 0)
        return res.values()
```

</details>
<BR>
