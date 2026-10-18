{: .no_toc}
# Pre Order 

> **Which traversal?** Passing information *down* to my children? That is pre-order. Need answers from my children before I can decide? That is [post-order](PostOrder.md).

Pre-order means **Root, then Left, then Right**. Visit the root first, then go all the way into the left subtree and finish all of it, then all of the right subtree.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 40, "rankSpacing": 70, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TD
    subgraph T ["Pre-order: Root, then Left, then Right"]
        direction TB
        R(["<b>① Root, first</b>"])
        L@{ shape: tri, label: "<b>② Left subtree</b>" }
        M["<b>then ⟶</b>"]
        S@{ shape: tri, label: "<b>③ Right subtree</b>" }
        R ==>|"go down"| L
        R ~~~ M
        R --- S
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
```

The same rule applies inside every subtree, because each subtree is itself a root with a left subtree and a right subtree.

Every single snippet here follows a Pre-order Traversal pattern: the  "Root" logic (comparing values or creating the parent node) happens before the function fully dives into the children. It is a "top-down" approach: the current level decides the fate of the branches below it.

- TOC
{:toc}

### [Symmetric Trees](https://leetcode.com/problems/symmetric-tree/)

> Check whether a binary tree is a mirror of itself (symmetric around its center).

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 40, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart LR
    subgraph A ["Symmetric"]
        direction TB
        ar(("1"))
        aL(("2"))
        aR(("2"))
        aLL(("3"))
        agLR[" "]
        agRL[" "]
        aRR(("3"))
        ar --- aL
        ar --- aR
        aL --- aLL
        aL ~~~ agLR
        aR ~~~ agRL
        aR --- aRR
    end
    subgraph B ["Not symmetric"]
        direction TB
        br(("1"))
        bL(("2"))
        bR(("2"))
        bgLL[" "]
        bLR(("3"))
        bgRL[" "]
        bRR(("3"))
        br --- bL
        br --- bR
        bL ~~~ bgLL
        bL --- bLR
        bR ~~~ bgRL
        bR --- bRR
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
    class ar,aL,aR,aLL,aRR,br,bL,bR,bLR,bRR n
    class agLR,agRL,bgLL,bgRL ghost
    style A fill:#f1f8e9,stroke:#689f38,color:#33691e
    style B fill:#fff5f5,stroke:#e57373,color:#b71c1c
```

**Key intuition 1:** A tree is symmetric when its left subtree is the mirror image of its right subtree, so you have to compare two nodes at the same time.

**Key intuition 2:** Write a helper that takes two nodes. They mirror each other if the values match, a.left mirrors b.right, and a.right mirrors b.left.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        def solve(a,b):
            if a is None and b is None:
                return True
            if a is None or b is None:
                return False
            if a.val != b.val:
                return False

            return solve(a.left, b.right) and solve(a.right, b.left)

        return solve(root, root)
```
</details>
<BR>

### [Flip Equivalent Binary Trees](https://leetcode.com/problems/flip-equivalent-binary-trees/)

> Are trees X and Y flip equivalent? A flip swaps the left and right children of a node, and you may flip any number of nodes.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 34, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart LR
    subgraph A ["Tree X"]
        direction TB
        ar(("1"))
        aL(("2"))
        aR(("3"))
        aLL(("4"))
        aLR(("5"))
        ar --- aL
        ar --- aR
        aL --- aLL
        aL --- aLR
    end
    subgraph B ["Tree Y"]
        direction TB
        br(("1"))
        bL(("3"))
        bR(("2"))
        bRL(("5"))
        bRR(("4"))
        br --- bL
        br --- bR
        bR --- bRL
        bR --- bRR
    end
    A ==>|"swap children<br/>at some nodes<br/>→ equal?"| B
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
    class ar,aL,aR,aLL,aLR,br,bL,bR,bRL,bRR n
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#fafafa,stroke:#bdbdbd,color:#37474f
```

**Key intuition 1:** This is the "same tree" check, with one extra freedom: at every pair of nodes you may match children straight across or crossed.

**Key intuition 2:** Check the values first, then accept either (left~left and right~right) or (left~right and right~left).

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def flipEquiv(self, a, b):
        if a == b == None:
            return True
        if a is None or b is None:
            return False
        if a.val != b.val:
            return False
        return (self.flipEquiv(a.left, b.left)  and self.flipEquiv(a.right, b.right) or
                self.flipEquiv(a.left, b.right) and self.flipEquiv(a.right, b.left))
