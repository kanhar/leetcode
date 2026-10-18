{: .no_toc}
# Strings
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xfipte)

- TOC
{:toc}

Strings are arrays of characters, so most string problems reuse array tricks: two pointers, sliding windows, and counting with a dictionary.

**Key intuition 1:** Counting letters (a dictionary or a 26-slot list) answers "same letters?" questions without sorting.

**Key intuition 2:** Python strings cannot be changed. Building a string with `+=` in a loop copies it every time; collect pieces in a list and `''.join` them once, or work in place on a list of characters.

### [Valid Anagram](https://leetcode.com/problems/valid-anagram/)

> Are two strings anagrams of each other (the same letters in a different order)?

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Same letters, same counts, different order"]
        direction LR
        F0_0["<b>l i s t e n</b>"]
        F0_1["<b>s i l e n t</b>"]
        F0_0 ~~~ F0_1
    end
    subgraph F1 ["Sorted or counted, both look the same"]
        direction LR
        F1_0["<b>e i l n s t</b>"]
    end
    F0 ==>|"count the letters"| F1
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
    class F0_0,F0_1 n
    class F1_0 hi
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Two words are anagrams exactly when they have the same count of every letter.

**Key intuition 2:** Comparing two `Counter`s is O(n), faster than sorting both strings.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionAnagram:
    def isAnagram(self, s: str, t: str) -> bool:
        # same letters with the same counts
        return collections.Counter(s) == collections.Counter(t)
```

</details>
<BR>

### [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)

> Ignoring case and non-alphanumeric characters, is the string a palindrome?

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Two pointers move inward, skipping punctuation"]
        direction LR
        F0_0["<b>A</b>"]
        F0_1["<b>m…</b>"]
        F0_2["<b>…</b>"]
        F0_3["<b>…m</b>"]
        F0_4["<b>A</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
    end
    subgraph F1 ["Every pair matched"]
        direction LR
        F1_0["<b>palindrome</b>"]
    end
    F0 ==>|"compare"| F1
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
    class F0_0,F0_2,F0_4,F1_0 n
    class F0_1,F0_3 hi
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** A palindrome matches from the outside in, so compare the first and last characters and move both inward (two pointers).

**Key intuition 2:** Skip characters that do not count, keeping left < right in the inner loops. See also [Two Pointers](../Arrays/TwoPointers.html).

<details><summary markdown="span">Execute!</summary>

```python
class SolutionPal:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            # skip anything that is not a letter or digit
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left = left + 1
            right = right - 1
        return True
```

</details>
<BR>

### [Group Anagrams](https://leetcode.com/problems/group-anagrams/)

> Given an array of strings, group anagrams together

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Words"]
        direction LR
        F0_0["<b>eat</b>"]
        F0_1["<b>tea</b>"]
        F0_2["<b>tan</b>"]
        F0_3["<b>ate</b>"]
        F0_4["<b>nat</b>"]
        F0_5["<b>bat</b>"]
        F0_0 ~~~ F0_1
        F0_1 ~~~ F0_2
        F0_2 ~~~ F0_3
        F0_3 ~~~ F0_4
        F0_4 ~~~ F0_5
    end
    subgraph F1 ["Grouped by their letter counts"]
        direction LR
        F1_0["<b>eat tea ate</b>"]
        F1_1["<b>tan nat</b>"]
        F1_2["<b>bat</b>"]
        F1_0 ~~~ F1_1
        F1_1 ~~~ F1_2
    end
    F0 ==>|"group"| F1
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
    class F0_0,F0_1,F0_2,F0_3,F0_4,F0_5,F1_0,F1_1,F1_2 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Words that are anagrams of each other have identical letter counts, so the counts make a perfect dictionary key. Put each word into the group for its key.

**Key intuition 2:** A list of 26 counts (as a tuple) is faster than sorting each word, and `sorted(word)` as the key also works.

<details><summary markdown="span">Execute!</summary>

Fix: the first version returned `ans.values()`, a view object rather than a list; it now returns `list(ans.values())`.

```python
class Solution:
    def groupAnagrams(self, wordList):
        ans = collections.defaultdict(list)
        for word in wordList:
            count = [0] * 26
            for c in word:
                count[ord(c) - ord('a')] += 1
            ans[tuple(count)].append(word)
        return list(ans.values())

