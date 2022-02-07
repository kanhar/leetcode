{: .no_toc}
# Dynamic Programming
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9di6va53)

- TOC
{:toc}

### [Robbing Non-Adjacent Houses](https://leetcode.com/problems/house-robber/)

> Optimize for max robbery amount, should adjacent houses not be robbable. 

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def rob(self, nums: List[int]) -> int:
        h = collections.defaultdict(int)
        if len(nums) == 0:
            return 0
        elif len(nums) == 1:
            return nums[0]
        elif len(nums) == 2:
            return max(nums[0], nums[1])

        h[0] = nums[0]
        h[1] = max(nums[0], nums[1])
        for i in range(1, len(nums)):
            h[i] = max(nums[i] + h[i - 2], h[i - 1])

        return max(h.values())

class Solution:
    def rob(self, nums: List[int]) -> int:
        def solve(nums, i):
            if i < 0:
                return 0
            else:
                return max(nums[i] + solve(nums, i - 2), solve(nums, i - 1))

        return solve(nums, len(nums) - 1)

class Solution:
    def rob(self, nums: List[int]) -> int:
        def solve(nums, i):
            if i < 0:
                return 0
            elif i in memo:
                return memo[i]
            else:
                memo[i] = max( nums[i] + solve(nums, i-2), solve(nums, i-1) )
                return memo[i]

        memo = {}
        return solve(nums, len(nums)-1)
```

</details>
<BR>

### [Longest Increasing Subsequence](https://leetcode.com/problems/longest-increasing-subsequence/)

> Given an unsorted sort of integers, find the length of the longest increasing subsequence.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def lengthOfLIS(self, nums):
        h = collections.defaultdict(lambda: 1)

        h[0] = 1
        for i in range(1, len(nums)):
            for j in range(0, i):
                if nums[i] > nums[j]:
                    h[i] = max(h[i], h[j] + 1)

        return max(h.values())
```

</details>
<BR>

### [Longest Palindromic Substring](https://leetcode.com/problems/longest-palindromic-substring/)

> Given a string s, find the longest palindromic substring in s.
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

### [Maximum Length of a sub-array that sums to k](https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/)
> Given an array nums and a target value k, find the maximum length of a subarray that sums to k.
If there isn't one, return 0 instead.
> Key intuition: If total_at_i + total_at_j = k, then sum(i..j) must be k
> [Contrast with](https://leetcode.com/problems/path-sum-iii/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxSubArrayLen(self, nums: List[int], k: int) -> int:
        h = collections.defaultdict(int)
        total_at_i = 0
        maxLen = 0
        for i in range(0, len(nums)):
            total_at_i += nums[i]
            if total_at_i not in h:
                h[total_at_i] = i

            total_at_j = total_at_i - k
            if total_at_i == k:
                maxLen = max(maxLen, i - 0 + 1)
            elif total_at_j in h:
                maxLen = max(maxLen, i - h[total_at_j])

        return maxLen
```
</details>
<br/>

### [Maximum Sub-array Sum](https://leetcode.com/problems/maximum-subarray/)

> Given an integer array, find the contiguous subarray which has the largest sum. 

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxSubArray(self, arr: List[int]) -> int:
        h = collections.defaultdict(int)
        for i in range(0, len(arr)):
            if i==0:
                h[i] = arr[i]
            else:
                h[i] = max(arr[i], h[i-1]+arr[i])

        return max(h.values())

    #Explanation
    def maxSubArray(self, n)-> int:
        max_so_far = n[0]
        elements_so_far = [max_so_far]
        for x in n[1:]:
            if x > sum(elements_so_far + [x]):
                elements_so_far = [x]
            else:
                elements_so_far.append(x)
            max_so_far = max(max_so_far, sum(elements_so_far))

        return max_so_far
```

</details>
<BR>

### [Pascals Triangle](https://leetcode.com/problems/pascals-triangle/)

> Given an integer numRows, return the first numRows of Pascal's triangle.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        dp = [[1]]
        for i in range(1, numRows):
            tmp = [1] * (i + 1)
            for j in range(1, i):  # First and last should not be overwritten in range 0..i+1 (== 1 to i)
                tmp[j] = dp[i - 1][j - 1] + dp[i - 1][j]
            dp = dp + [tmp]
        return dp
```

</details>
<BR>

### [Max Points in Matrix with Cost](https://leetcode.com/problems/maximum-number-of-points-with-cost/)

> Standard Dynamic programming problem. Google Onsite. 

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxPoints(self, A: List[List[int]]) -> int:

        if len(A)==0:
            return 0

        if len(A) == 1:
            return max(A)

        n = len(A)    # number of Rows
        m = len(A[0]) # number of Columns

        dp = [[0 for x in range(m)] for x in range(n) ] 

        # First row ready
        for j in range(m):
            dp[0][j] = A[0][j]

        # Second Rows on. 
        for i in range(1,n):
            for j in range(m):
                tmp = []

                for k in range(m):
                    tmp.append(dp[i-1][j] + A[i][k] - abs(k-j) )

                dp[i][j] = max(tmp)
        return max(dp[n-1])
```

</details><BR>
