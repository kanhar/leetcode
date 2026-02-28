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
        def solve(tmp, open, closed):
            if len(tmp) == 2 * n:
                res.append(tmp)
                return
            
            if open<n:
                solve(tmp + "(", open+1, closed)
            if closed<open:
                solve(tmp + ")", open, closed+1)
                # N.B: No pop needed because implicitly tmp is immutable and the pop is implicit   
        res = []
        solve("", 0, 0)
        return res

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

### [Subsets](https://leetcode.com/problems/subsets/)

>> Inp: [1,2,3]
>> Out: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        def solve(tmp, i):
            # Base Case: When we've looked at every number in nums
            if i == len(nums):
                res.append(tmp)
                return
            
            # Decision 1: Include nums[i]
            # (tmp + [nums[i]] creates a NEW list, so no pop needed)
            solve(tmp + [nums[i]], i + 1)
            
            # Decision 2: Exclude nums[i]
            # (We pass the existing tmp as-is)
            solve(tmp, i + 1)
            
            # N.B: No pop needed because tmp + [...] is a new object
            # and the "pop" is implicit when the function returns.

        res = []
        solve([], 0)
        return res

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

### [Permutations](https://leetcode.com/problems/permutations/description/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []

        def solve(tmp, remaining):
            # Base Case: No numbers left to pick
            if not remaining:
                res.append(tmp)
                return
            
            # Decision: Try every available number in 'remaining'
            for i in range(len(remaining)):
                # Pick the number at index i
                pick = remaining[i]
                
                # Create a new 'remaining' list without the number we just picked
                others = remaining[:i] + remaining[i+1:]
                
                # RECURSE: tmp + [pick] creates a NEW list, so no pop needed
                solve(tmp + [pick], others)

        solve([], nums)
        return res
```

</details>
<BR>

### [Combinations](https://leetcode.com/problems/combinations/description/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []

        def solve(tmp, start):
            # Base Case: If the current combination reaches length k
            if len(tmp) == k:
                res.append(tmp)
                return
            
            # Decision: Try every number from 'start' up to 'n'
            # (We use n + 1 because range is exclusive)
            for i in range(start, n + 1):
                # RECURSE: tmp + [i] creates a NEW list.
                # We pass i + 1 so the next call only picks larger numbers.
                solve(tmp + [i], i + 1)
            
            # N.B: No pop needed because tmp + [i] is a new object.

        # Start with an empty list and begin picking from number 1
        solve([], 1)
        return res
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
        if not digits:
            return []

        mapping = {'1': '', '2': "abc", '3': "def", '4': "ghi", '5': "jkl", '6': "mno", '7': "pqrs", '8': "tuv", '9': 'wxyz' }
        res = []

        def solve(tmp, i):
            # Base Case: When we've picked a letter for every digit
            if i == len(digits):
                res.append(tmp)
                return
            
            # Identify the letters for the current digit (e.g., '2' -> "abc")
            letters = mapping[digits[i]]
            
            # Decision: Try every possible letter for this digit
            for char in letters:
                # tmp + char creates a NEW string, so no pop is needed
                solve(tmp + char, i + 1)

        solve("", 0)
        return res

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

