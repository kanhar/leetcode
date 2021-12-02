"""

Ref: https://leetcode.com/discuss/interview-question/617596/facebook-onsite-merge-k-sorted-arrays
"""

import heapq
def solve(arr):
    h = []
    for i in range(0, len(arr)):
        heapq.heappush(h, (arr[i][0], i, 0))

    res = []
    while h:
        val, arrayNum, arrayIndex = heapq.heappop(h)
        res.append(val)

        if arrayIndex +1 < len(arr[arrayNum]):
            heapq.heappush(h, (arr[arrayNum][arrayIndex+1], arrayNum, arrayIndex+1))

    return res

arr = [ [ 1,2,3 ], [4,5,6], [0,1,2]]
print(solve(arr))