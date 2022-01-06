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

### [Merge-k-sorted-lists](https://kanhar.github.io/leetcode/problems/Arrays/LinkedLists.html#merge-k-sorted-lists)

