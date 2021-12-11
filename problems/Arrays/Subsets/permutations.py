"""
Given a collection of distinct integers, return all possible permutations.
Example:

Input: [1,2,3]
Output:
[
  [1,2,3],
  [1,3,2],
  [2,1,3],
  [2,3,1],
  [3,1,2],
  [3,2,1]
]

#Ref: https://leetcode.com/problems/permutations/

Note: Solution is position dependent, hence value independent. Also works if there are duplicates like below:
Ref: https://leetcode.com/problems/permutations-ii/
"""

class Solution(object):
    def permute(self, arr: List[int]) -> List[List[int]]:
        def perm(arr, accum = [], visited = set()):
            if len(accum) == len(arr):
                self.res.add(tuple(accum))
            else:
                for i in range(len(arr)):
                    if i not in visited:
                        perm(arr, accum + [arr[i]], visited | set([i]))

        self.res = set()
        perm(arr)
        return self.res