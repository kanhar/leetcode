{: .no_toc}
# Sliding Window
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9di1s4a1)

- TOC
{:toc}

### [Flower Bed Placement](https://leetcode.com/problems/can-place-flowers/)

> Given an integer array flowerbed containing 0's and 1's, where 0 means empty and 1 means not empty,
and an integer n, return if n new flowers can be planted in the flowerbed without violating the
no-adjacent-flowers rule.

<details><summary markdown="span">Let's see some code!</summary>

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

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        left = 0
        hsh = collections.defaultdict(int)
        maxLen = 0

        for i in range(0, len(s)):
            hsh[s[i]] += 1

            while hsh[s[i]] > 1:
                hsh[s[left]] -= 1
                left += 1

            maxLen = max(maxLen, i - left + 1)

        return maxLen

# Length of Longest Substring with all distinct characters.  Ex: "eceba" -> "ceba" (i.e. no repeating characters)
# Length of Longest Substring with K distinct characters.    Ex: "eceba", k=2 -> "ece"
class Solution(object):
    def lengthOfLongestSubstring(self, s: str) -> int:
        r, l, distinctChars, res = 0, 0, 0, 0
        hsh = collections.defaultdict(int)

        for r in range(0, len(s)):
            hsh[s[r]] += 1
            if hsh[s[r]] == 1:
                distinctChars += 1

            # Essentially this is code to re-balance hash. Pigeon Hole principle distinct Char less than total char,
            # means duplicate
            while l <= r and r - l + 1 > distinctChars:  # Change above to distinctChars > k for k distinct characters.
                hsh[s[l]] -= 1
                if hsh[s[l]] == 0:
                    distinctChars -= 1
                l += 1

            res = max(res, r - l + 1)

        return res

```

</details>
<BR>

### [Max Consecutive Ones](https://leetcode.com/problems/max-consecutive-ones-ii/)

> Given a binary array, find the maximum number of consecutive 1s in this sort if you can flip at most one 0.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        longest_sequence = 0

        left = 0
        zeroes = 0
        for i in range(len(nums)):
            if nums[i] == 0:
                zeroes += 1

            while zeroes > 1:
                if nums[left] == 0:
                    zeroes -= 1
                left += 1

            longest_sequence = max(longest_sequence, i - left + 1)

        return longest_sequence
```

</details>
<BR>

### [Minimum Size Subarray Sum](https://leetcode.com/problems/minimum-size-subarray-sum/)
> Given an array of n positive integers and a positive integer s, find the minimal length of a
contiguous subarray of which the sum ≥ s. If there isn't one, return 0 instead.
 
<details><summary markdown="span">Let's see some code!</summary>

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

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def removeDuplicates(self, nums):
        if len(nums)==0:
            return 0
        else:
            idx = 1
            for i in range(1, len(nums)):
                if i != 0 and nums[i] != nums[i-1]: #if equal continue i
                    nums[idx] = nums[i]
                    idx +=1
            return idx
```

</details>
<BR>