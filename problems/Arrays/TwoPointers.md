{: .no_toc}
# Two Pointers
Practise here: [Leetcode](https://leetcode.com/tag/two-pointers/)

Use two indexes instead of one nested loop. Put them at the two ends and move them inward, or have one run ahead of the other. It works when moving a pointer lets you safely rule something out, which is usually because the data is sorted or symmetric. It turns O(n²) into O(n).

Related: sliding windows (a pair of pointers that expands and shrinks) and fast/slow pointers on Linked Lists.

- TOC
{:toc}

### [Valid Palindrome](https://leetcode.com/problems/valid-palindrome/)

> Ignoring case and non-alphanumeric characters, is the string a palindrome?

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Two pointers move inward, skipping punctuation"]
        direction LR
        F0_0["<b>A</b>"]
        F0_1["<b>m…</b>"]
        F0_2["<b>…</b>"]
        F0_3["<b>…m</b>"]
        F0_4["<b>A</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
    end
    subgraph F1 ["Every pair matched"]
        direction LR
        F1_0["<b>palindrome</b>"]
    end
    F0 ==>|"compare"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_2,F0_4,F1_0 n
    class F0_1,F0_3 hi
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** A palindrome matches from the outside in, so compare the first and last characters and move both inward.

**Key intuition 2:** Skip characters that do not count, but keep left < right in every inner loop so the pointers never cross.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionPal:
    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1
        while left < right:
            # skip anything that is not a letter or digit
            while left < right and not s[left].isalnum():
                left += 1
            while left < right and not s[right].isalnum():
                right -= 1
            if s[left].lower() != s[right].lower():
                return False
            left = left + 1
            right = right - 1
        return True
```

</details>
<BR>

### [Two Sum II - Input Array Is Sorted](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

> Find two numbers in a sorted array that add up to the target. Return their 1-based positions.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Sorted, target 9: left + right = 2 + 15 = 17 (too big, move right inward)"]
        direction LR
        F0_0["<b>2</b>"]
        F0_1["<b>7</b>"]
        F0_2["<b>11</b>"]
        F0_3["<b>15</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
    end
    subgraph F1 ["2 + 7 = 9"]
        direction LR
        F1_0["<b>2</b>"]
        F1_1["<b>7</b>"]
        F1_0 --> F1_1
    end
    F0 ==>|"found"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_3 hi
    class F0_1,F0_2,F1_0,F1_1 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Sorted means the sum has a direction. If the total is too small, only a bigger left number can fix it; if too big, only a smaller right number can.

**Key intuition 2:** So every step throws away one candidate for good, and the two pointers meet after at most n steps.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionTwoSum2:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            total = numbers[left] + numbers[right]
            if total == target:
                # the problem numbers positions from 1
                return [left + 1, right + 1]
            if total < target:
                # too small: only a bigger left number can help
                left += 1
            else:
                # too big: only a smaller right number can help
                right -= 1
```

</details>
<BR>

### [Remove Duplicates from Sorted Array](https://leetcode.com/problems/remove-duplicates-from-sorted-array/)

> Remove duplicates in place and return the new length.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Sorted: reader runs ahead, writer keeps the unique values"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>1</b>"]
        F0_2["<b>2</b>"]
        F0_3["<b>2</b>"]
        F0_4["<b>3</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
    end
    subgraph F1 ["First 3 slots are the answer"]
        direction LR
        F1_0["<b>1</b>"]
        F1_1["<b>2</b>"]
        F1_2["<b>3</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
    end
    F0 ==>|"return 3"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F0_3,F0_4,F1_0,F1_1,F1_2 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** One pointer reads every element; the other marks where the next unique value goes. The array is rewritten behind the reader.

**Key intuition 2:** Because it is sorted, a value is new exactly when it differs from the last one written.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionDedup:
    def removeDuplicates(self, nums: List[int]) -> int:
        # nums[:write] is the answer built so far
        write = 0
        for read in range(len(nums)):
            if write == 0 or nums[read] != nums[write - 1]:
                nums[write] = nums[read]
                write += 1
        return write
```

</details>
<BR>

### [Container With Most Water](https://leetcode.com/problems/container-with-most-water/)

> Given wall heights, pick two walls that hold the most water.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Heights: the shorter wall limits the water, so move the shorter wall"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>8</b>"]
        F0_2["<b>6</b>"]
        F0_3["<b>2</b>"]
        F0_4["<b>5</b>"]
        F0_5["<b>4</b>"]
        F0_6["<b>8</b>"]
        F0_7["<b>3</b>"]
        F0_8["<b>7</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
        F0_4 --> F0_5
        F0_5 --> F0_6
        F0_6 --> F0_7
        F0_7 --> F0_8
    end
    subgraph F1 ["Best area"]
        direction LR
        F1_0["<b>49</b>"]
    end
    F0 ==>|"max area"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_8 hi
    class F0_1,F0_2,F0_3,F0_4,F0_5,F0_6,F0_7,F1_0 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Start with the widest container. The water level is set by the shorter wall, so moving the TALLER wall inward can only make things worse (narrower, same limit).

**Key intuition 2:** So always move the shorter wall, hoping for a taller one.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionWater:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height) - 1
        best = 0
        while left < right:
            best = max(best, (right - left) * min(height[left], height[right]))
            if height[left] < height[right]:
                # the shorter wall limits the water: try a taller one
                left += 1
            else:
                right -= 1
        return best
```

</details>
<BR>

## Harder: come back to these

### [3Sum](https://leetcode.com/problems/3sum/)

> Find all unique triplets that add up to zero.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Sort, fix one number, then two pointers close in on the other two"]
        direction LR
        F0_0["<b>-4</b>"]
        F0_1["<b>-1</b>"]
        F0_2["<b>-1</b>"]
        F0_3["<b>0</b>"]
        F0_4["<b>1</b>"]
        F0_5["<b>2</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
        F0_4 --> F0_5
    end
    subgraph F1 ["Triples that sum to zero"]
        direction LR
        F1_0["<b>-1 -1 2</b>"]
        F1_1["<b>-1 0 1</b>"]
        F1_0 --> F1_1
    end
    F0 ==>|"3Sum"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F0_3,F0_4,F0_5,F1_0,F1_1 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Sort, then fix the first number. What is left is Two Sum II on the rest: two pointers close in on the pair that completes it.

**Key intuition 2:** Skip repeated values (for the first number and for the second) so each triplet is listed once.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionThreeSum:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        result = []
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i - 1]:
                # same first number as last time: skip duplicates
                continue
            left = i + 1
            right = len(nums) - 1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total < 0:
                    left += 1
                elif total > 0:
                    right -= 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        # skip duplicate second numbers
                        left += 1
        return result
```

</details>
<BR>

