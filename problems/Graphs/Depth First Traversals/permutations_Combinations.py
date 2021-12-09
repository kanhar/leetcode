"""
Given two integers n and k, return all possible combinations of k numbers out of 1 ... n.

Example:

Input: n = 4, k = 2
Output:
[
  [2,4],
  [3,4],
  [2,3],
  [1,2],
  [1,3],
  [1,4],
]

TLE but analog with Permutations.
Ref: https://leetcode.com/problems/combinations/
"""
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def perm(arr, accum = [], visited = set()):
            if len(accum) == k:
                accum.sort()
                self.res[tuple(accum)] +=1
            else:
                for i in range(len(arr)):
                    if i not in visited:
                        perm(arr, accum + [arr[i]], visited | set([i]))

        self.res= collections.defaultdict(int)
        arr = [str(x) for x in range(1,n+1)]
        perm(arr)
        return self.res.keys()

"""
This one does not TLE. Same as above. TBD: Why? What is the range condition? 
"""
class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        def dfs(arr, accum , idx):
            if len(accum) == k:
                self.res.append(accum)
            else:
                for i in range(idx, len(arr) - (k - len(accum))+1 ):
                    dfs(arr, accum+[arr[i]], i+1)

        self.res = []
        arr = [i for i in range(1,n+1)]
        dfs(arr,[], 0)
        return self.res