```

</details>
<BR>

### [Merge Two Binary Trees](https://leetcode.com/problems/merge-two-binary-trees/)

> Lay one tree on top of the other and merge them: where two nodes overlap, add their values; otherwise keep the node that exists.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 30, "rankSpacing": 40, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "18px"}}}%%
flowchart TB
    subgraph A ["Tree 1"]
        direction TB
        ar(("1"))
        aL(("3"))
        aR(("2"))
        aLL(("5"))
        agLR[" "]
        ar --- aL
        ar --- aR
        aL --- aLL
        aL ~~~ agLR
    end
    subgraph B ["Tree 2"]
        direction TB
        br(("2"))
        bL(("1"))
        bR(("3"))
        bgLL[" "]
        bLR(("4"))
        bgRL[" "]
        bRR(("7"))
        br --- bL
        br --- bR
        bL ~~~ bgLL
        bL --- bLR
        bR ~~~ bgRL
        bR --- bRR
    end
    subgraph M ["Merged  (overlapping nodes add up)"]
        direction TB
        mr(["<b>3</b> = 1+2"])
        mL(["<b>4</b> = 3+1"])
        mR(["<b>5</b> = 2+3"])
        mLL(("5"))
        mLR(("4"))
        mgRL[" "]
        mRR(("7"))
        mr --- mL
        mr --- mR
        mL --- mLL
        mL --- mLR
        mR ~~~ mgRL
        mR --- mRR
    end
    A ==> M
    B ==> M
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
    class ar,aL,aR,aLL,br,bL,bR,bLR,bRR,mLL,mLR,mRR n
    class agLR,bgLL,bgRL,mgRL ghost
    class mr,mL,mR hi
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style M fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Where only one tree has a node, just reuse that whole subtree. There is nothing to merge.

**Key intuition 2:** Where both have a node, add the values and merge the left children and the right children the same way.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def mergeTrees(self, a: TreeNode, b: TreeNode) -> TreeNode:
        if a is None and b is None:
            return
        if a is None:
            return b
        if b is None:
            return a

        return TreeNode(a.val + b.val, self.mergeTrees(a.left, b.left), self.mergeTrees(a.right, b.right))
```

</details>
<BR>

### [Subtree of Another Tree](https://leetcode.com/problems/subtree-of-another-tree/) 

> Does the tree subRoot appear inside root, with exactly the same structure and values?

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 32, "rankSpacing": 42, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart LR
    subgraph A ["root"]
        direction TB
        ar(("3"))
        aL(("4"))
        aR(("5"))
        aLL(("1"))
        aLR(("2"))
        ar --- aL
        ar --- aR
        aL --- aLL
        aL --- aLR
    end
    subgraph B ["subRoot"]
        direction TB
        br(("4"))
        bL(("1"))
        bR(("2"))
        br --- bL
        br --- bR
    end
    B -.->|"appears<br/>inside root?<br/>yes"| A
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
    class ar,aR n
    class aL,aLL,aLR,br,bL,bR hi
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 2 stroke:#e65100,stroke-width:4px
    linkStyle 3 stroke:#e65100,stroke-width:4px
    linkStyle 4 stroke:#e65100,stroke-width:4px
    linkStyle 5 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** Two questions: does subRoot match the tree starting right here? If not, ask the same question about the left and right children.

**Key intuition 2:** "Does it match starting here" is just the same-tree check. Keep it as its own small helper.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    # LeetCode uses root/subRoot names
    def isSubtree(self, root, subRoot):
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

> Count the paths whose values add up to a target. A path goes downward (parent to child) and may start and end at any node. [See also](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/)

```mermaid
%%{init: {"flowchart": {"padding": 11, "nodeSpacing": 26, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "17px"}}}%%
flowchart TD
    subgraph T ["target = 8  →  3 downward paths:  5+3,  5+2+1,  −3+11"]
        direction TB
        tr(("10"))
        tL(("5"))
        tR(("-3"))
        tLL(("3"))
        tLR(("2"))
        tgRL[" "]
        tRR(("11"))
        tLLL(("3"))
        tLLR(("-2"))
        tgLRL[" "]
        tLRR(("1"))
        tr --- tL
        tr --- tR
        tL --- tLL
        tL --- tLR
        tR ~~~ tgRL
        tR --- tRR
        tLL --- tLLL
        tLL --- tLLR
        tLR ~~~ tgLRL
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
    class tr,tLLL,tLLR n
    class tL,tR,tLL,tLR,tRR,tLRR hi
    class tgRL,tgLRL ghost
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 2 stroke:#1565c0,stroke-width:4px
    linkStyle 3 stroke:#2e7d32,stroke-width:4px
    linkStyle 5 stroke:#6a1b9a,stroke-width:4px
    linkStyle 9 stroke:#2e7d32,stroke-width:4px
```

**Key intuition 1:** A path can start at any node, so for every node ask: how many downward paths that start here add up to the target?

**Key intuition 2:** The total is the paths starting at this node, plus the answer for the left subtree, plus the answer for the right subtree. That is why the code has two recursions.

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

