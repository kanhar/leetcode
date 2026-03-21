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
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        if not nums: return 0

        h = collections.defaultdict(int)
        
        # Every element is an increasing subsequence of at least length 1
        for i in range(len(nums)):
            h[i] = 1

        for i in range(0, len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[j] > nums[i]:
                    # Update h[j] only if going through i gives a longer sequence
                    h[j] = max(h[j], h[i] + 1)
            
        return max(h.values())
```

</details>
<BR>


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


### [Total number of Subarrays with Sum Equals K](https://leetcode.com/problems/subarray-sum-equals-k/description/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        h = collections.defaultdict(int)
        # 1. Base case: a prefix sum of 0 has occurred once (before index 0)
        h[0] = 1 
        
        total_at_i = 0
        count = 0 # This will track the number of subarrays
        
        for i in range(len(nums)):
            total_at_i += nums[i]
            
            # 2. Check if (current_sum - k) exists in our history
            target = total_at_i - k
            if target in h:
                count += h[target] # Add the number of times we've seen this target
            
            # 3. Always increment the frequency of the current prefix sum
            h[total_at_i] += 1

        return count
```
</details>
<br/>


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