import collections
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        d = collections.defaultdict(list)
        for s in strs:
            d[frozenset(collections.Counter(s).items())].append(s)
        res = []
        for k,v in d.items():
            res.append(v)
        return res
```

</details>
<BR>

### [String Compression](https://leetcode.com/problems/string-compression/)

> Replace runs of the same character with the character and the run length ("aa" becomes "a2"; a single letter stays "b"). Do it in place and return the new length.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Runs of the same letter become letter + count (a single letter stays alone)"]
        direction LR
        F0_0["<b>a</b>"]
        F0_1["<b>a</b>"]
        F0_2["<b>b</b>"]
        F0_3["<b>b</b>"]
        F0_4["<b>b</b>"]
        F0_5["<b>c</b>"]
        F0_0 ~~~ F0_1
        F0_1 ~~~ F0_2
        F0_2 ~~~ F0_3
        F0_3 ~~~ F0_4
        F0_4 ~~~ F0_5
    end
    subgraph F1 ["Written back into the same array"]
        direction LR
        F1_0["<b>a</b>"]
        F1_1["<b>2</b>"]
        F1_2["<b>b</b>"]
        F1_3["<b>3</b>"]
        F1_4["<b>c</b>"]
        F1_0 ~~~ F1_1
        F1_1 ~~~ F1_2
        F1_2 ~~~ F1_3
        F1_3 ~~~ F1_4
    end
    F0 ==>|"compress"| F1
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
    class F0_0,F0_1,F0_2,F0_3,F0_4,F0_5,F1_0,F1_1,F1_2,F1_3,F1_4 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Use two indexes: `read` finds the end of each run, `write` stores the compressed result. The output is never longer than the input, so `write` never overtakes `read`.

**Key intuition 2:** A run of 12 is written as the two characters '1' and '2', and a run of 1 gets no number at all. Bug fix: the old version dropped single letters ("abc" came out empty).

<details><summary markdown="span">Execute!</summary>

```python
class SolutionCompress:
    def compress(self, chars: List[str]) -> int:
        # where the next compressed character goes
        write = 0
        read = 0
        while read < len(chars):
            letter = chars[read]
            run = 0
            while read < len(chars) and chars[read] == letter:
                read += 1
                # count the run of equal letters
                run += 1
            chars[write] = letter
            write += 1
            if run > 1:
                # the count, one digit per slot ("12" takes two)
                for digit in str(run):
                    chars[write] = digit
                    write += 1
        # the compressed form is chars[:write]
        return write
```

</details>
<BR>

## Harder: come back to these

### [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)

> Given a string s, find the longest palindromic substring in s.
```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Expand outward from each centre while both sides match (try odd and even centres)"]
        direction LR
        F0_0["<b>b</b>"]
        F0_1["<b>a</b>"]
        F0_2["<b>b</b>"]
        F0_3["<b>a</b>"]
        F0_4["<b>d</b>"]
        F0_0 ~~~ F0_1
        F0_1 ~~~ F0_2
        F0_2 ~~~ F0_3
        F0_3 ~~~ F0_4
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
    class F0_0,F0_4 n
    class F0_1,F0_2,F0_3 hi
    style F0 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Every palindrome has a centre. Try each position as a centre (and each gap between letters, for even lengths), then expand outward while the two sides match.

**Key intuition 2:** There are 2n - 1 centres and each expansion is at most O(n), so O(n²) total, which is perfectly acceptable for an interview.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        def palindromeAt(w,l,r):
            while l>=0 and r < len(w) and w[l]==w[r]:
                l -=1
                r +=1
            return w[l+1:r]

        res = ""
        for i in range(0, len(s)):
            odd  = palindromeAt(s,i,i)
            even = palindromeAt(s,i,i+1)
            res = max([res,odd,even], key=len)
        return res
```

</details>
<BR>
