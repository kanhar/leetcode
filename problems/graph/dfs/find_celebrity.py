import collections
"""
Suppose you are at a party with n people (labeled from 0 to n - 1) and among them, there may exist one celebrity. 
The definition of a celebrity is that all the other n - 1 people know him/her but he/she does not know any of them.

You are given a helper function bool knows(a, b) which tells you whether A knows B. Implement a function int findCelebrity(n). 
There will be exactly one celebrity if he/she is in the party. Return the celebrity's label if there is a celebrity in the party.

Ref: https://leetcode.com/problems/find-the-celebrity/
"""
class Solution:
    def findCelebrity(self, n: int) -> int:
        found = [0]*n
        for i in range(n):
            for j in range(n):
                if i!=j and found[i] != 1:
                    if knows(i,j):
                        found[i]=1

        for i in range(n):
            if found[i] != 1:
                notKnows = [x for x in range(n) if x != i and not knows(x,i)]
                if len(notKnows) == 0:
                    return i

        return -1