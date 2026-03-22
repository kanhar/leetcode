{: .no_toc}
# Backtracking

Backtracking (a specific form of Depth-First Search), used to explore a Decision Tree where each level of the tree represents a choice.

In every problem here we build a solution one piece at a time. At each step, we ask: "What are my valid options right now?"

* Subsets: At each number, do I Include it or Exclude it?
* Permutations: Which of the remaining numbers should I swap into the current position?
* Generate Parentheses: Can I add an '('? Can I add a ')'?
* Phone Digits: Which letter from the current digit's mapping should I pick?

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
            
            # Key Intuition: [1] subsets [] (don't include) and [1] (include). Solution Mirrors this structure
            
            # Include nums[i]            
            solve(tmp + [nums[i]], i + 1)
            
            # Exclude nums[i]            
            solve(tmp, i + 1)
            
        res = []
        solve([], 0)
        return res
```

</details>
<BR>

### [Combinations](https://leetcode.com/problems/combinations/description/)

<details><summary markdown="span">Execute!</summary>

To transition from Subsets to Combinations (specifically "Combinations of size $k$"), the logic remains almost identical to your "Include/Exclude" pattern.The main difference is the stopping condition: instead of waiting until you've looked at every number, you stop as soon as your tmp list reaches the required size $k$.

```python
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        
        def solve(tmp, i):
            # Base Case 1: If we found a combination of size k, save it
            if len(tmp) == k:
                res.append(tmp[:]) # Use a copy to avoid reference issues
                return
            
            # Base Case 2: If we ran out of numbers to pick from
            if i > n:
                return
            
            # Include i
            solve(tmp + [i], i + 1)
            
            # Exclude i
            solve(tmp, i + 1)
            
        solve([], 1)
        return res
```

</details>
<BR>


### [Permutations](https://leetcode.com/problems/permutations/description/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        def backtrack(start):
            # Base Case: If the start index reaches the end, we've formed a permutation
            if start == len(nums):
                res.append(nums[:]) # Append a copy of the current state
                return

            for i in range(start, len(nums)):
                # 1. "Include" nums[i] at the current 'start' position by swapping
                nums[start], nums[i] = nums[i], nums[start]
                
                # 2. Recurse for the next position
                backtrack(start + 1)
                
                # 3. "Exclude" (Backtrack): Swap back to restore the original order
                nums[start], nums[i] = nums[i], nums[start]
        res = []
        backtrack(0)
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

```
</details>
<BR>

### [3Sum](https://leetcode.com/problems/3sum/)

Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]]
such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.

Notice that the solution set must not contain duplicate triplets.

<details><summary markdown="span">Execute!</summary>

Standard backtracking
```python
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        def solve(idx, accum):
            if len(accum) == 3:
                if sum(accum) == 0:
                    res.add(tuple(accum))
                return
            
            for i in range(idx, len(nums)):
                solve(i + 1, accum + [nums[i]])

        nums.sort() # Sorting helps handle duplicates and optimization
        res = set()                        
        solve(0, [])
        return [list(t) for t in res]
```

Backtracking with 2sum optimization

```python
class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        def twoSum(arr, target_val): 
            left = 0
            right = len(arr) - 1
            curr = [] 
            while left < right:
                total = arr[left] + arr[right]
                if total > target_val:
                    right -= 1
                elif total < target_val:
                    left += 1
                else:
                    curr.append([arr[left], arr[right]])
                    left += 1
                    right -= 1
            return curr

        def solve():
            for i, n in enumerate(nums):
                for t in twoSum(nums[i + 1:], target - n):
                    res.append([n] + t)

        nums.sort()
        res = []
        target = 0
        
        solve() 

        return [list(x) for x in set([tuple(sorted(x)) for x in res])]
```

</details>
<BR>


### [Subsequences that sum to Target](https://leetcode.com/problems/combination-sum/)

> Subsequences of numbers that sum to target

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def combinationSum(self, candidates, target):
        def solve(remain, idx, path):
            if remain == 0:
                res.append(list(path)) 
                return
            
            if remain < 0:
                return

            for i in range(idx, len(candidates)):                            
                solve(remain - candidates[i], i, path + [candidates[i]])

        res = []        
        candidates.sort() # Sort to allow for potential pruning (optimization)
        solve(target, 0, [])
        return res
```

</details>
<BR>


### [Subarray Product less than K](https://leetcode.com/problems/subarray-product-less-than-k)

Given an array of integers nums and an integer k, return the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than k.

Note: Nuance between Subsequences (for loop in backtracking ) and Subarrays (recursion moving incrementally )

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k <= 1: return 0
        
        def multiply(arr):
            if not arr: return float('inf') # Prevent empty arrays from being counted
            total = 1
            for a in arr:
                total = total * a
            return total

        def solve(idx, accum):
            current_prod = multiply(accum)
            
            if current_prod < k:
                res.append(tuple(accum))
            else:
                return 

            if idx >= len(nums):
                return

            solve(idx + 1, accum + [nums[idx]])
        
        res = list()
        
        for i in range(len(nums)):
            solve(i + 1, [nums[i]])
            
        return len(res)
```

Should ideally be solved using a  [Sliding Window](https://kanhar.github.io/leetcode/problems/Arrays/SlidingWindow.html#subarray-product-less-than-k)

</details>
<BR>
