{: .no_toc}
# Binary Tree - Top down Traversal
Practise here: [Leetcode]()

- TOC
{:toc}

### Level Order Traversal

> Given a binary tree, return the level order traversal of its nodes' values (i.e, from left to right, level by level).
> [Leetcode](https://leetcode.com/problems/binary-tree-level-order-traversal/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        q = [(root, 0)]

        res = collections.defaultdict(list)
        while q:
            tmp, d = q.pop(0)
            if tmp is None:
                continue

            res[d].append(tmp.val)
            q.append((tmp.left, d + 1))
            q.append((tmp.right, d + 1))

        return res.values()

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

### Flip Equivalent Binary Trees

> Evaluate if a binary tree X is flip equivalent to a binary tree Y - i.e. if we can make X equal
to Y after some number of flip operations. 
> [Leetcode](https://leetcode.com/problems/flip-equivalent-binary-trees/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution(object):
    def flipEquiv(self, a, b):
        if a == b == None:
            return True
        elif a is None or b is None:
            return False
        elif a.val != b.val:
            return False
        return (self.flipEquiv(a.left, b.left)  and self.flipEquiv(a.right, b.right) or
                self.flipEquiv(a.left, b.right) and self.flipEquiv(a.right, b.left))
```

</details>
<BR>

### Invert Binary Trees

> Invert a binary tree.
> [Leetcode](https://leetcode.com/problems/invert-binary-tree/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
def invertTree(root):
    if root is not None:
        return TreeNode(root.val, invertTree(root.right), invertTree(root.left))

```

</details>
<BR>

### Merge Two Binary Trees

> Given two binary trees and imagine that when you put one of them to cover the other, 
some nodes of the two trees are overlapped while the others are not. The merge rule is that if two nodes overlap, 
then sum node values up as the new value of the merged node.
> [Leetcode](https://leetcode.com/problems/merge-two-binary-trees/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def mergeTrees(self, a: TreeNode, b: TreeNode) -> TreeNode:
        if a is None and b is None:
            return
        if a is None:
            return b
        elif b is None:
            return a
        if a is not None and b is not None:
            return TreeNode(a.val + b.val, self.mergeTrees(a.left, b.left), self.mergeTrees(a.right, b.right))
```

</details>
<BR>

### Populating Next Right Pointers in Each Node

> Populate each next pointer to point to its next right node. 
> [Leetcode](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

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

### Symmetric Trees

> Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).
> [Leetcode](https://leetcode.com/problems/symmetric-tree/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def isSymmetric(self, root: TreeNode) -> bool:
        def check(a,b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            if a.val == b.val and check(a.left,b.right) and check(a.right, b.left):
                return True
            else:
                return False

        return check(root,root)
```

</details>
<BR>