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

### [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) 

> Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values with a subtree of s.
<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def isSubtree(self, s, t):
        def check(a, b):
            if a == b == None:
                return True
            elif None in [a, b] or a.val != b.val:
                return False
            else:
                return check(a.left, b.left) and check(a.right, b.right)

        #s >> t
        def checkAll(s, t):
            if not s:
                return False
            elif check(s, t):
                return True
            else:
                return dfs(s.left, t) or dfs(s.right, t)

        return checkAll(s, t)
```

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