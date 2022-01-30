{: .no_toc}
# Binary Tree - Generic Traversals
Practise here: [Leetcode]()

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
