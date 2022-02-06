{: .no_toc}
# Binary Search
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xf0762)

- TOC
{:toc}

### [Finding a minimum in a Rotated Sorted Array](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

> Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def findMin(self, nums: List[int]) -> int:
        def findPivot(arr, left, right):
            if left > right:
                return None
            
            mid = (left+right)//2
            
            if arr[mid+1] < arr[mid]:
                return mid+1
            else:
                if arr[left] > arr[mid]:
                    return findPivot(arr, left, mid)
                else:
                    return findPivot(arr, mid+1, right)
        
        if nums[0] < nums[~0]:          # Edge case: Already sorted
            return nums[0]
        elif len(nums)==1:
            return nums[0]
        else:
            pivot = findPivot(nums, 0, len(nums)-1)
            return nums[pivot]
```

</details>
<BR>

### [Search a 2d Matrix](https://leetcode.com/problems/search-a-2d-matrix/)

> Find a value in a matrix where integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        def bsearch(arr, left=0, right=None):
            if right is None:
                right = len(arr) - 1

            while left <= right:
                mid = (left + right) // 2
                if arr[mid] == target:
                    return True
                elif arr[mid] < target:
                    left = mid + 1
                else:
                    right = mid - 1

            return False

        if len(matrix) == 0:
            return False

        left = 0
        right = len(matrix) - 1

        while left <= right:
            mid = (left + right) // 2
            if target < matrix[mid][0]:
                right = mid - 1
            elif target > matrix[mid][-1]:
                left = mid + 1
            else:
                return bsearch(matrix[mid])
        return False
```

</details>
<BR>


### [Min.Weight for k contiguous split](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

> Divide Array into k contiguous slices, minimize max weight per slice. 
> Identical to [split-array-largest-sum](https://leetcode.com/problems/split-array-largest-sum/)

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        # Eval if an arr can be broken up into k partitions, with no partition's sum > k. 
        def feasible(arr, w, k):
            currSum = 0
            pivot = 0
            for a in arr:
                currSum +=a            
                if currSum > w:
                    pivot +=1
                    currSum = a
                    
            return pivot < k        
        
        left  = max(weights)
        right = sum(weights)
        
        while left < right:
            mid = (left+right)//2
            
            if feasible(weights,mid,days):
                right = mid
            else:
                left = mid + 1
        
        return left
```

</details>
<BR>
