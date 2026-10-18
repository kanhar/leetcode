{: .no_toc}
# Binary Trees - Tuplify Method
Practise here: [Leetcode]()

- TOC
{:toc}

### [Find Duplicate Subtrees](https://leetcode.com/problems/find-duplicate-subtrees/) 

> Return one root for each group of duplicate subtrees (same structure and same values).

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 38, "rankSpacing": 46, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TD
    subgraph T ["Duplicates:  “2 → 4” appears 2 times,  “4” appears 3 times"]
        direction TB
        tr(("1"))
        tL(("2"))
        tR(("3"))
        tLL(("4"))
        tgLR[" "]
        tRL(("2"))
        tRR(("4"))
        tRLL(("4"))
        tgRLR[" "]
        tr --- tL
        tr --- tR
        tL --- tLL
        tL ~~~ tgLR
        tR --- tRL
        tR --- tRR
        tRL --- tRLL
        tRL ~~~ tgRLR
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
    class tr,tR n
    class tL,tRL hi
    class tLL,tRR,tRLL a
    class tgLR,tgRLR ghost
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 2 stroke:#e65100,stroke-width:4px
    linkStyle 6 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** Describe every subtree as a tuple (value, left description, right description). Two subtrees are identical exactly when their tuples are equal.

**Key intuition 2:** Count how often each tuple appears in a dictionary, and report a subtree the moment its count reaches 2.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def findDuplicateSubtrees(self, root: Optional[TreeNode]) -> List[Optional[TreeNode]]:
        def tuplify(node):
            if node:
                tuple = (node.val, tuplify(node.left), tuplify(node.right))
                res[tuple].append(node)
                return tuple

        res = collections.defaultdict(list)
        tuplify(root)

        # Minor detail: v[0] cause any one parent node needs to be returned
        dupes = {k: v[0] for (k, v) in res.items() if len(v) > 1}
        return dupes.values()
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

**Key intuition:** Describe both trees with the same tuple. subRoot appears inside root exactly when its tuple equals the tuple of some node in root.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        def tuplify(node):
            if node:
                return (node.val, tuplify(node.left), tuplify(node.right))

        if not root:
            return False

        if tuplify(root) == tuplify(subRoot):
            return True

        return self.isSubtree(root.left, subRoot) or self.isSubtree(root.right, subRoot)
```

</details>
<BR>

### [Serialize and Deserialize Binary Tree](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/)

> Serialize a binary tree to a string, and deserialize the string back into the same tree.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 40, "rankSpacing": 36, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TB
    subgraph A ["Tree"]
        direction TB
        ar(("1"))
        aL(("2"))
        aR(("3"))
        aRL(("4"))
        aRR(("5"))
        ar --- aL
        ar --- aR
        aR --- aRL
        aR --- aRR
    end
    S["a string, in any format you choose<br/>(for example: 1,2,3,null,null,4,5)"]
    subgraph B ["Same tree"]
        direction TB
        br(("1"))
        bL(("2"))
        bR(("3"))
        bRL(("4"))
        bRR(("5"))
        br --- bL
        br --- bR
        bR --- bRL
        bR --- bRR
    end
    A ==>|"serialize"| S
    S ==>|"deserialize"| B
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
    class ar,aL,aR,aRL,aRR n
    class S y
    class br,bL,bR,bRL,bRR g
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** A traversal that also records the missing children rebuilds a tree in only one way. The tuple (value, left, right), with None for a missing child, is exactly that record.

**Key intuition 2:** Deserialize is the mirror image of serialize: read the value, then rebuild the left, then rebuild the right.

<details><summary markdown="span">Execute!</summary>

```python
import collections
import json
class Codec:
    def serialize(self, root):
        def tuplify(node):
            if node:
                return (node.val, tuplify(node.left), tuplify(node.right))

        res = tuplify(root)
        return json.dumps(res)

    def deserialize(self, data):
        def detuplify(arr):
            if arr:
                root = TreeNode(arr[0])
                root.left = detuplify(arr[1])
                root.right = detuplify(arr[2])
                return root
        return detuplify(json.loads(data))
```

</details>
<BR>


### [Serialize and Deserialize N-ary Tree](https://leetcode.com/problems/serialize-and-deserialize-n-ary-tree/) <BR>

> The same for an n-ary tree: serialize it to a string, and deserialize the string back into the same tree.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 40, "rankSpacing": 36, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "19px"}}}%%
flowchart TB
    subgraph A ["Tree"]
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
    S["a string, in any format you choose"]
    subgraph B ["Same tree"]
        direction TB
        br(("1"))
        b0(("3"))
        b1(("2"))
        b2(("4"))
        b00(("5"))
        b01(("6"))
        br --- b0
        br --- b1
        br --- b2
        b0 --- b00
        b0 --- b01
    end
    A ==>|"serialize"| S
    S ==>|"deserialize"| B
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
    class ar,a0,a1,a2,a00,a01 n
    class S y
    class br,b0,b1,b2,b00,b01 g
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition:** Same as the binary version, except each node records a list of children. Serialize writes (value, [children...]) and deserialize reads it back the same way.

<details><summary markdown="span">Execute!</summary>

```python
class Codec:
    def serialize(self, root):
        def tuplify(root):
            if root:
                return (root.val, [tuplify(x) for x in root.children])

        return json.dumps(tuplify(root))

    def deserialize(self, data):
        def detuplify(arr):
            if arr:
                root = Node(arr[0], [])
                for c in arr[1]:
                    root.children.append(detuplify(c))
                return root

        return detuplify(json.loads(data))
```

</details>
<BR>

