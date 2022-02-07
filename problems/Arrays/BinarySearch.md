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
        # Eval if an arr can be broken up into k partitions, with no partition having sum > k. 
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
        
        while left <= right:
            mid = (left+right)//2
            
            if feasible(weights,mid,days):
                right = mid - 1
            else:
                left = mid + 1
        
        return left
```

</details>
<BR>

### [Count Nodes Complete BT](https://leetcode.com/problems/count-complete-tree-nodes/)

> Given a complete binary tree, count the number of nodes.

<details><summary markdown="span">Execute using Math</summary>

```python
class Solution(object):
    def countNodes(self, root):        
        # Note: Depth != Height
        # Perfect Complete Binary Tree - Node Count = 2^(d+1)-1. 
        # Ex: D=1, Height = 2, NodeCount = 2^2-1 = 3
        #   1
        # 2   3
        def depth(root):
            if not root:
                return 0
            return 1 + depth(root.left)
        
        def height(root):
            return 1 + depth(root)
        
        # Assumes a perfect Complete Binary Tree of Height H.
        def sumNodes(h):
            return 2**(h-1) - 1
        
        # Examples:
        # 
        #     1
        #   2   3
        # 4
        
        #       1
        #    2      3
        #  4   5  6
          
        # Core Algorithm.
        # When heights are  equal, go right
        # When heights are !equal, go left
        count = 0
        while root:
            lh = height(root.left)
            rh = height(root.right)
            if lh == rh:
                count += 1 + sumNodes(lh)
                root = root.right
            else:
                count += 1 + sumNodes(rh)
                root = root.left
        return count
        
     # Alternate Version Version
     class Solution:
        def countNodes(self, root):
            if not root:
                return 0
            leftDepth = self.getDepth(root.left)
            rightDepth = self.getDepth(root.right)
            if leftDepth == rightDepth:
                return pow(2, leftDepth) + self.countNodes(root.right)
            else:
                return pow(2, rightDepth) + self.countNodes(root.left)
    
        def getDepth(self, root):
            if not root:
                return 0
            return 1 + self.getDepth(root.left)
```
</details>
<BR>

<details><summary markdown="span">Execute using Binary Search</summary>

```python
class Solution:
    def compute_depth(self, node: TreeNode) -> int:
        d = 0
        while node.left:
            node = node.left
            d += 1
        return d
    
    # Last level nodes are enumerated from 0 to 2**d - 1 (left -> right).
    def exists(self, idx: int, d: int, node: TreeNode) -> bool:
        left, right = 0, 2**d - 1
        for _ in range(d):
            pivot = (left+right)//2
            if idx <= pivot:
                node = node.left
                right = pivot
            else:
                node = node.right
                left = pivot + 1
        return node is not None
        
    def countNodes(self, root: TreeNode) -> int:
        # if the tree is empty
        if not root:
            return 0
        
        d = self.compute_depth(root)
        # Last level nodes are enumerated from 0 to 2**d - 1 (left -> right).
        left, right = 1, 2**d - 1
        while left <= right:
            pivot = (left+right)//2
            if self.exists(pivot, d, root):
                left = pivot + 1
            else:
                right = pivot - 1
        
        # The tree contains 2**d - 1 nodes on the first (d - 1) levels
        # and left nodes on the last level.
        return (2**d - 1) + left
```
</details>
<BR>

