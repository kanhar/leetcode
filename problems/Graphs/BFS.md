{: .no_toc}
# Breadh First Search
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9lu7fe4c)

- TOC
{:toc}

### [Generate Parentheses](https://leetcode.com/problems/generate-parentheses/)

> Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        one = "()"
        if n == 1:
            return [one]
        else:
            tmp = []
            for r in self.generateParenthesis(n - 1):
                for i in range(len(r)):
                    tmp.append(r[:i] + one + r[i:])

            return set(tmp)


class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def solve(n):
            one='()'
            if n==1:
                return {one}
            else:
                return {res[:i]+one+res[i:] for res in solve(n-1) for i in range(len(res))}
                # For n = 2:
                #   Res = "()"
                #   For i in range(0,2)
                #       Ans = Res[:0] + () + Res[0:]
                #       Ans = None    + () + ()
                #       Ans = Res[:1] + () + Res[1:]
                #       Ans =    (    + () +    )
        return list(solve(n))


```

</details>
<BR>

### [Letter Combinations of a Phone Number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

> Given a string containing digits from 2-9 inclusive, return all possible letter
combinations that the number could represent.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if len(digits) == 0:
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

class Solution:
    def letterCombinations(self, digits):
        if not len(digits):
            return []
        else:
            mapping = {'1': '',     '2': "abc",     '3': "def", '4': "ghi", '5': "jkl", '6': "mno",  '7': "pqrs",    '8': "tuv", '9': 'wxyz'  }
            res = ['']
            for d in digits:
                res = [r + t for t in mapping[d] for r in res]
            return res
```
</details>
<BR>


### [Subsets](https://leetcode.com/problems/subsets/)

> Parse valid IP, Ipv4 and IPv6.

<details><summary markdown="span">Let's see some code!</summary>

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

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = [[]]

        for n in nums:
            res += [ r + [n] for r in res]

        return res
```

</details>
<BR>

