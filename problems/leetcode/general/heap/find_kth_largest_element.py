'''
Find the kth largest element in an unsorted array. Note that it is the kth largest element in the sorted order, not the kth distinct element.

Example 1:

Input: [3,2,1,5,6,4] and k = 2
Output: 5
Example 2:

Input: [3,2,3,1,2,4,5,5,6] and k = 4
Output: 4
Note:
You may assume k is always valid, 1 ≤ k ≤ array's length.

Ref: https://leetcode.com/problems/kth-largest-element-in-an-array/
'''

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        def findnsmallset(arr, n):
            if len(arr)==1:
                return arr[0]
            if len(arr)==0:
                return -1
            P = arr[int(len(arr)/2)]
            smaller = [x for x in arr if x < P]
            bigger = [x for x in arr if x > P]
            equal = [x for x in arr if x == P]
            if n < len(smaller):
                return findnsmallset(smaller,n)
            elif len(smaller) <= n < len(smaller)+len(equal):
                return P
            else:
                return findnsmallset(bigger,n-len(smaller)-len(equal))

        def median(arr):
            m = len(arr)//2
            if len(arr)%2==1: #even
                return findnsmallset(arr,m)
            else:
                return int((findnsmallset(arr,m) + findnsmallset(arr,m-1))/2)
        return( findnsmallset(nums,len(nums)-k)  )

    def findKthLargestHeap(self, nums, k):
        import queue
        heap = queue.PriorityQueue()
        for n in nums:
            heap.put(n)

        for i in range(0,len(nums)-k):
            heap.get()

        return (heap.get() )