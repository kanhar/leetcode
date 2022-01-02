{: .no_toc}
# Binary Search
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xf0762)

- TOC
{:toc}

### Finding a minimum in a Rotated Sorted Array

> Suppose an array sorted in ascending order is rotated at some pivot unknown to you beforehand.
> [Leetcode](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/)

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def find_rotate_index(self, nums, left, right):
        if nums[left] <= nums[right]:  # Edge case, already sorted.
            return 0

        while left <= right:
            mid = (left + right) // 2

            if nums[mid+1] < nums[mid]:
                return mid + 1
            else:
                if nums[left] > nums[mid]:  # Left side is unsorted. This condition cannot be reversed (i.e. zone into where the problem is, not opposite )
                    right = mid - 1
                else:
                    left = mid + 1

    def findMin(self, nums: typing.List[int]) -> int:
        pivot = self.find_rotate_index(nums, 0, len(nums)-1)
        return nums[pivot]
```

</details>
<BR>

### Kth Largest Element in an Array

> Find the kth largest element in an unsorted array. Note that it is the kth largest element in
the sorted order, not the kth distinct element.
> [Leetcode](https://leetcode.com/problems/kth-largest-element-in-an-array/)
> 
<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def findnsmallset(arr, n):
            if len(arr)==1:
                return arr[0]
            if len(arr)==0:
                return -1
            P = arr[int(len(arr)/2)]
            smaller = [x for x in arr if x < P]
            bigger = [x for x in arr if x > P]
            equal = [x for x in arr if x == P]
            if n < len(smaller):
                return findnsmallset(smaller,n)
            elif len(smaller) <= n < len(smaller)+len(equal):
                return P
            else:
                return findnsmallset(bigger,n-len(smaller)-len(equal))

        def median(arr):
            m = len(arr)//2
            if len(arr)%2==1: #even
                return findnsmallset(arr,m)
            else:
                return int((findnsmallset(arr,m) + findnsmallset(arr,m-1))/2)
        return findnsmallset(nums,len(nums)-k)
```

</details>
<BR>

### Search a 2d Matrix

> Find a value in a matrix where integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row.
> [Leetcode](https://leetcode.com/problems/search-a-2d-matrix/)
<details><summary markdown="span">Let's see some code!</summary>

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
