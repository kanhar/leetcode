{: .no_toc}
# Sliding Window
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9di1s4a1)

- TOC
{:toc}

### [Flower Bed Placement](https://leetcode.com/problems/can-place-flowers/)

> Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty,
and an integer n, return if n new flowers can be planted in the flowerbed without violating the
no-adjacent-flowers rule.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def canPlaceFlowers(self, f: List[int], n: int) -> bool:
        for i in range(0, len(f)):
            a = 0 if i == 0 else f[i - 1]
            b = f[i]
            c = 0 if i == len(f) - 1 else f[i + 1]

            if a == b == c == 0:
                f[i] = 1
                n -= 1

        return n <= 0

```

</details>
<BR>

### [Longest Substring without repeating characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

> Given a string, find the length of the longest substring without repeating characters.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        h = collections.defaultdict(int)
        left = 0
        maxL = 0
        for i, c in enumerate(s):
            h[c]+=1

            while h[c] > 1:
                h[s[left]]-=1
                left+=1

            maxL = max(maxL, i-left + 1)

        return maxL
```

</details>
<BR>

### [Minimum Window Substring](https://leetcode.com/problems/minimum-window-substring/)

> Given two strings s and t of lengths m and n respectively, return the minimum window substring of 
> s such that every character in t (including duplicates) is included in the window.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):  
    def minWindow(self, s, t):
        need = collections.Counter(t)
        missing = len(t)
        
        # Initialize with a string longer than s so the first window always fits
        min_chr = s + " " 
        left = 0
        for i, c in enumerate(s):
            if need[c] > 0:
                missing -= 1
            need[c] -= 1
            
            while missing == 0:                
                if i - left + 1 < len(min_chr):
                    min_chr = s[left:i+1]
                
                need[s[left]] += 1
                if need[s[left]] > 0:
                    missing += 1           
                left += 1        
        
        # If min_chr is still longer than s, no window was found
        return min_chr if len(min_chr) <= len(s) else ""
```
</details>
<BR>



### [Permutation in String](https://leetcode.com/problems/permutation-in-string/description)

Given two strings s1 and s2, return true if s2 contains a permutation of s1, or false otherwise.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def checkInclusion(self, s1, s2):
        # s1 is like 't', s2 is like 's'
        need = collections.Counter(s1)
        missing = len(s1)
        
        left = 0

        for i, c in enumerate(s2):
            if need[c] > 0:
                missing -= 1
            need[c] -= 1

            if i - left + 1 > len(s1):
                if need[s2[left]] >= 0:
                    missing += 1
                need[s2[left]] += 1
                left += 1
            
            # 3. If missing is 0 and window is exactly len(s1) we found a permutation
            if missing == 0:
                return True
                
        return False
```
</details>
<BR>

### [Subarray Product less than K](https://leetcode.com/problems/subarray-product-less-than-k)

Given an array of integers nums and an integer k, return the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than k.

Can also be solved using [backtracking](https://kanhar.github.io/leetcode/problems/Graphs/DFS.html#subarray-product-less-than-k) but inefficent 

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        # If k is 0 or 1, no product of positive integers can be < k
        if k <= 1:
            return 0
        
        current_prod = 1
        left = 0
        count = 0
        
        for i, num in enumerate(nums):
            # Equivalent to hsh[s[i]] += 1: Add the new number to the window
            current_prod *= nums[i]
            
            # Equivalent to while hsh[s[i]] > 1: Shrink until product is valid
            while current_prod >= k:
                current_prod //= nums[left]
                left += 1
            
            # Instead of maxL, we add the number of valid subarrays ending at 'i'
            # Each element in the current window [left...i] is a new valid subarray
            count += (i - left + 1)
        
        return count
```

</details>
<BR>

### [Max Consecutive Ones](https://leetcode.com/problems/max-consecutive-ones-ii/)

> Given a binary array, find the maximum number of consecutive 1s in this sort if you can flip at most one 0.
> Key Intuition: Look for a sliding window with 1 zero, if 2 zeroes found, remove first zero found
<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        maxL = 0

        left = 0
        zeroes = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                zeroes += 1

            # Flipping a zero is equivalent to ignore a zero
            while zeroes >= 2:
                if nums[left] == 0:
                    zeroes -= 1
                left += 1

            maxL = max(maxL, i - left + 1)

        return maxL
```

</details>
<BR>

### [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)
> Given an array of n positive integers and a positive integer s, find the minimal length of a
contiguous subarray of which the sum ≥ s. If there isn't one, return 0 instead.
 
<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        left = 0
        minLength = float('inf')
        currSum = 0
        for i in range(len(nums)):
            currSum += nums[i]

            while currSum >= target:
                if currSum >= target:
                    minLength = min(minLength, i - left + 1)

                currSum -= nums[left]
                left += 1

        if minLength == float('inf'):
            return 0
        else:
            return minLength
```
</details>
<BR>

### [Remove duplicates from Sorted array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

> Remove duplicates in-place in a sorted array.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def removeDuplicates(self, nums):
        if len(nums)==0:
            return 0
        else:
            idx = 1
            for i in range(1, len(nums)):
                if nums[i] == nums[i-1]:
                    continue
                else:
                    nums[idx] = nums[i]
                    idx +=1
            return idx
```

</details>
<BR>


### Sliding window of K that is partially sorted

> Given an array of integers arr where each element is at most k places away from its sorted position, code an efficient function sortKMessedArray that sorts arr. For instance, for an input array of size 10 and k = 2, an element belonging to index 6 in the sorted array will be located at either index 4, 5, 6, 7 or 8 in the input array.

> Arr = [1, 4, 5, 2, 3, 7, 8, 6, 10, 9], k = 2

<details><summary markdown="span">Execute!</summary>

Solution using Heaps
```python
import heapq
def sort_k_messed_array(arr, k):
  if k>len(arr):
    return
  
  h = []
  for i in range(k):
    heapq.heappush(h, arr[i])

  res = []
  for i in range(k, len(arr)):
    heapq.heappush(h, arr[i])
    res.append(heapq.heappop(h))
  
  while h:
    res.append(heapq.heappop(h))
    
  return res
  
  # Correctness Check
  # 1, 4
  # 1, 4, 5   H = [1]
  # 4, 5, 2   H = [2]  
```
</details>
<BR>

<details><summary markdown="span">Execute!</summary>
Solution Using Insertion Sort. To be coded. <BR>
Intuition: Take a slice, find minimum element in O(k), place it. Make n steps -> O(n*k)
```python
TBD
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
