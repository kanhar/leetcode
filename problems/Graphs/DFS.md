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

### [Best time to buy and sell](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/description)

<details><summary markdown="span">Execute!</summary>

```python
def maxProfit(prices):
    # Memoization table: (index, buying_state)
    memo = {}

    def backtrack(i, buying):
        # Base case: reached the end of the price list
        if i >= len(prices):
            return 0
        
        # Check if we've already computed this state
        if (i, buying) in memo:
            return memo[(i, buying)]

        if buying:
            # Option 1: Buy today (spend money, move to next day to sell)
            buy = backtrack(i + 1, False) - prices[i]
            # Option 2: Cooldown (skip today, stay in buying state)
            cooldown = backtrack(i + 1, True)
            res = max(buy, cooldown)
        else:
            # Option 1: Sell today (gain money, skip 1 day for cooldown)
            sell = backtrack(i + 2, True) + prices[i]
            # Option 2: Cooldown (skip today, stay in selling state)
            cooldown = backtrack(i + 1, False)
            res = max(sell, cooldown)

        memo[(i, buying)] = res
        return res

    return backtrack(0, True)

# Example Usage:
# prices = [1, 2, 3, 0, 2]
# Output: 3 
```

</details>
<BR>


### [Word Search](Word Search)

> Given an m x n grid of characters board and a string word, return true if word exists in the grid.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        def backtrack(r, c, index):
            # Base Case: All characters matched
            if index == len(word):
                return True
            
            # Failure Cases: Out of bounds, wrong character, or already visited
            if (r < 0 or c < 0 or 
                r >= ROWS or c >= COLS or 
                board[r][c] != word[index]):
                return False
            
            # Step 1: Mark as visited (Backtracking Setup)
            temp = board[r][c]
            board[r][c] = "#"
            
            # Step 2: Explore neighbors
            # result will be True if any direction finds the rest of the word
            found = (backtrack(r + 1, c, index + 1) or
                     backtrack(r - 1, c, index + 1) or
                     backtrack(r, c + 1, index + 1) or
                     backtrack(r, c - 1, index + 1))
            
            # Step 3: Backtrack (Restore the cell)
            board[r][c] = temp
            
            return found

        ROWS, COLS = len(board), len(board[0])
        # Try starting the word from every single cell
        for r in range(ROWS):
            for c in range(COLS):
                if backtrack(r, c, 0):
                    return True
        
        return False
```

</details>
<BR>


### [Minimum Knight Moves](https://leetcode.com/problems/minimum-knight-moves/description)

In an infinite chess board with coordinates from -infinity to +infinity, you have a knight at square [0, 0].

Return the minimum number of steps needed to move the knight to the square [x, y]. It is guaranteed the answer exists.

Note: You can use symmetry to stick to one quadrant

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        x, y = abs(x), abs(y)
        memo = {}

        def solve(r, c):
            # We use abs() to keep the knight in the first quadrant 
            # and simplify the number of states we track.
            r, c = abs(r), abs(c)
            
            if r == x and c == y:
                return 0
            
            # If we've been here and found a shorter way, stop this branch.
            if (r, c) in memo:
                return memo[(r, c)]
            
            # If we wander too far away from the target, stop.
            # (Adding a buffer of 2 for the "swing" moves)
            if r > x + 2 or c > y + 2:
                return float('inf')

            # We mark this as 'inf' temporarily to prevent infinite loops 
            # if the knight jumps back to a square currently in the recursion stack.
            memo[(r, c)] = float('inf')

            # Standard knight moves, but we prioritize moving toward the target
            res = 1 + min(
                solve(r + 2, c + 1), solve(r + 1, c + 2),
                solve(r - 1, c + 2), solve(r - 2, c + 1),
                solve(r + 2, c - 1), solve(r + 1, c - 2)
            )
            
            memo[(r, c)] = res
            return res

        return solve(0, 0)
```

</details>
<BR>
