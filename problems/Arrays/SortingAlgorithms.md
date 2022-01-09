{: .no_toc}
# Sorting Algorithms

- TOC
{:toc}

### [Heap Sort](https://leetcode.com/problems/maximum-gap/)

> Sort an array of integers, and find the maximum gap between any two in the sorted array.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:

    def maximumGap(self, num):
        if len(num) < 2:
            return 0

        num = self.heap_sort(num)
        res = 0
        for i in range(1, len(num)):
            res = max(num[i] - num[i - 1], res)
        return res

    def heap_sort(self, arr):
        def build_heap_at_i(arr, i, size):
            left = i * 2 + 1
            rigt = i * 2 + 2

            biggerChildren = [x for x in [left, rigt] if x <= size and arr[x]> arr[i] ]
            if len(biggerChildren) != 0:
                max_i = max(biggerChildren, key=lambda x: arr[x])

                arr[i], arr[max_i] = arr[max_i], arr[i]
                build_heap_at_i(arr, max_i, size)

        def build_heap(arr):
            size = len(arr)-1
            mid  = int(size/2)
            for i in range(mid,-1,-1):
                build_heap_at_i(arr, i, size)

        def heap_sort(arr):
            size = len(arr)-1
            for i in range(size, -1, -1):
                arr[0], arr[i] = arr[i], arr[0]
                size = size - 1
                build_heap_at_i(arr, 0, size)

        def print_heap(arr,i=0,d=0):
            if i not in range(0, len(arr)):
                return
            l = i*2+1
            r = i*2+2
            print_heap(arr,l,d+1)
            print("   " * d,arr[i])
            print_heap(arr,r,d+1)

        build_heap(arr)
        heap_sort(arr)
        return arr

```

</details>
<BR>


### [Radix Sort](https://leetcode.com/problems/maximum-gap/)

> Sort an array of integers, and find the maximum gap between any two in the sorted array.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:

    def maximumGap(self, num):
        if len(num) < 2:
            return 0

        num = self.radixSort(num)

        res = 0
        for i in range(1, len(num)):
            res = max(num[i] - num[i - 1], res)
        return res

    def radixSort(self, num):
        for i in range(31):
            onebucket = []
            zerobucket = []
            needle = 1 << i
            for j in range(len(num)):
                if num[j] & needle != 0:
                    onebucket.append(num[j])
                else:
                    zerobucket.append(num[j])
            num = []
            num += zerobucket
            num += onebucket
        return num
```

</details>
<BR>

### [Quick Sort](https://leetcode.com/problems/maximum-gap/)

> Sort an array of integers, and find the maximum gap between any two in the sorted array.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:

    def maximumGap(self, num):
        if len(num) < 2:
            return 0

        num = self.qsort(num)

        res = 0
        for i in range(1, len(num)):
            res = max(num[i] - num[i - 1], res)
        return res

    def qsort(self, L):
        if L == []:
            return []

        P = L[0]
        R = L[1:]

        return self.qsort([x for x in R if x< P])+ [P] + self.qsort([x for x in R if x>=P])
```

</details>
<BR>

### [Merge Sort](https://leetcode.com/problems/maximum-gap/)

> Sort an array of integers, and find the maximum gap between any two in the sorted array.

<details><summary markdown="span">Let's see some code!</summary>

```python
```

</details>
<BR>


### [Quick Select - Nth Smallest / Median / Percentile](https://leetcode.com/problems/kth-largest-element-in-an-array/)

> Original Leetcode Problem: Find the kth largest element in an unsorted array. Note that it is the kth largest element in
the sorted order, not the kth distinct element.
> 
> However we use can this problem to test an alternative solution, leveraging the 
> [Quickselect algorithm](https://en.wikipedia.org/wiki/Quickselect), which zeroes in on the nth smallest element in log(n) time. 

> The same strategy is also very effective in calculating a Median or a Percentile.
 
<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def findnsmallset(arr, n):
            P = arr[len(arr)//2]
            
            smaller = [x for x in arr if x < P]
            equal = [x for x in arr if x == P]
            bigger = [x for x in arr if x > P]
            
            if n < len(smaller):
                return findnsmallset(smaller,n)
            elif n in range(len(smaller), len(smaller)+len(equal)):
                return P
            else:
                return findnsmallset(bigger,n-(len(smaller)+len(equal)))
          
        if len(nums)==1:
            return nums[0]
        if len(nums)==0:
            return -1
        else:
            return findnsmallset(nums,len(nums)-k)
```

```python
        def median(arr):
            m = len(arr)//2
            if len(arr)%2==1: 
                return findnsmallset(arr,m)
            else:
                return (findnsmallset(arr,m) + findnsmallset(arr,m-1))//2
```

</details>
<BR>