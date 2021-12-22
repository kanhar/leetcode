"""
Given an array of distinct integers candidates and a target integer target, return a list of all unique
combinations of candidates where the chosen numbers sum to target. You may return the combinations in any order.

Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]

Ref: https://leetcode.com/problems/combination-sum/
"""

class Solution(object):
    def combinationSum(self, candidates, target):
        def solve(arr, target, idx=0, path=[]):
            if target < 0:
                return []
            elif target == 0:
                res.append(path)
            else:
                for i in range(idx, len(arr)):
                    solve(arr, target - arr[i], i, path + [arr[i]])
                return res

        res = []
        candidates.sort()
        solve(candidates, target)
        return res

