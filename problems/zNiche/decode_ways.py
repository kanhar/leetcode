"""
A message containing letters from A-Z is being encoded to numbers using the following mapping:
'A' -> 1 'B' -> 2 .. 'Z' -> 26
Given a non-empty string containing only digits, determine the total number of ways to decode it.
Input: "226"
Output: 3. Explanation: It could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
Input: 100: Output: 0 (this is an important edge case, that it is not 1 )

Ref: https://leetcode.com/problems/decode-ways/
"""

class Solution:
    def numDecodings(self, s: str) -> int:
        if not s:
            return 0
        
        memo = {}

        def solve(index):
            # Base Case: If we've reached the end of the string, we found 1 valid path
            if index == len(s):
                return 1
            
            # If we've already calculated the ways from this index, return it
            if index in memo:
                return memo[index]

            # A string starting with '0' cannot be decoded
            if s[index] == '0':
                return 0

            # Option 1: Decode a single digit
            # We move forward by 1 index
            res = solve(index + 1)

            # Option 2: Decode two digits
            # Check if there's enough string left and if it's between 10 and 26
            if index + 1 < len(s):
                two_digit = int(s[index : index + 2])
                if 10 <= two_digit <= 26:
                    res += solve(index + 2)

            # Store in memo and return
            memo[index] = res
            return res

        return solve(0)


