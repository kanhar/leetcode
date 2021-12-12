"""
There are a total of n courses you have to take, labeled from 0 to n-1.

Some courses may have prerequisites, for example to take course 0 you have to first take course 1,
which is expressed as a pair: [0,1]

Given the total number of courses and a list of prerequisite pairs, return the ordering of courses
you should take to finish all courses.

There may be multiple correct orders, you just need to return one of them. If it is impossible to finish
 all courses, return an empty sort.

Example 1:

Input: 2, [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you should have finished
             course 0. So the correct course order is [0,1] .

Ref: https://leetcode.com/problems/course-schedule-ii/

Time: O(V+E)
Space: O(V+E)
"""
import collections
import typing

class Solution:
    def findOrder(self, numCourses: int, prereq: typing.List[typing.List[int]]) -> List[int]:
        nodes = [x for x in range(numCourses)]
        edges = collections.defaultdict(list)
        indeg = {x: 0 for x in nodes}
        for course, dep in prereq:
            edges[course].append(dep)
            indeg[dep] += 1

        q = [x for x in indeg if indeg[x] == 0]
        res = []

        while q:
            curr = q.pop(0)
            res.append(curr)
            for neighbor in edges[curr]:
                indeg[neighbor] -= 1
                if indeg[neighbor] == 0:
                    q.append(neighbor)

        if len(res) == len(nodes):
            return reversed(res)
        else:
            return []
