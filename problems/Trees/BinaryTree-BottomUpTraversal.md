{: .no_toc}
# Binary Tree - Bottom Up Traversal
Practise here: [Leetcode]()

- TOC
{:toc}

### Path with Maximum sum

> Given a non-empty binary tree, find the maximum path sum
> [Leetcode](https://leetcode.com/problems/binary-tree-maximum-path-sum/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

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

### Tree Diameter

> Tree Diameter
> [Leetcode](https://leetcode.com/problems/diameter-of-binary-tree/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode, max_d=0) -> int:
        def solve(root):
            if root is None:
                return 0
            else:
                left  = solve(root.left)
                right = solve(root.right)
                self.res = max(self.res, left + right)      # Calculates Diameter
                return max(left, right) + 1                 # Calculates Depth
        self.res = 0
        solve(root)
        return self.res

class Solution:
    def diameterOfBinaryTree(self, root: TreeNode, max_d=0) -> int:
        def depth(root):
            if root is None:
                return 0

            return max(depth(root.left), depth(root.right)) + 1

        def diam_at(root):
            if root is None:
                return 0

            return depth(root.left) + depth(root.right)

        if root is None:
            return 0

        return max(max_d, diam_at(root), self.diameterOfBinaryTree(root.left), self.diameterOfBinaryTree(root.right))
```

</details>
<BR>

### Number of Paths having Sum

> Given a binary tree in which each node contains an integer value. Find the number of paths that sum to a given value.

> [Leetcode](https://leetcode.com/problems/path-sum-iii/) <BR>
> [See also](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/)

<details><summary markdown="span">Let's see some code!</summary>

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


class Solution:
    def pathSum(self, root: TreeNode, sum: int) -> int:
        def preorder(node: TreeNode, curr_sum) -> None:
            if not node:
                return

            curr_sum += node.val        # current prefix sum
            if curr_sum == k:
                self.totalCount += 1

            # number of times the curr_sum − k has occurred already,
            # determines the number of times a path with sum k has occurred up to the current node
            self.totalCount += h[curr_sum - k]

            # Add the current sum into hashmap to use it during the child nodes processing only
            h[curr_sum] += 1
            preorder(node.left, curr_sum)
            preorder(node.right, curr_sum)
            h[curr_sum] -= 1
            # ^ remove current sum from hashmap - to not use it during the parallel subtree processing

        totalCount, k = 0, sum
        h = collections.defaultdict(int)
        preorder(root, 0)
        return self.totalCount
```

</details>
<BR>

### Find the lexicographically smallest string that starts at a leaf of this tree and ends at the root.

> Given
> [Leetcode](https://leetcode.com/problems/smallest-string-starting-from-leaf/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:
        def solve(node, accum=[]):
            if node:
                if node and node.left is None and node.right is None:  # i.e. if leaf
                    res.append(''.join([chr(x + 97) for x in reversed(accum + [node.val])]))
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

### Check if tree is Height Balanced

> Given a binary tree, determine if it is height-balanced - left and right subtrees of every node differ in height by no more than 1.
> [Leetcode](https://leetcode.com/problems/balanced-binary-tree/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

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

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def depth(node):
            if not node:
                return 0
            else:
                return max(depth(node.left), depth(node.right)) + 1

        def isBalanced(node):
            if not node:
                return True
            elif abs(depth(node.left) - depth(node.right)) > 1:
                return False
            else:
                return isBalanced(node.left) and isBalanced(node.right)

        return isBalanced(root)
```

</details>
<BR>

### Lowest Common Ancestor

> Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
> [Leetcode](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) <BR>

<details><summary markdown="span">Let's see some code!</summary>

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



