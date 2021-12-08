"""
Given a set of distinct integers, nums, return all possible subsets (the power set).

Note: The solution set must not contain duplicate subsets.

Example:

Input: nums = [1,2,3]
Output:
[
  [3],
  [1],
  [2],
  [1,2,3],
  [1,3],
  [2,3],
  [1,2],
  []
]

Ref: https://leetcode.com/problems/subsets/
"""

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = [[]]

        for n in nums:
            res += [ r + [n] for r in res]

        return res

    def power_set(self, arr):
        n = len(arr)
        res = []
        for i in range( 1 << n):    # == 2^n
            tmp = []
            for j in range(n):
                if i & (1 << j ):   # == 2^j
                    tmp += [arr[j]]
            res += [tmp]
        return(res)

    #abc
#len=3 
#00 0    ""
#01 1    "a"
#10 2    "b"
#11 3    "c"

#convert to
#000 0    ""
#010 2    "a"
#100 4    "b"
#110 6    "c"

#len=8    
#000 0    
#001 1    
#010 2
#011 3
#100 4
#101 5
#110 6    
#111 7    
