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
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def tuplify(node):
            if node:
                return (node.val, tuplify(node.left), tuplify(node.right))
                
        if not root:
            return False
        
        if tuplify(root) == tuplify(subRoot):
            return True
        
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

</details>
<BR>

### [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

> Serialize and de-transform any generic Binary Tree

<details><summary markdown="span">Execute!</summary>

```python
import collections
import json
class Codec:
    def serialize(self, root):
        def tuplify(node):
            if node:
                return (node.val, tuplify(node.left), tuplify(node.right))

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
        def tuplify(root):
            if root:
                return (root.val, [tuplify(x) for x in root.children])

        return json.dumps(tuplify(root))

    def deserialize(self, data):
        def detuplify(arr):
            if arr:
                root = Node(arr[0], [])
                for c in arr[1]:
                    root.children.append(detuplify(c))
                return root
                
        return detuplify(json.loads(data))
```

</details>
<BR>

