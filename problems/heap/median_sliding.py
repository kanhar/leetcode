"""
Median is the middle value in an ordered integer list. If the size of the list is even, there is no middle value. So the median is the mean of the two middle value.

For example,
[2,3,4], the median is 3

[2,3], the median is (2 + 3) / 2 = 2.5

Design a data structure that supports the following two operations:

void addNum(int num) - Add a integer number from the data stream to the data structure.
double findMedian() - Return the median of all elements so far.

Ref: https://leetcode.com/problems/find-median-from-data-stream/
"""

from heapq import heappush, heappop
class MedianFinder:
    def __init__(self):
        self.lo, self.hi = [], []

    #Shuffle:
    # add to lo
    # Add biggest number from lo to hi
    # if too many in hi, move back smallest from hi to lo.
    def addNum(self, num: int) -> None:
        heappush(self.lo, -num)
        heappush(self.hi, -heappop(self.lo))
        if len(self.hi) > len(self.lo) :
            heappush(self.lo, -heappop(self.hi))

    def findMedian(self) -> float:
        if len(self.lo) == len(self.hi):
            return (-self.lo[0] + self.hi[0]) / 2
        else:
            return -self.lo[0] #since we never let hi get bigger than lo
