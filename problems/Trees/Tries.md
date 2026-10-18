{: .no_toc}
# Prefix Tree (Trie)
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9db74ov1)

A trie stores words one letter per node, so words that start the same way share the same path. (The ternary search tree is a different structure with its own optional page: [Ternary Search Trees](TernarySearchTrees.md).)

```mermaid
%%{init: {"flowchart": {"padding": 18, "nodeSpacing": 22, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TD
    subgraph T ["Words: car, cat, cow, do, dog   (green = a word ends here)"]
        direction TB
        root(["root"])
        n0(("c"))
        n1(("d"))
        n2(("a"))
        n3(("o"))
        n4(("o"))
        n5(("r"))
        n6(("t"))
        n7(("w"))
        n8(("g"))
        root --- n0
        root --- n1
        n0 --- n2
        n0 --- n3
        n1 --- n4
        n2 --- n5
        n2 --- n6
        n3 --- n7
        n4 --- n8
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
    classDef hg fill:#e8f5e9,stroke:#e65100,stroke-width:3px,color:#1b5e20
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class root a
    class n0,n1,n2,n3 n
    class n4,n5,n6,n7,n8 g
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
```

* Each line is one letter. Walking down from the root spells a prefix.
* A green node means a word ends there: `do` is a word, and also the start of `dog`.
* Words that start the same way share their path: `car` and `cat` store `c` and `a` only once.

#### Build one in 5 lines

Every problem below starts from this builder. A node is just a dictionary that maps a letter to the next node.

```python
def build(words):
    root = {}
    for word in words:
        node = root
        for ch in word:
            # step down; create the letter if it is new
            node = node.setdefault(ch, {})
        # a word ends here
        node["$"] = True
    return root

# {'c': {'a': {'r': {'$': True}, 't': {'$': True}}}}
build(["car", "cat"])
```

**Study order:** the first three problems below are the whole idea, and they are short. Wildcard search adds one twist. The last two are hard, so come back to them later.

- TOC
{:toc}

### [Implement Trie](https://leetcode.com/problems/implement-trie-prefix-tree/)

> Implement `insert`, `search` (is this exact word stored?) and `startsWith` (does any stored word begin with this?).

```mermaid
%%{init: {"flowchart": {"padding": 18, "nodeSpacing": 22, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart LR
    subgraph T ["insert “apple”, then “app”   (green = a word ends here)"]
        direction LR
        root(["root"])
        n0(("a"))
        n1(("p"))
        n2(("p"))
        n3(("l"))
        n4(("e"))
        root --- n0
        n0 --- n1
        n1 --- n2
        n2 --- n3
        n3 --- n4
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
    classDef hg fill:#e8f5e9,stroke:#e65100,stroke-width:3px,color:#1b5e20
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class root a
    class n0,n1,n3 n
    class n2,n4 g
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
```

**Key intuition 1:** Words that start the same share the same path from the root, so a prefix is just "walk down the letters and see whether the path exists".

**Key intuition 2:** Mark the node where a word ENDS (here with a '$' key). Without it you cannot tell the stored word "app" from the mere prefix of "apple": search needs the marker, startsWith does not.

<details><summary markdown="span">Execute!</summary>

```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def _walk(self, text: str):
        node = self.root
        for ch in text:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word: str) -> bool:
        node = self._walk(word)
        return node is not None and "$" in node

    def startsWith(self, prefix: str) -> bool:
        return self._walk(prefix) is not None
```

</details>
<BR>

### [Replace Words](https://leetcode.com/problems/replace-words/)

> Replace each word in a sentence with the shortest dictionary root that is a prefix of it. Words with no root stay as they are.

```mermaid
%%{init: {"flowchart": {"padding": 18, "nodeSpacing": 22, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TD
    subgraph T ["“cattle” becomes “cat”   (the shortest root that is a prefix)"]
        direction TB
        root(["root"])
        n0(("b"))
        n1(("c"))
        n2(("r"))
        n3(("a"))
        n4(("a"))
        n5(("a"))
        n6(("t"))
        n7(("t"))
        n8(("t"))
        root --- n0
        root --- n1
        root --- n2
        n0 --- n3
        n1 --- n4
        n2 --- n5
        n3 --- n6
        n4 --- n7
        n5 --- n8
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
    classDef hg fill:#e8f5e9,stroke:#e65100,stroke-width:3px,color:#1b5e20
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class root a
    class n0,n2,n3,n5 n
    class n1,n4 hi
    class n6,n8 g
    class n7 hg
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 1 stroke:#e65100,stroke-width:4px
    linkStyle 4 stroke:#e65100,stroke-width:4px
    linkStyle 7 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** For each word, walk down the trie; the first time you land on a node that ends a word, that is the shortest root, so stop and use it.

**Key intuition 2:** If the path runs out of letters before any word ends, the word has no root and stays as it is.

<details><summary markdown="span">Execute!</summary>

```python
# the trie builder from the top of this page
def build(words):
    root = {}
    for word in words:
        node = root
        for ch in word:
            # step down; create the letter if it is new
            node = node.setdefault(ch, {})
        # a word ends here
        node["$"] = True
    return root

