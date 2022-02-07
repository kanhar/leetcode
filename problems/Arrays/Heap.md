{::options parse_block_html="true" /}

{: .no_toc}
# Heaps
Practise here: [Heaps](https://leetcode.com/list?selectedList=9duvlo7t)

- TOC
{:toc}

### [Kth Largest Element](https://leetcode.com/problems/kth-largest-element-in-an-array/)

> Find the kth largest element in an unsorted array. 

<details><summary markdown="span">Execute!</summary>
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

<details><summary markdown="span">Execute!</summary>

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

<details><summary markdown="span">Execute!</summary>

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

</details>
<BR>