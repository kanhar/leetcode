{: .no_toc}
# Inductive Construction
These solutions all follow a Breadth-First Search (BFS) strategy on a state-space tree, where Level 0 is the empty starting point, Level 1 contains all possibilities using one element, and Level 2 expands to all possibilities using two elements.

Practise here: [Leetcode](https://leetcode.com/list?selectedList=9lu7fe4c)

- TOC
{:toc}

### [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)

> Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = {"()"} 
        
        for _ in range(n - 1):
            tmp = set()
            for s in res:
                for i in range(len(s)):
                    tmp.add(s[:i] + "()" + s[i:])
            res = tmp
            
        return list(res)
```

</details>
<BR>

### [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

> Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not len(digits):
            return []

        mapping = {'1': '', '2': "abc", '3': "def", '4': "ghi", '5': "jkl", '6': "mno", '7': "pqrs", '8': "tuv", '9': 'wxyz' }
        res = ['']

        for d in digits:
            tmp = []
            for c in mapping[d]:
                for r in res:
                    tmp.append(r + c)
            res = tmp

        return res
```
</details>
<BR>


### [Subsets](https://leetcode.com/problems/subsets/)

>> Inp: [1,2,3]
>> Out: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = [[]]

        for n in nums:
            tmp = []
            for r in res:
                tmp.append(r+[n])
            res += tmp

        return res
```

</details>
<BR>

