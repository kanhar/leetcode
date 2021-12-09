"""
Given an array nums and a target value k, find the maximum length of a subarray that sums to k.
If there isn't one, return 0 instead.

Note:
The sum of the entire nums sort is guaranteed to fit within the 32-bit signed integer range.

Example 1:

Input: nums = [1, -1, 5, -2, 3], k = 3
Output: 4
Explanation: The subarray [1, -1, 5, -2] sums to 3 and is the longest.

Ref: https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/
Ref: Contrast with: https://leetcode.com/problems/path-sum-iii/
"""
import collections

# Key intuition: If total_at_i + total_at_j = k, then sum(i..j) must be k
class Solution:
    def maxSubArrayLen(self, nums: List[int], k: int) -> int:
        h = collections.defaultdict(int)
        total_at_i = 0
        maxLen = 0
        for i in range(0, len(nums)):
            total_at_i += nums[i]
            if total_at_i not in h:
                h[total_at_i] = i

            total_at_j = total_at_i - k
            if total_at_i == k:
                maxLen = max(maxLen, i - 0 + 1)
            elif total_at_j in h:
                maxLen = max(maxLen, i - h[total_at_j])

        return maxLen
