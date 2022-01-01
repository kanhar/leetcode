{::options parse_block_html="true" /}

{: .no_toc}
# Heaps
This is a Heap. Practise here: [Heaps](https://leetcode.com/list?selectedList=9duvlo7t)

1. TOC
{:toc}

## Kth Largest Element

> Find the kth largest element in an unsorted sort. Note that it is the kth largest element in the sorted order, not the kth distinct element.
Input: [3,2,1,5,6,4] and k = 2. Output: 5. [Leetcode](https://leetcode.com/problems/kth-largest-element-in-an-array/)

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
<br/>


## Median Sliding

> Median is the middle value in an ordered integer list.
If the size of the list is even, there is no middle value.
So the median is the mean of the two middle value. <BR>
> Design a data structure that supports the following two operations:
> void addNum(int num) - Add a integer number from the data stream to the data structure.
> double findMedian() - Return the median of all elements so far.
> [2,3,4], the median is 3<BR>
> [2,3], the median is (2 + 3) / 2 = 2.5

Ref: https://leetcode.com/problems/find-median-from-data-stream/

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
<br/>

