{: .no_toc}
# Two pointers

- TOC
{:toc}
  

### [4sum](https://leetcode.com/problems/4sum/)

> See also recursive way to solve this [here](https://kanhar.github.io/leetcode/problems/Graphs/DFS.html#4sum)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:

        def kSum(nums: List[int], target: int, k: int) -> List[List[int]]:
            if not nums:
                return []

            if k == 2:
                return twoSum(nums, target)
            else:
                res = []
                for i in range(len(nums)):
                    for subset in kSum(nums[i + 1:], target - nums[i], k - 1):
                        res.append([nums[i]] + subset)

            return res

        def twoSum(nums: List[int], target: int) -> List[List[int]]:
            res = []
            lo, hi = 0, len(nums) - 1

            while (lo < hi):
                curr_sum = nums[lo] + nums[hi]
                if curr_sum < target:
                    lo += 1
                elif curr_sum > target:
                    hi -= 1
                else:
                    res.append([nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1

            return res

        nums.sort()
        return set([tuple(x) for x in kSum(nums, target, 4)])
```

</details>
<BR>

### [Container with Max Water](https://leetcode.com/problems/container-with-most-water/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        
        l = 0
        r = len(height)-1
        maxarea = 0
        while l<r:
            maxarea = max(maxarea, (r-l)*min(height[l], height[r]) )
            if height[l]<height[r]:
                l+=1
            else:
                r-=1
        
        return maxarea
```

</details>
<BR>
