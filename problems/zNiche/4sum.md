### [4sum](https://leetcode.com/problems/4sum/)

> See also recursive way to solve this [here](https://kanhar.github.io/leetcode/problems/Arrays/TwoPointers.html#4sum)

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
