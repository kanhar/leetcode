# KMP

Searching for a pattern naively restarts from scratch after every mismatch, which is O(n·m). KMP (Knuth-Morris-Pratt) never goes backwards in the text, so it is O(n + m). It is a good one to know but rarely required: most interviews accept `haystack.find(needle)` or the naive loop.

### [Knuth Morris Pratt Algorithm (KMP) - String Search](https://leetcode.com/problems/implement-strstr/)

> Implement strStr(). Return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Pattern “abab”: for each position, the length of the longest prefix that is also a suffix"]
        direction LR
        F0_0["<b>a: 0</b>"]
        F0_1["<b>b: 0</b>"]
        F0_2["<b>a: 1</b>"]
        F0_3["<b>b: 2</b>"]
        F0_0 ~~~ F0_1
        F0_1 ~~~ F0_2
        F0_2 ~~~ F0_3
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
    class F0_0,F0_1,F0_2 n
    class F0_3 g
    style F0 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** When a mismatch happens, you already know the last few characters you matched. If the end of what matched is also the start of the pattern (a prefix that is also a suffix), you can resume there instead of restarting.

**Key intuition 2:** The table ("longest proper prefix that is also a suffix" for each position) tells you exactly how far to fall back. Build it once from the pattern, then scan the text once.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:

    def indexOf(self, t, p):
        def getLongestProperPrefix(p):
            # arrarra -> [0, 0, 0, 1, 2, 3, 4]
            # amar ->    [0, 0, 1, 0]
            # aaoiaa ->  [0, 1, 0, 0, 1, 2]
            arr = [0]
            j = 0
            for i in range(1, len(p)):
                while j > 0 and p[j] != p[i]:
                    j = arr[j - 1]
                if p[j] == p[i]:
                    j += 1
                arr.append(j)
            print(arr)
            return arr

        def getMatches(t,p):
            kmp = getLongestProperPrefix(p)
            res = []
            j = 0
            for i in range(len(t)):
                while j > 0 and t[i] != p[j]:
                    j = kmp[j - 1]
                if t[i] == p[j]:
                    j += 1
                if j == len(p):
                    res.append(i - (j - 1))
                    j = kmp[j - 1]
            return res

        ans = getMatches(t,p)
        return ans if ans != [] else [-1]

    def strStr(self, string: str, pattern: str) -> int:
        return self.indexOf(string, pattern)[0] if pattern else 0
```

</details>
<BR>
