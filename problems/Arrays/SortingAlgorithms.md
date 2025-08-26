{: .no_toc}
# Sorting Algorithms

- TOC
{:toc}

### [Heap Sort](https://leetcode.com/problems/maximum-gap/)

> Sort an array of integers, and find the maximum gap between any two in the sorted array.

<details><summary markdown="span">Execute! See better explanation [here](https://thelicato.medium.com/sorting-algorithms-in-python-heapsort-ad31323fce18)</summary>

```python
class Solution:
    def maximumGap(self, nums: List[int]) -> int:
        def max_heapify(array, n, i):
            l = (2*i)+1 # Left(i)
            r = (2*i)+2 # Right(i)
            largest=i
            if l < n and array[l] > array[largest]:
                largest = l
            if r < n and array[r] > array[largest]:
                largest = r
            if largest != i:
                array[i], array[largest] = array[largest], array[i]
                max_heapify(array, n, largest)

        def build_max_heap(array):
            n = len(array)
            for i in range((len(array)//2 + 1), -1, -1):
                max_heapify(array, n, i)

        def heapsort(array):
            build_max_heap(array)
            n = len(array)
            for i in range(n-1, 0, -1):
                array[0], array[i] = array[i], array[0]
                max_heapify(array, i, 0)

            return array    
    
        if len(nums) < 2:
            return 0

        nums = heapsort(nums)
        res = 0
        for i in range(1, len(nums)):
            res = max(nums[i] - nums[i - 1], res)
        return res
```

</details>
<BR>


### [Radix Sort](https://leetcode.com/problems/maximum-gap/)

> Sort an array of integers, and find the maximum gap between any two in the sorted array.

<details><summary markdown="span">Execute!</summary>

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

<details><summary markdown="span">Execute!</summary>

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

<details><summary markdown="span">Execute!</summary>

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
 
<details><summary markdown="span">Execute!</summary>

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

### Insertion Sort
To be implemented, also see k-messed sort.

### [Kanhar Sort! :)](https://leetcode.com/problems/maximum-gap/)

I like to jokingly call this Kanhar Sort, faster than Merge, Heap and Quick sort.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maximumGap(self, num):
        if len(num) < 2:
            return 0

        num = self.KanharSort(num)
        print(num)
        res = 0
        for i in range(1, len(num)):
            res = max(num[i] - num[i - 1], res)
        return res
    
    def KanharSort(self, nums: List[int]) -> int:
        edges = collections.defaultdict(list)
        indeg = {x: 0 for x in nums}
        
        for a,b, in zip(nums, nums[1:]):
            (a,b) = (a,b) if a <= b else (b,a)
            edges[a].append(b)
            indeg[b]+=1
    
        res = []
        h = [x for x in indeg if indeg[x] == 0] 
        heapq.heapify(h)
        while h:
            curr = heapq.heappop(h)
            res.append(curr)
            for e in edges[curr]:
                indeg[e]-=1
                if indeg[e]==0:
                    heapq.heappush(h, e)
        print(res)
        return res 
```
