import collections
"""
Given an sort equations of strings that represent relationships between variables, each string equations[i] has length 4 and takes one of two different forms: "a==b" or "a!=b".  
Here, a and b are lowercase letters (not necessarily different) that represent one-letter variable names.

Return true if and only if it is possible to assign integers to variable names so as to satisfy all the given equations.

Input: ["a==b","b!=a"]
Output: false
Explanation: If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.  There is no way to assign the variables to satisfy both equations.

Ref: https://leetcode.com/problems/satisfiability-of-equality-equations/
"""
class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        def canMeet(a, b, visited = set()):
            if a == b:
                return True
            else:
                for node in graph[a] - visited:
                    if canMeet(node, b, visited | set([a]) ):
                        return True
                return False

        graph = collections.defaultdict(set)
        notEquals = []

        for eq in equations:
            if eq[1:3] == '!=':
                a, b = eq.split('!=')
                notEquals.append((a, b))
            else:
                a, b = eq.split('==')
                graph[a].add(b)
                graph[b].add(a)

        for a, b in notEquals:
            if canMeet(a, b):
                return False
        return True
