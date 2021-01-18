'''
Largest Triple Products
You're given a list of n integers arr[0..(n-1)].
You must compute a list output[0..(n-1)] such that, for each index i (between 0 and n-1, inclusive), output[i] is equal
to the product of the three largest elements out of arr[0..i] (or equal to -1 if i < 2, as arr[0..i] then includes fewer than three elements).
Note that the three largest elements used to form any product may have the same values as one another, but they must be at different indices in arr.
Signature
int[] findMaxProduct(int[] arr)
Input
n is in the range [1, 100,000].
Each value arr[i] is in the range [1, 1,000].
Output
Return a list of n integers output[0..(n-1)], as described above.
Example 1
n = 5
arr = [1, 2, 3, 4, 5]
output = [-1, -1, 6, 24, 60]
The 3rd element of output is 3*2*1 = 6, the 4th is 4*3*2 = 24, and the 5th is 5*4*3 = 60.

'''
import math
import heapq
from functools import reduce

def multiply(arr):
    return reduce(lambda x,y: x*y, arr)

def findMaxProduct(arr):
    res = [-1,-1]
    if len(arr) <= 2:
        return res
    res.append(multiply(arr[:3]))

    h = arr[:3]
    heapq.heapify(h)

    for i in range(3, len(arr)):
        if arr[i] > h[0]:
            heapq.heappop(h)
            heapq.heappush(h, arr[i])

        res.append(multiply(h))

    return res


print([-1, -1, 56, 56, 140, 140] == findMaxProduct([2, 4, 7, 1, 5, 3]) )


'''
Find sliding Median
n = 4
arr = [5, 15, 1, 3]
output = [5, 10, 5, 4]
'''
import math
import heapq
def findMedian(arr):

    global lo
    global hi
    lo = []
    hi = []
    def addNum(num):
        global lo
        global hi

        heapq.heappush(lo, -num)
        heapq.heappush(hi, -heapq.heappop(lo))
        if len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))

    def findMed():
        global lo
        global hi

        if len(lo) == len(hi):
            return (-lo[0] + hi[0]) // 2
        else:
            return -lo[0]

    res = []
    for a in arr:
        addNum(a)
        res.append(findMed())

    return res

print([5, 10, 5, 4] == findMedian( [5, 15, 1, 3]))