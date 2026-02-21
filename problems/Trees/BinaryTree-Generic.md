{: .no_toc}
# Binary Tree - Traversals

- TOC
{:toc}

### [Pre-Order](https://leetcode.com/problems/binary-tree-preorder-traversal/)

> &nbsp;1 <BR>
> 2    3 <BR>

> Pre-Order: [1,2,3]

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def preorderTraversal(self, root: TreeNode) -> List[int]:
        if root is None:
            return []
        else:
            res = []
            stk = [root]
            while stk:
                root = stk.pop()
                res.append(root.val)
                if root.left:  stk.append(root.left)
                if root.right: stk.append(root.right)
            return res
```

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:        
        def solve(node):
            if node:
                res.append(node.val)
                solve(node.left)
                solve(node.right)
        
        res = []
        solve(root)
        return res
```

</details>
<BR>


### [Post-Order](https://leetcode.com/problems/binary-tree-postorder-traversal/)

> &nbsp;1 <BR>
> 2    3 <BR>

> PostOrder: [2,3,1]

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def postorderTraversal(self, root):
        res = []
        stack = [(root, False)]
        while stack:
            (node, visited) = stack.pop()
            if not node:
                continue

            if visited:
                res.append(node.val)
            else:
                stack.append((node, True))
                stack.append((node.right, False))
                stack.append((node.left, False))
        return res
```

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def solve(node):
            if node:                
                solve(node.left)                
                solve(node.right)   
                res.append(node.val)
        res = []
        solve(root)
        return res
```
</details>
<BR>


### [In-Order](https://leetcode.com/problems/binary-tree-inorder-traversal/)

> &nbsp;1 <BR>
> 2    3 <BR>

> InOrder: [2,1,3]

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def inorderTraversal(self, root: TreeNode):
        res   = []
        stack = []
        curr  = root
        while stack or curr:
            if curr:
                stack.append(curr)
                curr = curr.left
            else:
                curr = stack.pop()
                res.append(curr.val)
                curr = curr.right
        return res
```

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def solve(node):
            if node:                
                solve(node.left)
                res.append(node.val)
                solve(node.right)        
        res = []
        solve(root)
        return res
```
</details>
<BR>

### [Sideways: Populating Next Right Pointers in Each Node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)

> Populate each next pointer to point to its next right node. 
<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def connect(self, root: 'Node') -> 'Node':
        q = [root]
        qChildren = []

        while q:
            curr = q.pop(0)
            if not curr:
                continue

            if q:
                curr.next = q[0]

            if curr.left:
                qChildren.append(curr.left)
            if curr.right:
                qChildren.append(curr.right)

            if not q and qChildren:
                q, qChildren = qChildren, q

        return root
```

</details>
<BR>

### [Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

> Given a binary tree, return the level order traversal of its nodes' values (i.e, from left to right, level by level).

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    #Using global state
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def solve(node, d):
            if not node:
                return
            else:
                res[d].append(node.val)
                solve(node.left, d + 1)
                solve(node.right, d + 1)

        res = collections.defaultdict(list)
        solve(root, 0)
        return res.values()
```

</details>
<BR>

### [DFS Traversal: Smallest string from Leaf](https://leetcode.com/problems/smallest-string-starting-from-leaf/)

> Smallest String from Leaf

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:
        def solve(node, accum=[]):
            if not node:
                return
            
            if node.left is None and node.right is None:  # i.e. if leaf
                tmp = accum + [node.val]
                tmp.reverse()              
                tmps = ''.join([chr(x + 97) for x in tmp])
                res.append(tmps)
            else:
                solve(node.left, accum + [node.val])
                solve(node.right, accum + [node.val])

        res = []
        solve(root)
        res = sorted(res)
        return res[0]
```

</details>
<BR>
