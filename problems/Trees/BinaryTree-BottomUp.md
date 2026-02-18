{: .no_toc}
# Binary Tree - Bottom Up Traversal
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



