{: .no_toc}
# Strings
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xfipte)

- TOC
{:toc}

### [Group Anagrams](https://leetcode.com/problems/group-anagrams/)

> Given an array of strings, group anagrams together

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def groupAnagrams(self, wordList):
        ans = collections.defaultdict(list)
        for word in wordList:
            count = [0] * 26
            for c in word:
                count[ord(c) - ord('a')] += 1
            ans[tuple(count)].append(word)
        return ans.values()

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

### [Palindrome](https://leetcode.com/problems/valid-palindrome/)

> Valid Palindrome

<details><summary markdown="span">Execute!</summary>

```python

```

</details>
<BR>

### [String Compression](https://leetcode.com/problems/string-compression/)

> Suppose "aa" is replaced by "a2". "bb" is replaced by "b2". "ccc" is replaced by "c3".

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def compress(self, s: List[str]) -> int:
        count = 1
        res = ""
        prev = ''
        for i in range(1, len(s)):
            prev = s[i-1]
            curr = s[i]
            if curr==prev:
                count+=1
            else:
                res += prev + str(count) if count >1 else ''
                count=1

        res += prev + str(count) if count >1 else ''

        for i in range(0,len(res)):
            s[i] = res[i]

        return( len(res) )
```

</details>
<BR>