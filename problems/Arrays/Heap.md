{::options parse_block_html="true" /}

{: .no_toc}
# Heaps
Practise here: [Heaps](https://leetcode.com/list?selectedList=9duvlo7t)

- TOC
{:toc}

### [Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/)

> Find the kth largest element in an unsorted array. 

<details><summary markdown="span">Let's see some code!</summary>
```python
    import heapq
    class Solution:
        def findKthLargest(self, nums, k):
            h = []
            for n in nums:
                heapq.heappush(h, -n)
            i = 1
            tmp = None
            while i <= k:
                tmp = -heapq.heappop(h)
                i += 1    
            return tmp
```
And voila it now works
</details>
<BR>

### [Median Sliding](https://leetcode.com/problems/find-median-from-data-stream/)

> Design a data structure that allows ingestion of numbers, and can in O(1) time
> return the median. 

<details><summary markdown="span">Let's see some code!</summary>

```python
import heapq

class MedianFinder:
    # Heaps by default are MinHeaps. Unless you use negation
    def __init__(self):
        self.maxHeap = []
        self.minHeap = []

    def addNum(self, num: int) -> None:
        heapq.heappush(self.maxHeap, -num)
        heapq.heappush(self.minHeap, -heapq.heappop(self.maxHeap))

        if len(self.minHeap) > len(self.maxHeap):
            heapq.heappush(self.maxHeap, -heapq.heappop(self.minHeap))

    def findMedian(self) -> float:
        if len(self.minHeap) == len(self.maxHeap):
            return (-self.maxHeap[0] + self.minHeap[0]) / 2
        else:
            return -self.maxHeap[0]
```
</details>
<BR>

### Merge k Sorted Arrays

> See also: [Merge-k-sorted-linked-lists](https://kanhar.github.io/leetcode/problems/Arrays/LinkedLists.html#merge-k-sorted-lists)

```python
def merge_k_way(lists):
    import heapq
    heap  = [(l[0],i,0) for i,l in enumerate(lists) if len(l)> 0 ]
    heapq.heapify(heap)

    res = []
    while heap:
        smallest,k,i = heapq.heappop(heap)
        res.append(smallest)
        
        #Add new smallest from list K, at index i
        if i < len(lists[k])-1: 
            heapq.heappush(heap,(lists[k][i+1],k,i+1))

    return(res)
```

```python
merge_k_way([1,2,3], [4,5,6]) # Returns [1,2,3,4,5,6]
```

### K-Messed Sort

> Given an array of integers arr where each element is at most k places away from its sorted position, code an efficient function sortKMessedArray that sorts arr. For instance, for an input array of size 10 and k = 2, an element belonging to index 6 in the sorted array will be located at either index 4, 5, 6, 7 or 8 in the input array.

> Arr = [1, 4, 5, 2, 3, 7, 8, 6, 10, 9], k = 2 

> Out = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
<details><summary markdown="span">Let's see some code!</summary>

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