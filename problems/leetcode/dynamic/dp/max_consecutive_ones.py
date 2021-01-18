'''
Given a binary array, find the maximum number of consecutive 1s in this array if you can flip at most one 0.

Example 1:
Input: [1,0,1,1,0]
Output: 4
Explanation: Flip the first zero will get the the maximum number of consecutive 1s.
    After flipping, the maximum number of consecutive 1s is 4.

Ref: https://leetcode.com/problems/max-consecutive-ones-ii/
'''
class Solution:
    def findMaxConsecutiveOnes(self, nums: List[int]) -> int:
        maxCnt = prev = curr = 0
        for num in nums:
            if num == 0:
                maxCnt = max(maxCnt, prev+curr+1)
                prev   = curr
                curr   = 0
            else:
                curr += 1
                maxCnt =min(max(maxCnt, prev+curr+1), len(nums))
                #if the last one is 1, we need to count it one more time
                #if all numbers are 1, it will exceed total length, so choose len(nums)
        return maxCnt
