{: .no_toc}
# Binary Tree - Traversals

- TOC
{:toc}

### [Pre-Order](https://leetcode.com/problems/binary-tree-preorder-traversal/)

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 50, "rankSpacing": 50, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "24px"}}}%%
flowchart TB
    subgraph T ["Tree"]
        direction TB
        tr(("1"))
        tL(("2"))
        tR(("3"))
        tLL(("4"))
        tLR(("5"))
        tr --- tL
        tr --- tR
        tL --- tLL
        tL --- tLR
    end
    subgraph O ["Pre-order  (Root, Left, Right)"]
        direction LR
        o0["<b>1</b>"]
        o1["<b>2</b>"]
        o2["<b>4</b>"]
        o3["<b>5</b>"]
        o4["<b>3</b>"]
        o0 --> o1
        o1 --> o2
        o2 --> o3
        o3 --> o4
    end
    T ==>|"visit order"| O
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
    class tr,tL,tR,tLL,tLR,o0,o1,o2,o3,o4 a
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style O fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** The name says when the root is visited relative to its children: before them (pre), between them (in), after them (post).

**Key intuition 2:** The iterative version replaces the call stack with your own stack. Push the right child before the left so the left comes off first.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def solve(node):
            if node:
                res.append(node.val)
                solve(node.left)
                solve(node.right)

        res = []
        solve(root)
        return res
```

```python
class Solution(object):
    def preorderTraversal(self, root):
        res = []
        stack = [(root, False)]

        while stack:
            node, visited = stack.pop()

            if not node:
                continue

            if visited:
                # Node is marked as visited, add to result
                res.append(node.val)
            else:
                # REVERSE ORDER of Preorder: Right, Left, Root
                # Processed third
                stack.append((node.right, False))
                # Processed second
                stack.append((node.left, False))
                # Processed first
                stack.append((node, True))

        return res
```

</details>
<BR>


### [Post-Order](https://leetcode.com/problems/binary-tree-postorder-traversal/)

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 50, "rankSpacing": 50, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "24px"}}}%%
flowchart TB
    subgraph T ["Tree"]
        direction TB
        tr(("1"))
        tL(("2"))
        tR(("3"))
        tLL(("4"))
        tLR(("5"))
        tr --- tL
        tr --- tR
        tL --- tLL
        tL --- tLR
    end
    subgraph O ["Post-order  (Left, Right, Root)"]
        direction LR
        o0["<b>4</b>"]
        o1["<b>5</b>"]
        o2["<b>2</b>"]
        o3["<b>3</b>"]
        o4["<b>1</b>"]
        o0 --> o1
        o1 --> o2
        o2 --> o3
        o3 --> o4
    end
    T ==>|"visit order"| O
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
    class tr,tL,tR,tLL,tLR,o0,o1,o2,o3,o4 a
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style O fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition:** Root last means you need both children finished first, so post-order is the shape of every "combine the answers from my children" problem.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def solve(node):
            if node:
                solve(node.left)
                solve(node.right)
                res.append(node.val)
        res = []
        solve(root)
        return res
```
</details>
<BR>

```python
class Solution(object):
    def postorderTraversal(self, root):
        res = []
        stack = [(root, False)]
        while stack:
            (node, visited) = stack.pop()
            if not node:
                continue

            if visited:
                res.append(node.val)
            else:
                stack.append((node, True))
                stack.append((node.right, False))
                stack.append((node.left, False))
        return res
```

### [In-Order](https://leetcode.com/problems/binary-tree-inorder-traversal/)

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 50, "rankSpacing": 50, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "24px"}}}%%
flowchart TB
    subgraph T ["Tree"]
        direction TB
        tr(("1"))
        tL(("2"))
        tR(("3"))
        tLL(("4"))
        tLR(("5"))
        tr --- tL
        tr --- tR
        tL --- tLL
        tL --- tLR
    end
    subgraph O ["In-order  (Left, Root, Right)"]
        direction LR
        o0["<b>4</b>"]
        o1["<b>2</b>"]
        o2["<b>5</b>"]
        o3["<b>1</b>"]
        o4["<b>3</b>"]
        o0 --> o1
        o1 --> o2
        o2 --> o3
        o3 --> o4
    end
    T ==>|"visit order"| O
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
    class tr,tL,tR,tLL,tLR,o0,o1,o2,o3,o4 a
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style O fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition:** On a binary search tree, in-order visits the values in sorted order. That is the reason this traversal matters.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def solve(node):
            if node:
                solve(node.left)
                res.append(node.val)
                solve(node.right)
        res = []
        solve(root)
        return res
```

```python
class Solution(object):
    def inorderTraversal(self, root):
        res = []
        stack = [(root, False)]
        while stack:
            (node, visited) = stack.pop()
            if not node:
                continue

            if visited:
                res.append(node.val)
            else:
                stack.append((node.right, False))
                stack.append((node, True))
                stack.append((node.left, False))
        return res
