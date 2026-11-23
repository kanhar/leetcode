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

### [Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/)

> Invert a binary tree.

The same problem as on the [Pre-Order page](PreOrder.md#invert-binary-trees), solved the other way round: children first.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 36, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart LR
    subgraph A ["Input"]
        direction TB
        ar(("4"))
        aL(("2"))
        aR(("7"))
        aLL(("1"))
        aLR(("3"))
        ar --- aL
        ar --- aR
        aL --- aLL
        aL --- aLR
    end
    subgraph B ["Output"]
        direction TB
        br(("4"))
        bL(("7"))
        bR(("2"))
        bRL(("3"))
        bRR(("1"))
        br --- bL
        br --- bR
        bR --- bRL
        bR --- bRR
    end
    A ==>|"invert"| B
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
    class ar,aL,aR,aLL,aLR,bL,bR,bRL,bRR n
    class br hi
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Swapping a node's two children and inverting its two subtrees can be done in either order, so both traversals work. Pre-order swaps first and recurses second. Post-order recurses first and swaps second.

**Key intuition 2:** Post-order: invert both subtrees first (each call hands back its inverted subtree), then swap this node's two children on the way back up.

**Careful with in-order.** Left, then swap, then right looks natural but is wrong. After the swap, `root.right` is the subtree you have just inverted, so the second call inverts it back, and the original right subtree is never inverted. On random trees it gives the wrong answer most of the time.

<details><summary markdown="span">Execute! (post-order, swapping the nodes in place)</summary>

```python
class Solution:
    def invertTree(self, root: TreeNode) -> TreeNode:
        if root is None:
            return None

        # Invert both subtrees FIRST. Each call hands back its inverted subtree.
        left = self.invertTree(root.left)
        right = self.invertTree(root.right)

        # Then swap this node's children, on the way back up.
        root.left = right
        root.right = left

        return root
```

</details>
<BR>

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

## Rewiring problems: change the pointers

These problems do not just compute an answer, they **rewire the tree in place**. The pattern is the same each time: handle the children first, take the subtree each recursive call hands back, then change this node's pointers. Invert (the first problem on this page) is the simplest example.

### [Binary Tree Pruning](https://leetcode.com/problems/binary-tree-pruning/)

> Every node is 0 or 1. Remove every subtree that does not contain a 1 and return the root.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 30, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "24px"}}}%%
flowchart TB
    subgraph B ["Before: the red 0 has no 1 below it"]
        direction TB
        br(("1"))
        bgL[" "]
        bR(("0"))
        bRL(("0"))
        bRR(("1"))
        br ~~~ bgL
        br --- bR
        bR --- bRL
        bR --- bRR
    end
    subgraph A ["After: it is cut off"]
        direction TB
        ar(("1"))
        agL[" "]
        aR(("0"))
        agRL[" "]
        aRR(("1"))
        ar ~~~ agL
        ar --- aR
        aR ~~~ agRL
        aR --- aRR
    end
    B ==>|"prune"| A
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
    class br,bRR,ar,aRR g
    class bgL,agL,agRL ghost
    class bR,aR n
    class bRL r
    style B fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style A fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** You cannot tell whether a subtree should go until you have looked at everything below it, so the children must be handled first: post-order.

**Key intuition 2:** Assign what the recursive call returns back into your own pointer: `root.left = self.pruneTree(root.left)`. A subtree that was removed comes back as `None`, and assigning `None` is what cuts it off.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def pruneTree(self, root: TreeNode) -> TreeNode:
        if root is None:
            return None

        # Clean both subtrees first. A subtree with no 1 in it comes back as None.
        root.left = self.pruneTree(root.left)
        root.right = self.pruneTree(root.right)

        # Both sides were cut off and this node is a 0: nothing here is worth keeping.
        if root.val == 0 and root.left is None and root.right is None:
            return None

        return root
```

</details>
<BR>

### [Flatten Binary Tree to Linked List](https://leetcode.com/problems/flatten-binary-tree-to-linked-list/)

> Flatten the tree in place into a "linked list": every right pointer points to the next node, every left pointer is None, and the order is the pre-order traversal.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 30, "rankSpacing": 40, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "24px"}}}%%
flowchart TB
    subgraph B ["Before"]
        direction TB
        br(("1"))
        bL(("2"))
        bR(("5"))
        bLL(("3"))
        bLR(("4"))
        bgRL[" "]
        bRR(("6"))
        br --- bL
        br --- bR
        bL --- bLL
        bL --- bLR
        bR ~~~ bgRL
        bR --- bRR
    end
    subgraph A ["After: pre-order 1, 2, 3, 4, 5, 6 along the right pointers"]
        direction TB
        ar(("1"))
        agL[" "]
        aR(("2"))
        agRL[" "]
        aRR(("3"))
        agRRL[" "]
        aRRR(("4"))
        agRRRL[" "]
        aRRRR(("5"))
        agRRRRL[" "]
        aRRRRR(("6"))
        ar ~~~ agL
        ar --- aR
        aR ~~~ agRL
        aR --- aRR
        aRR ~~~ agRRL
        aRR --- aRRR
        aRRR ~~~ agRRRL
        aRRR --- aRRRR
        aRRRR ~~~ agRRRRL
        aRRRR --- aRRRRR
    end
    B ==>|"flatten"| A
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
    class br,bL,bR,bLL,bLR,bRR n
    class bgRL,agL,agRL,agRRL,agRRRL,agRRRRL ghost
    class ar,aR,aRR,aRRR,aRRRR,aRRRRR hi
    style B fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style A fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Flatten the left and right subtrees first: each becomes a chain that only uses right pointers. Then splice. The left chain goes between this node and the right chain.

**Key intuition 2:** Save `left` and `right` in variables before you rewire. Set `root.left = None`, walk to the end of the chain you moved, and attach the old right chain there. The answer is in pre-order, but the easy solution is post-order: fix the children, then splice.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def flatten(self, root: TreeNode) -> None:
        if root is None:
            return

        # Flatten both sides first: each becomes a chain that only uses right pointers.
        self.flatten(root.left)
        self.flatten(root.right)

        left = root.left
        right = root.right

        # Move the left chain to the right side and cut the left pointer.
        root.left = None
        root.right = left

        # Walk to the end of that chain and attach the old right chain there.
        tail = root
        while tail.right:
            tail = tail.right

        tail.right = right
```

