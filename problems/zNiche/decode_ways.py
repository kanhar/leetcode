"""
A message containing letters from A-Z is being encoded to numbers using the following mapping:
'A' -> 1 'B' -> 2 .. 'Z' -> 26
Given a non-empty string containing only digits, determine the total number of ways to decode it.
Input: "226"
Output: 3. Explanation: It could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).
Input: 100: Output: 0 (this is an important edge case, that it is not 1 )

Ref: https://leetcode.com/problems/decode-ways/
"""

def memoize(f):
    memo = {}
    def wrapper(*args):
        if args not in memo:
            memo[args] = f(*args)
        return memo[args]
    return wrapper

class Solution(object):
    def numDecodings(self, s: str) -> int:
        return 0 if not s else self.solve(s)

    @memoize
    def solve(self, s) -> int:
        if len(s)==0:
            return 1
        elif len(s)==1:
            return 1 if s[0] != '0' else 0
        else:
            if s[0] == '0':
                return 0
            else:
                #two ways to break up a sequence of[abc]: (a,bc) + (ab,c)
                return self.solve(s[1:]) + \
                       (self.solve(s[2:]) if len(s)>1 and int(s[0:2]) in range( 1, 27 ) else 0)