```

</details>
<BR>

### [Sideways: Populating Next Right Pointers in Each Node](https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/)

> Populate each next pointer to point to its next right node.

```mermaid
%%{init: {"flowchart": {"padding": 8, "nodeSpacing": 40, "rankSpacing": 26, "subGraphTitleMargin": {"top": 0, "bottom": 4}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TB
    subgraph A ["Before"]
        direction TB
        ar(("1"))
        aL(("2"))
        aR(("3"))
        aLL(("4"))
        aLR(("5"))
        agRL[" "]
        aRR(("7"))
        ar --- aL
        ar --- aR
        aL --- aLL
        aL --- aLR
        aR ~~~ agRL
        aR --- aRR
    end
    subgraph B ["After: each next points right (or null)"]
        direction TB
        subgraph L1 [" "]
            direction LR
            L1_0(("1"))
            L1_null(["null"])
            L1_0 --> L1_null
        end
        subgraph L2 [" "]
            direction LR
            L2_0(("2"))
            L2_1(("3"))
            L2_null(["null"])
            L2_0 --> L2_1
            L2_1 --> L2_null
        end
        subgraph L3 [" "]
            direction LR
            L3_0(("4"))
            L3_1(("5"))
            L3_2(("7"))
            L3_null(["null"])
            L3_0 --> L3_1
            L3_1 --> L3_2
            L3_2 --> L3_null
        end
        L1 ~~~ L2
        L2 ~~~ L3
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
    class ar,aL,aR,aLL,aLR,aRR n
    class agRL ghost
    class L1_0,L2_0,L2_1,L3_0,L3_1,L3_2 hi
    class L1_null,L2_null,L3_null empty
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
    style L1 fill:none,stroke:none
    style L2 fill:none,stroke:none
    style L3 fill:none,stroke:none
```

**Key intuition:** Work one level at a time. While you walk a level left to right, you can collect the next level's nodes and link them as you go.

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

            if not q:
                tmp = q
                q = qChildren
                qChildren = tmp

        return root
```

</details>
<BR>

### [Level Order Traversal](https://leetcode.com/problems/binary-tree-level-order-traversal/)

> Return the values level by level, from left to right.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 34, "rankSpacing": 40, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart LR
    subgraph A ["Input"]
        direction TB
        ar(("3"))
        aL(("9"))
        aR(("20"))
        aRL(("15"))
        aRR(("7"))
        ar --- aL
        ar --- aR
        aR --- aRL
        aR --- aRR
    end
    subgraph B ["Output"]
        direction TB
        o0(["[3]"])
        o1(["[9, 20]"])
        o2(["[15, 7]"])
        o0 ~~~ o1
        o1 ~~~ o2
    end
    A ==>|"level<br/>by level"| B
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
    class ar,o0 a
    class aL,aR,o1 y
    class aRL,aRR,o2 g
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Breadth-first search with a queue visits nodes level by level. The depth-first alternative passes the depth down and files each value into the list for its depth.

**Key intuition 2:** A node's level is its parent's level plus 1, which is why both approaches work.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    #Using global state
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        def solve(node, d):
            if not node:
                return

            res[d].append(node.val)
            solve(node.left, d + 1)
            solve(node.right, d + 1)

        res = collections.defaultdict(list)
        solve(root, 0)
        return res.values()
```

</details>
<BR>

### [Level Order Traversal n-Ary](https://leetcode.com/problems/n-ary-tree-level-order-traversal/) <BR>

> The same for an n-ary tree: return the values level by level.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 34, "rankSpacing": 40, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart LR
    subgraph A ["Input"]
        direction TB
        ar(("1"))
        a0(("3"))
        a1(("2"))
        a2(("4"))
        a00(("5"))
        a01(("6"))
        ar --- a0
        ar --- a1
        ar --- a2
        a0 --- a00
        a0 --- a01
    end
    subgraph B ["Output"]
        direction TB
        o0(["[1]"])
        o1(["[3, 2, 4]"])
        o2(["[5, 6]"])
        o0 ~~~ o1
        o1 ~~~ o2
    end
    A ==>|"level<br/>by level"| B
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
    class ar,o0 a
    class a0,a1,a2,o1 y
    class a00,a01,o2 g
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition:** Exactly the same idea as the binary version. The only change is that a node has a list of children instead of a left and a right.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def levelOrder(self, root: 'Node') -> List[List[int]]:
        def solve(node, d):
            if not node:
                return

            if d == 0:
                res[d].append(node.val)
                d += 1

            for child in node.children:
                res[d].append(child.val)
                solve(child, d + 1)

        res = collections.defaultdict(list)
        solve(root, 0)
        return res.values()
```

</details>
<BR>

### [DFS Preorder Traversal: Smallest string from Leaf](https://leetcode.com/problems/smallest-string-starting-from-leaf/)

> Each node holds a number from 0 to 25 for a letter (a to z). Return the smallest string that starts at a leaf and ends at the root.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 34, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TD
    subgraph T ["Smallest string read from a leaf up to the root = “dba”"]
        direction TB
        tr(["<b>0</b><br/>a"])
        tL(["<b>1</b><br/>b"])
        tR(["<b>2</b><br/>c"])
        tLL(["<b>3</b><br/>d"])
        tLR(["<b>4</b><br/>e"])
        tRL(["<b>3</b><br/>d"])
        tRR(["<b>4</b><br/>e"])
        tr --- tL
        tr --- tR
        tL --- tLL
        tL --- tLR
        tR --- tRL
        tR --- tRR
        note["all leaf-to-root strings: dba, eba, dca, eca   (a = 0, b = 1, c = 2, ...)"]
        tLL ~~~ note
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
    class tr,tL,tLL hi
    class tR,tLR,tRL,tRR n
    class note empty
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 0 stroke:#e65100,stroke-width:4px
    linkStyle 2 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** Build the string from the root downward by putting each new letter in front, so the finished string already reads leaf to root.

**Key intuition 2:** Only a leaf (no children) completes a string. Collect those and take the smallest.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def smallestFromLeaf(self, root: Optional[TreeNode]) -> str:
        def preorder(node, path):
            if not node:
                return

            path = chr(ord('a') + node.val) + path

            if not node.left and not node.right:
                res.append(path)

            preorder(node.left, path)
            preorder(node.right, path)
        res = []
        preorder(root, "")
        return min(res)
```

</details>
<BR>
