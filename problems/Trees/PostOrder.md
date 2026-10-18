{: .no_toc}
# Post Order

> **Which traversal?** Need answers from my children before I can decide? That is post-order. Passing information *down* to my children? That is [pre-order](PreOrder.md).

Post-order means **Left, then Right, then Root**. Any tree is a root with a left subtree and a right subtree. You go all the way into the left subtree and finish all of it, then all of the right subtree, and only then do you come back to the root. The root is always the last node to finish.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 40, "rankSpacing": 70, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TD
    subgraph T ["Post-order: Left, then Right, then Root"]
        direction TB
        R(["<b>③ Root, last</b>"])
        L@{ shape: tri, label: "<b>① Left subtree</b>" }
        M["<b>then ⟶</b>"]
        S@{ shape: tri, label: "<b>② Right subtree</b>" }
        R ==>|"go down"| L
        R ~~~ M
        R --- S
        S ==>|"then up"| R
    end
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class R a
    class L,S p
    class M txt
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 0 stroke:#e65100,stroke-width:4px
    linkStyle 3 stroke:#e65100,stroke-width:4px
```

The same rule applies inside every subtree, because each subtree is itself a root with a left subtree and a right subtree.

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

Every problem below visits each node once: **O(n) time, O(h) space** for the recursion stack, where h is the tree height (O(log n) when balanced, O(n) when skewed).

- TOC
{:toc}

### [Max Depth of a Binary Tree](https://leetcode.com/problems/maximum-depth-of-binary-tree/description/)

> The maximum depth of a binary tree is the number of nodes on the longest path from the root down to a leaf.

```mermaid
%%{init: {"flowchart": {"padding": 16, "nodeSpacing": 60, "rankSpacing": 55, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart TD
    subgraph T ["Max depth = 3  (3 nodes on the highlighted path)"]
        direction TB
        tr(("3"))
        tL(("9"))
        tR(("20"))
        tRL(("15"))
        tRR(("7"))
        tr --- tL
        tr --- tR
        tR --- tRL
        tR --- tRR
    end
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class tr,tR,tRL hi
    class tL,tRR n
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 1 stroke:#e65100,stroke-width:4px
    linkStyle 2 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** A node's depth is one more than its deeper child. You cannot know yours until both children have told you theirs.

**Key intuition 2:** A missing child has depth 0. That single fact is your base case, and it makes a leaf come out as depth 1.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        def depth(node):
            if not node:
                return 0

            ls = depth(node.left)
            rs = depth(node.right)

            return max(ls,rs) + 1
        return depth(root)
```

</details>
<BR>

### [Tree Diameter](https://leetcode.com/problems/diameter-of-binary-tree/)

> The diameter is the number of edges on the longest path between any two nodes. The path may or may not pass through the root.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 46, "rankSpacing": 48, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TD
    subgraph T ["Diameter = 4  (edges on the longest path between any two nodes)"]
        direction TB
        tr(("1"))
        tL(("2"))
        tgR[" "]
        tLL(("3"))
        tLR(("4"))
        tLLL(("5"))
        tgLLR[" "]
        tgLRL[" "]
        tLRR(("6"))
        tr --- tL
        tr ~~~ tgR
        tL ---|"2"| tLL
        tL ---|"3"| tLR
        tLL ---|"1"| tLLL
        tLL ~~~ tgLLR
        tLR ~~~ tgLRL
        tLR ---|"4"| tLRR
    end
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class tr n
    class tL,tLL,tLR,tLLL,tLRR hi
    class tgR,tgLLR,tgLRL ghost
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 2 stroke:#e65100,stroke-width:4px
    linkStyle 3 stroke:#e65100,stroke-width:4px
    linkStyle 4 stroke:#e65100,stroke-width:4px
    linkStyle 7 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** The longest path bends at exactly one node, its highest point: it goes down the left side and down the right side. So the longest path through a node is (left depth) + (right depth).

**Key intuition 2:** A parent can only use one arm of a path, because a path cannot fork on the way up. So each node returns one number (its depth) but records a different one (left + right) in a global.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        def solve(root):
            if root is None:
                return 0

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

> Find the length, in edges, of the longest path in which every node has the same value.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 46, "rankSpacing": 48, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TD
    subgraph T ["Longest path of equal values = 2  (edges)"]
        direction TB
        tr(("5"))
        tL(("4"))
        tR(("5"))
        tLL(("1"))
        tLR(("1"))
        tgRL[" "]
        tRR(("5"))
        tr --- tL
        tr ---|"1"| tR
        tL --- tLL
        tL --- tLR
        tR ~~~ tgRL
        tR ---|"2"| tRR
    end
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class tr,tR,tRR hi
    class tL,tLL,tLR n
    class tgRL ghost
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 1 stroke:#e65100,stroke-width:4px
    linkStyle 5 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** This is Tree Diameter with a rule: an arm only counts if that child has the same value as me. Otherwise that arm is 0.

**Key intuition 2:** Same trick as diameter: return the longer single arm to your parent, and record the sum of both arms as a candidate answer.

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

> Find the maximum path sum. A path can start and end at any node.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 46, "rankSpacing": 48, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TD
    subgraph T ["Max path sum = 42  (15 + 20 + 7)"]
        direction TB
        tr(("-10"))
        tL(("9"))
        tR(("20"))
        tRL(("15"))
        tRR(("7"))
        tr --- tL
        tr --- tR
        tR --- tRL
        tR --- tRR
    end
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class tr,tL n
    class tR,tRL,tRR hi
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 2 stroke:#e65100,stroke-width:4px
    linkStyle 3 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** Same shape as Tree Diameter: the best path bends at one top node, so record node + left arm + right arm.

**Key intuition 2:** A negative arm only hurts, so treat it as 0 (take max(arm, 0)). Return node + the better single arm so your parent can extend the path.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        def solve(node):
            if not node:
                return 0

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

> A tree is height-balanced if, at every node, the left and right subtrees differ in height by no more than 1.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 60, "rankSpacing": 50, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph A ["Balanced  (sides differ by at most 1)"]
        direction TB
        ar(("3"))
        aL(("9"))
        aR(("20"))
        aRL(("15"))
        aRR(("7"))
        ar ---|"height 1"| aL
        ar ---|"height 2"| aR
        aR --- aRL
        aR --- aRR
    end
    subgraph B ["Not balanced  (root sides differ by 2)"]
        direction TB
        br(("1"))
        bL(("2"))
        bgR[" "]
        bLL(("3"))
        bgLR[" "]
        br ---|"height 2"| bL
        br ~~~ bgR
        bL --- bLL
        bL ~~~ bgLR
        bE(["none"])
        br ---|"height 0"| bE
    end
    A ~~~ B
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class ar,aL,aR,aRL,aRR,bL,bLL n
    class br r
    class bgR,bgLR ghost
    class bE empty
    style A fill:#f1f8e9,stroke:#689f38,color:#33691e
    style B fill:#fff5f5,stroke:#e57373,color:#b71c1c
```

**Key intuition 1:** Do not compute heights separately for every node (that repeats work). Compute the height once, from the bottom up, and check the balance on the way back up.

**Key intuition 2:** A node is unbalanced if its two heights differ by more than 1. Once one node is unbalanced, the whole tree is.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        def depth(node):
            if not node:
                return 0

            ls = depth(node.left)
            rs = depth(node.right)

            if abs(ls - rs) > 1:
                self.balanced = False

            return 1 + max(ls, rs)

        self.balanced = True
        depth(root)
        return self.balanced
```

</details>
<BR>

### [Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

> Find the lowest common ancestor (LCA) of two given nodes: the lowest node that has both of them as descendants (a node counts as a descendant of itself).

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 32, "rankSpacing": 46, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "18px"}}}%%
flowchart TD
    subgraph T ["p = 5, q = 1  →  LCA = 3  (lowest node with both below it)"]
        direction TB
        tr(["<b>3</b><br/>LCA"])
        tL(["<b>5</b><br/>p"])
        tR(["<b>1</b><br/>q"])
        tLL(("6"))
        tLR(("2"))
        tRL(("0"))
        tRR(("8"))
        tLRL(("7"))
        tLRR(("4"))
        tr --- tL
        tr --- tR
        tL --- tLL
        tL --- tLR
        tR --- tRL
        tR --- tRR
        tLR --- tLRL
        tLR --- tLRR
    end
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class tr hi
    class tL,tR a
    class tLL,tLR,tRL,tRR,tLRL,tLRR n
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
```

**Key intuition 1:** Ask each subtree one question: "do you contain p or q?" If both sides say yes, this node is the lowest common ancestor.

**Key intuition 2:** If only one side says yes, pass that answer upward unchanged: it is either the LCA that was already found or one of the targets.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if not root:
            return None
        if root in (p,q):
            return root

        left = self.lowestCommonAncestor(root.left, p, q)
        right = self.lowestCommonAncestor(root.right, p, q)

        if left and right:
            return root
        if not left and not right:
            return None
        if right:
            return right
        if left:
            return left
```

</details>
<BR>