class Solution:
    def replaceWords(self, dictionary: List[str], sentence: str) -> str:
        root = build(dictionary)

        def shortest_root(word):
            node = root
            for i, ch in enumerate(word):
                if ch not in node:
                    # no root is a prefix of this word
                    return word
                node = node[ch]
                if "$" in node:
                    # the first word end is the shortest root
                    return word[:i + 1]
            return word

        return " ".join(shortest_root(w) for w in sentence.split())
```

</details>
<BR>

### [Longest Common Prefix](https://leetcode.com/problems/longest-common-prefix/)

> Find the longest common prefix of a list of words.

```mermaid
%%{init: {"flowchart": {"padding": 18, "nodeSpacing": 22, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart LR
    subgraph T ["Longest common prefix of flower, flow, flight = “fl”"]
        direction LR
        root(["root"])
        n0(("f"))
        n1(("l"))
        n2(("i"))
        n3(("o"))
        n4(("g"))
        n5(("w"))
        n6(("h"))
        n7(("e"))
        n8(("t"))
        n9(("r"))
        root --- n0
        n0 --- n1
        n1 --- n2
        n1 --- n3
        n2 --- n4
        n3 --- n5
        n4 --- n6
        n5 --- n7
        n6 --- n8
        n7 --- n9
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
    classDef hg fill:#e8f5e9,stroke:#e65100,stroke-width:3px,color:#1b5e20
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class root a
    class n0,n1 hi
    class n2,n3,n4,n6,n7 n
    class n5,n8,n9 g
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 0 stroke:#e65100,stroke-width:4px
    linkStyle 1 stroke:#e65100,stroke-width:4px
```

*A trie is not required here. It is useful because it makes the answer visible: the shared prefix is the path before the first branch.*

**Key intuition 1:** The common prefix is how far every word stays on the same single path. Build a trie and walk down from the root while there is exactly one child and no word ends.

**Key intuition 2:** Stop at the first branch (two children) or the first word end. Everything walked so far is the common prefix.

<details><summary markdown="span">Execute!</summary>

```python
# the trie builder from the top of this page
def build(words):
    root = {}
    for word in words:
        node = root
        for ch in word:
            # step down; create the letter if it is new
            node = node.setdefault(ch, {})
        # a word ends here
        node["$"] = True
    return root

class SolutionLCP:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        node = build(strs)
        prefix = []
        # one way to go, and no word ends here
        while len(node) == 1 and "$" not in node:
            ch = next(iter(node))
            prefix.append(ch)
            node = node[ch]
        return "".join(prefix)
```

</details>
<BR>

### [Design Add and Search Words](https://leetcode.com/problems/design-add-and-search-words-data-structure/)

> Design a dictionary with `addWord` and `search`, where a `.` in a search matches any one letter.

```mermaid
%%{init: {"flowchart": {"padding": 18, "nodeSpacing": 22, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TD
    subgraph T ["search(“.ad”) matches bad, dad and mad   (“.” = any one letter)"]
        direction TB
        root(["root"])
        n0(("b"))
        n1(("d"))
        n2(("m"))
        n3(("a"))
        n4(("a"))
        n5(("a"))
        n6(("d"))
        n7(("d"))
        n8(("d"))
        root --- n0
        root --- n1
        root --- n2
        n0 --- n3
        n1 --- n4
        n2 --- n5
        n3 --- n6
        n4 --- n7
        n5 --- n8
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
    classDef hg fill:#e8f5e9,stroke:#e65100,stroke-width:3px,color:#1b5e20
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class root a
    class n0,n1,n2,n3,n4,n5 hi
    class n6,n7,n8 hg
    style T fill:#fafafa,stroke:#bdbdbd,color:#37474f
    linkStyle 0 stroke:#e65100,stroke-width:4px
    linkStyle 1 stroke:#e65100,stroke-width:4px
    linkStyle 2 stroke:#e65100,stroke-width:4px
    linkStyle 3 stroke:#e65100,stroke-width:4px
    linkStyle 4 stroke:#e65100,stroke-width:4px
    linkStyle 5 stroke:#e65100,stroke-width:4px
    linkStyle 6 stroke:#e65100,stroke-width:4px
    linkStyle 7 stroke:#e65100,stroke-width:4px
    linkStyle 8 stroke:#e65100,stroke-width:4px
```

**Key intuition 1:** Insert is identical to the plain trie. Only search changes: a normal letter follows one child.

**Key intuition 2:** A '.' wildcard could be ANY letter, so try every child (recursion/DFS). The trie keeps this fast because a dead path is abandoned immediately.

<details><summary markdown="span">Execute!</summary>

```python
class WordDictionary:
    def __init__(self):
        self.root = {}

    def addWord(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word: str) -> bool:
        def dfs(node, i):
            if i == len(word):
                return "$" in node
            ch = word[i]
            # any letter: try every branch
            if ch == ".":
                return any(dfs(child, i + 1) for key, child in node.items() if key != "$")
            return ch in node and dfs(node[ch], i + 1)

        return dfs(self.root, 0)
```

</details>
<BR>

## Harder: come back to these

### [Word Search II](https://leetcode.com/problems/word-search-ii/)

> Given a board of letters and a list of words, find every word that can be traced through neighboring cells (up, down, left, right), using each cell at most once per word.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 24, "rankSpacing": 50, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "24px"}}}%%
flowchart LR
    subgraph A ["Board"]
        direction TB
        grid["<b>o   a   t</b><br/><b>x   e   h</b>"]
    end
    subgraph B ["Words"]
        direction TB
        w1(["<b>oath</b>  found"])
        w2(["<b>eat</b>  found"])
        w3(["<b>pea</b>  not found"])
        w1 ~~~ w2
        w2 ~~~ w3
    end
    A ==>|"trace a word through<br/>neighbors (up, down,<br/>left, right), no cell<br/>used twice"| B
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
    class grid n
    class w1,w2 g
    class w3 r
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Searching every word separately repeats the same work. Put all the words in ONE trie and run a single DFS over the grid, following only paths that are still a prefix of some word.

**Key intuition 2:** If the current path is not a prefix of any word, stop: that is the pruning that makes it fast. When a word ends, record it and remove it so it is found once.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionWS2:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = {}
        for word in words:
            node = root
            for ch in word:
                node = node.setdefault(ch, {})
            # keep the whole word at its last letter
            node["$"] = word

        found = []

        def dfs(r, c, node):
            ch = board[r][c]
            if ch not in node:
                return
            nxt = node[ch]
            if "$" in nxt:
                # take each word only once
                found.append(nxt.pop("$"))
            # this cell is used on the current path
            board[r][c] = "#"
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr = r + dr
                nc = c + dc
                if 0 <= nr < len(board) and 0 <= nc < len(board[0]):
                    dfs(nr, nc, nxt)
            board[r][c] = ch
            if not nxt:
                # nothing left below this letter: prune it
                node.pop(ch)

        for r in range(len(board)):
            for c in range(len(board[0])):
                dfs(r, c, root)
        return found
```

</details>
<BR>

### [Word Break](https://leetcode.com/problems/word-break/)

> Can the string `s` be split into one or more words from the dictionary? Words can be reused.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 10, "rankSpacing": 40, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph A ["Dictionary"]
        direction LR
        d1(["<b>leet</b>"])
        d2(["<b>code</b>"])
        d3(["<b>cat</b>"])
        d1 ~~~ d2
        d2 ~~~ d3
    end
    subgraph B ["“leetcode” can be split: true"]
        direction LR
        s1(["<b>leet</b>"])
        s2(["<b>code</b>"])
        s1 --> s2
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
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class d1,s1 a
    class d2,s2 g
    class d3 n
    style A fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style B fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Ask: "is s[i:] splittable?" for every start i. Remember the answer so each position is solved once (dynamic programming).

**Key intuition 2:** From position i, the trie tells you every dictionary word that starts there, so you only try real words instead of every substring.

<details><summary markdown="span">Execute!</summary>

```python
from functools import lru_cache

# the trie builder from the top of this page
def build(words):
    root = {}
    for word in words:
        node = root
        for ch in word:
            # step down; create the letter if it is new
            node = node.setdefault(ch, {})
        # a word ends here
        node["$"] = True
    return root

class SolutionBreak:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        root = build(wordDict)

        @lru_cache(None)
        def solve(start):
            if start == len(s):
                return True
            node = root
            for i in range(start, len(s)):
                if s[i] not in node:
                    return False
                node = node[s[i]]
                # a word ends here: can the rest be split?
                if "$" in node and solve(i + 1):
                    return True
            return False

        return solve(0)
```

</details>
<BR>
