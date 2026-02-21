{: .no_toc}
# Binary Trees

![Alt text](https://github.com/kanhar/leetcode/blob/main/IMG_20260221_060619.png)

Practise here: [Leetcode]()

- TOC
{:toc}

### [Path with Maximum sum](https://leetcode.com/problems/binary-tree-maximum-path-sum/)

> Given a non-empty binary tree, find the maximum path sum

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def solve(node):
            if not node:
                return 0
            else:
                ls = solve(node.left)
                rs = solve(node.right)

                ls = max(ls, 0)
                rs = max(rs, 0)

                self.maxSum = max(self.maxSum, node.val + ls + rs)

                return max(ls, rs) + node.val

        self.maxSum = float('-inf')
        solve(root)
        return self.maxSum

```

</details>
<BR>

### [Tree Diameter](https://leetcode.com/problems/diameter-of-binary-tree/)

> Calculate Tree Diameter

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode, max_d=0) -> int:
        def solve(root):
            if root is None:
                return 0
            else:
                ls = solve(root.left)
                rs = solve(root.right)
                
                self.res = max(self.res, ls + rs)      # Calculates Diameter
                return max(ls, rs) + 1                 # Calculates Depth
        self.res = 0
        solve(root)
        return self.res
```

</details>
<BR>

### [Number of Paths having Sum](https://leetcode.com/problems/path-sum-iii/)

> Given a binary tree in which each node contains an integer value. Find the number of paths that sum to a given value.
> [See also](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def pathSum(self, root: TreeNode, target: int) -> int:
        def find_paths(root, target):
            if not root:
                return 0

            return int(root.val == target) + find_paths(root.left, target-root.val) + find_paths(root.right, target-root.val)

        if not root:
            return 0

        return find_paths(root, target) + self.pathSum(root.left, target) + self.pathSum(root.right, target)
```

</details>
<BR>

### [Smallest string from Leaf](https://leetcode.com/problems/smallest-string-starting-from-leaf/)

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

### [Check if tree is Height Balanced](https://leetcode.com/problems/balanced-binary-tree/) 

> Given a binary tree, determine if it is height-balanced - left and right subtrees of every node differ in height by no more than 1.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def depth(node):
            if not node:
                return 0
            else:
                ls = depth(node.left)
                rs = depth(node.right)

                if abs(ls - rs) > 1:
                    self.isBalanced = False

                return 1 + max(ls, rs)

        self.isBalanced = True
        depth(root)
        return self.isBalanced
```

</details>
<BR>

### [Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

> Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def lowestCommonAncestor(self, root, p, q):
        if not root:
            return None
        elif p == root or q == root:
            return root
        else:
            left  = self.lowestCommonAncestor(root.left,  p , q)
            right = self.lowestCommonAncestor(root.right, p , q)

            if left and right:
                return root
            elif not left:
                return right
            elif not right:
                return left
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

### [Flip Equivalent Binary Trees](https://leetcode.com/problems/flip-equivalent-binary-trees/)

> Evaluate if a binary tree X is flip equivalent to a binary tree Y - i.e. if we can make X equal
to Y after some number of flip operations. 

<details><summary markdown="span">Execute!</summary>

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

### [Invert Binary Trees](https://leetcode.com/problems/invert-binary-tree/)

> Invert a binary tree.

<details><summary markdown="span">Execute!</summary>

```python
def invertTree(root):
    if root is not None:
        return TreeNode(root.val, 
                        invertTree(root.right), 
                        invertTree(root.left))

```

</details>
<BR>

### [Merge Two Binary Trees](https://leetcode.com/problems/merge-two-binary-trees/)

> Given two binary trees and imagine that when you put one of them to cover the other, 
some nodes of the two trees are overlapped while the others are not. The merge rule is that if two nodes overlap, 
then sum node values up as the new value of the merged node.

<details><summary markdown="span">Execute!</summary>

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

### [Populating Next Right Pointers in Each Node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)

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

### [Symmetric Trees](https://leetcode.com/problems/symmetric-tree/)

> Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).

<details><summary markdown="span">Execute!</summary>

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

