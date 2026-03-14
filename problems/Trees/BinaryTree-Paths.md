{: .no_toc}
# Binary Trees

![Alt text](../../IMG_20260221_060619.png)

Key intuition here: In every one of these examples, the "Root" is a manager waiting for reports from the "Left Child" and "Right Child" before it can finish its own job.

The "Tell": The Wait for Reports - Notice the pattern in every snippet:

```
ls = solve(node.left)
rs = solve(node.right)
```

The Decision: Only after these two lines do you see the logic that updates a global variable (like self.res or self.maxSum) or calculates a return value.

Why these MUST be Post-order: 

* Max Depth / Balanced Tree: You can't possibly know your own height until you know the height of your tallest child. You have to wait for the numbers to "bubble up."
* Diameter / Max Path Sum: These are "Bridge" problems. You need to know the longest "arms" coming from the left and right to see if their sum creates a new global record at the current node.
* LCA: A node only knows it is the "Lowest Common Ancestor" if it receives a "Found Target" signal from both subtrees.


- TOC
{:toc}

### [Max Depth of a Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)

> Max depth of a binary Tree

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def depth(node):
            if not node:
                return 0
            else:
                ls = depth(node.left)
                rs = depth(node.right)

                return max(ls,rs) + 1
        return depth(root)
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

                # If this node was the highest point of a path, how long would that path be (diameter)
                self.res = max(self.res, ls + rs)

                # Calculates Depth
                return max(ls, rs) + 1                 
        self.res = 0
        solve(root)
        return self.res
```

</details>
<BR>

### [Longest Univalue path](https://leetcode.com/problems/longest-univalue-path/)

> Longest Univalue path

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def longestUnivaluePath(self, root: Optional[TreeNode]) -> int:
        def solve(node):
            if not node:
                return 0

            ls = solve(node.left)
            rs = solve(node.right)

            ls = ls + 1 if node.left and node.left.val == node.val else 0
            rs = rs + 1 if node.right and node.right.val == node.val else 0

            self.maxpath = max(self.maxpath, ls + rs)

            return max(ls, rs)
        self.maxpath = 0      
        solve(root)
        return self.maxpath
```

</details>
<BR>

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
                l = max(solve(node.left), 0)
                r = max(solve(node.right), 0)
                
                # What is the best path that passes through me, connecting my left and right subtrees?"
                self.maxSum = max(self.maxSum, node.val + l + r)

                # If my parent wants to include me in a path, what is the best single branch I can offer them?
                return max(l, r) + node.val

        self.maxSum = float('-inf')
        solve(root)
        return self.maxSum
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
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return None
        elif root in (p,q):
            return root
        else:
            left = self.lowestCommonAncestor(root.left, p, q)
            right = self.lowestCommonAncestor(root.right, p, q)

            if left and right:
                return root
            elif not left and not right:
                return None
            elif right:
                return right
            elif left:
                return left
```

</details>
<BR>