This version walks to the end of the left chain at every node, so it is O(n²) on a tree that leans left. It is the clearest way to see the splice; a linear-time version exists.

</details>
<BR>

### [Binary Tree Upside Down](https://leetcode.com/problems/binary-tree-upside-down/)

> Turn the tree upside down and return the new root (LeetCode Premium).
> The original left child becomes the new root, the original root becomes its right child, and the original right child becomes its left child. Every right node has a left sibling and no children.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 30, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "24px"}}}%%
flowchart TB
    subgraph B ["Before: the left spine is 1, 2, 4"]
        direction TB
        br(("1"))
        bL(("2"))
        bR(("3"))
        bLL(("4"))
        bLR(("5"))
        br --- bL
        br --- bR
        bL --- bLL
        bL --- bLR
    end
    subgraph A ["After: now a right spine 4, 2, 1"]
        direction TB
        ar(("4"))
        aL(("5"))
        aR(("2"))
        aRL(("3"))
        aRR(("1"))
        ar --- aL
        ar --- aR
        aR --- aRL
        aR --- aRR
    end
    B ==>|"flip"| A
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
    class br,bL,bLL,ar,aR,aRR hi
    class bR,bLR,aL,aRL n
    style B fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style A fill:#f1f8e9,stroke:#689f38,color:#33691e
    linkStyle 0 stroke:#e65100,stroke-width:4px
    linkStyle 2 stroke:#e65100,stroke-width:4px
    linkStyle 5 stroke:#e65100,stroke-width:4px
    linkStyle 7 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** Only the left spine moves. Its arrows reverse, so a node's left child becomes its parent and the spine turns into a right spine. A node's old right child follows its old sibling and becomes that sibling's left child. The new root is the leftmost node.

**Key intuition 2:** Post-order: flip the left subtree first, then rewire this node. There is no recursive call on the right side, because a right child is always a leaf, so there is nothing below it to flip. Finally cut the old root's own pointers, or the tree is left with a cycle.

**Key intuition 3:** It also works top-down (pre-order): carry the node above and its old right child down as arguments and rewire as you go. Like Invert, this problem can be solved in either traversal: post-order hands the answer up, pre-order passes the information down.

<details><summary markdown="span">Execute!</summary>

Post-order: flip the left side first, then rewire this node. The new root comes back up through the calls.

```python
class Solution:
    def upsideDownBinaryTree(self, root: TreeNode) -> TreeNode:
        # Nothing to flip: an empty tree, or a node with no left child.
        if root is None or root.left is None:
            return root

        # These two stay valid after the recursive call below, because the call
        # only changes nodes at or below root.left. The root itself is untouched.
        left_child = root.left
        right_child = root.right

        # Flip the left side. We do NOT recurse on the right side: the problem
        # guarantees a right child is a leaf, so there is nothing below it to flip.
        new_root = self.upsideDownBinaryTree(left_child)

        # left_child is now at the bottom of the flipped part.
        # Hang the old right child on its left and the old root on its right.
        left_child.left = right_child
        left_child.right = root

        # The old root is now a leaf. Cut it loose, or the tree has a cycle.
        root.left = None
        root.right = None

        return new_root
```

Pre-order: rewire each node on the way down, passing the node above it and that node's old right child as arguments. Nothing is rewired on the way back; the new root is returned from the very bottom of the left spine.

```python
class Solution:
    def upsideDownBinaryTree(self, root: TreeNode) -> TreeNode:
        # parent: the node above this one. parent_right: that parent's old right child.
        def flip(node, parent, parent_right):
            # Ran past the bottom of the left spine: parent is the new root.
            if node is None:
                return parent

            left = node.left
            right = node.right

            # Rewire this node FIRST, on the way down, using what was passed in.
            node.left = parent_right
            node.right = parent

            # Then move down the left spine, passing this node and its old right child.
            return flip(left, node, right)

        return flip(root, None, None)
```

</details>
<BR>
