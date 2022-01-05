{: .no_toc}
# Binary Tree - Generic Traversals
Practise here: [Leetcode]()

- TOC
{:toc}

### [Pre-Order](https://leetcode.com/problems/binary-tree-preorder-traversal/)

> Pre-Order Traversal - Iterative and Recursive

<details><summary markdown="span">Let's see some code!</summary>

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

</details>
<BR>

### [In-Order](https://leetcode.com/problems/binary-tree-inorder-traversal/)

> Pre-Order Traversal - Iterative and Recursive

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def inorderTraversal(self, root: TreeNode):
        def inOrder(a):
            if a is not None:
                inOrder(a.left)
                self.res.append(a.val)
                inOrder(a.right)

        def inOrderIterative(a):
            res   = []

            stack = []
            curr  = a
            while stack or curr:
                if curr:
                    stack.append(curr)
                    curr = curr.left
                else:
                    curr = stack.pop()
                    res.append(curr.val)
                    curr = curr.right
            return res

        self.res = []
        inOrder(root)
        return self.res

        return inOrderIterative(root)
```

</details>
<BR>

### [Post-Order](https://leetcode.com/problems/binary-tree-postorder-traversal/)

> Post-Order Traversal - Iterative and Recursive

<details><summary markdown="span">Let's see some code!</summary>

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

</details>
<BR>
