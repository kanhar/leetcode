{: .no_toc}
# Binary Search Trees
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9db7rant)

- TOC
{:toc}

### [Convert Sorted Array to BST](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree)

> Given an integer array nums where the elements are sorted in ascending order,
convert it to a height-balanced binary search tree.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 36, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart LR
    subgraph A ["Sorted array"]
        direction LR
        a0["-10"]
        a1["-3"]
        a2["0"]
        a3["5"]
        a4["9"]
        a0 ~~~ a1
        a1 ~~~ a2
        a2 ~~~ a3
        a3 ~~~ a4
    end
    subgraph B ["Height-balanced BST"]
        direction TB
        t0(("0"))
        tm10(("-10"))
        tg1(("."))
        tm10 --- tg1
        tm3(("-3"))
        tm10 --- tm3
        t0 --- tm10
        t5(("5"))
        tg2(("."))
        t5 --- tg2
        t9(("9"))
        t5 --- t9
        t0 --- t5
    end
        A ==> B
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
    class a2,t0 hi
    class a0,a3,tm10,t5 a
    class a1,a4,tm3,t9 n
    class tg1,tg2 ghost
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
    linkStyle 4 stroke:none
    linkStyle 7 stroke:none
```

The code picks `mid = (start + end) // 2`. The middle of the whole array (0) is the root. The left half `[-10, -3]` has its middle at -10, so -3 hangs to its right. The right half `[5, 9]` has its middle at 5, so 9 hangs to its right.

**Key intuition:** Make the middle element the root. Then both sides have about the same number of elements, which is what makes the tree balanced. Repeat on each half.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def sortedArrayToBST(self, arr: List[int], start = 0, end = None) -> TreeNode:
        if end is None:
            end = len(arr)-1

        if start > end:
            return None

        mid = (start+end)//2
        return TreeNode(arr[mid], self.sortedArrayToBST(arr, start, mid - 1), self.sortedArrayToBST(arr, mid + 1, end))
```

</details>
<BR>

### [Inorder successor](https://leetcode.com/problems/inorder-successor-in-bst/)

> Given a binary search tree and a node in it, find the in-order successor of that node in the BST.
The successor of a node p is the node with the smallest key greater than p.val.
>  <BR>

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 36, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart TB
    subgraph S ["Successor of 15"]
        direction TB
        s20(("20"))
        s10(("10"))
        s5(("5"))
        s10 --- s5
        s15(("15"))
        s10 --- s15
        s20 --- s10
        s30(("30"))
        s25(("25"))
        s30 --- s25
        s35(("35"))
        s30 --- s35
        s20 --- s30
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
    class s20 g
    class s10,s5,s30,s25,s35 n
    class s15 hi
    style S fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 1 stroke:#e65100,stroke-width:4px
    linkStyle 2 stroke:#e65100,stroke-width:4px
```

At 20, 15 is smaller, so go left and remember 20 (green). At 10, 15 is larger, so go right. At 15, nothing larger is below, so the search returns nothing, and the remembered 20 is the answer. Going right never remembers anything, because the answer cannot be there.

**Key intuition 1:** If p is smaller than the current node, this node might be the successor: remember it and go left to look for something closer. Otherwise go right.

**Key intuition 2:** The successor is the smallest value greater than p, which is why the "remember it" step only happens when you turn left.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def inorderSuccessor(self, root, p):
        if not root:
            return None
        if p.val < root.val:
            #cause the successor will be by definition one up
            return self.inorderSuccessor(root.left,p) or root

        #cause the successor will always be down. No need to go up here.
        return self.inorderSuccessor(root.right,p)
```

</details>
<BR>

### [Lowest Common Ancestor](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

> Given a binary Search tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 36, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart TB
    subgraph L ["Lowest common ancestor of 5 and 15"]
        direction TB
        l20(("20"))
        l10(("10"))
        l5(("5"))
        l10 --- l5
        l15(("15"))
        l10 --- l15
        l20 --- l10
        l30(("30"))
        l25(("25"))
        l30 --- l25
        l35(("35"))
        l30 --- l35
        l20 --- l30
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
    class l20,l30,l25,l35 n
    class l10 g
    class l5,l15 a
    style L fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 2 stroke:#e65100,stroke-width:4px
```

At 20 both 5 and 15 are smaller, so go left. At 10 one is smaller and one is larger (the two nodes split), so 10 is the lowest common ancestor.

**Key intuition 1:** The BST ordering tells you which way both nodes lie: both smaller means go left, both larger means go right.

**Key intuition 2:** The first node where p and q fall on different sides (or one of them equals the node) is the lowest common ancestor.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def lowestCommonAncestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        if root is not None:
            if root.val < min(p.val, q.val):
                return self.lowestCommonAncestor(root.right, p,q)
            if root.val > max(p.val, q.val):
                return self.lowestCommonAncestor(root.left, p,q)

            return root
```

</details>
<BR>

### [Check if BST](https://leetcode.com/problems/validate-binary-search-tree/)

> Given a binary tree, determine if it is a valid binary search tree (BST).

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 36, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart TB
    subgraph V ["Each node gets a (low, high) window"]
        direction TB
        v10["10<br/>(−∞, ∞)"]
        v5["5<br/>(−∞, 10)"]
        v10 --- v5
        v15["15<br/>(10, ∞)"]
        v6["6<br/>(10, 15)"]
        v15 --- v6
        vg1(("."))
        v15 --- vg1
        v10 --- v15
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
    class v10,v15 a
    class v5 g
    class v6 r
    class vg1 ghost
    style V fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 1 stroke:#e65100,stroke-width:4px
    linkStyle 2 stroke:none
    linkStyle 3 stroke:#e65100,stroke-width:4px
```

Going left caps the high end at the parent's value, going right raises the low end. The 6 is smaller than its parent 15, so a parent-only check passes, but it sits in the right subtree of 10, so its window is (10, 15) and 6 fails.

**Key intuition 1:** It is not enough to compare a node with its parent. Every node must fall inside a (low, high) window inherited from all its ancestors.

**Key intuition 2:** Going left lowers the upper bound to the node's value. Going right raises the lower bound to it. Another way to see it: an in-order traversal must be strictly increasing.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def isValidBST(self, root: TreeNode, lo=float('-inf'), hi=float('inf')) -> bool:
        if not root:
            return True
        if not lo < root.val < hi:
            return False

        return self.isValidBST(root.left, lo, min(root.val, hi)) and self.isValidBST(root.right, max(lo, root.val), hi)
```

</details>
<BR>