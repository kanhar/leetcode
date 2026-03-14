{: .no_toc}
# Pre Order 

![Alt text](../../IMG_20260221_060619.png)

Every single snippet here follows a Pre-order Traversal pattern: the  "Root" logic (comparing values or creating the parent node) happens before the function fully dives into the children. It is a "top-down" approach: the current level decides the fate of the branches below it.

- TOC
{:toc}

### [Invert Binary Trees](https://leetcode.com/problems/invert-binary-tree/)

![Diagram: Inverted Tree](https://assets.leetcode.com/uploads/2021/03/14/invert2-tree.jpg)
> Invert a binary tree. <BR>
> Note: This is an interesting use of reversing sorted order of a BST in place <BR> 
> * In order traversal of a BST (L,N,R) results in a ascending sorted list
> * In order traversal of an inverted BST (R,N,L) results in a descending sorted list.  

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

### [Symmetric Trees](https://leetcode.com/problems/symmetric-tree/)

> Given a binary tree, check whether it is a mirror of itself (ie, symmetric around its center).

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def solve(a,b):
            if a is None and b is None:
                return True
            elif a is None or b is None:
                return False
            elif a.val != b.val:
                return False
            else:
                return solve(a.left, b.right) and solve(a.right, b.left)

        return solve(root, root)
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

### [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) 

> Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values with a subtree of s.
<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def isSubtree(self, root, subRoot): # LeetCode uses root/subRoot names
        if not root: 
            return False
        
        # 1. Check if they match starting here
        if self.isMatch(root, subRoot):
            return True
        
        # 2. If not, recurse down the main tree
        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)

    def isMatch(self, a, b):
        if not a and not b:
            return True
        if not a or not b: 
            return False
        if a.val != b.val:
            return False
        return self.isMatch(a.left, b.left) and self.isMatch(a.right, b.right)
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

