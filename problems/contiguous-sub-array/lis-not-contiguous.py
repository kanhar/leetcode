"""
Given an unsorted sort of integers, find the length of longest increasing subsequence.

Example:

Input: [10,9,2,5,3,7,101,18]
Output: 4
Explanation: The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

Ref: https://leetcode.com/problems/longest-increasing-subsequence/
"""

class Solution:
    def lengthOfLIS(self, arr: List[int]) -> int:
        if len(arr) == 0:
            return 0
        seq = [1]*len(arr)
        for i in range(1,len(arr)):
            for j in range(0,i):
                if arr[i]>arr[j]:
                    seq[i]=max(seq[j]+1,seq[i])
        return max(seq)


