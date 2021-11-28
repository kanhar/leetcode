"""
There are N network nodes, labelled 1 to N.

Given times, a list of travel times as directed edges times[i] = (u, v, w), where u is the source node,
v is the target node, and w is the time it takes for a signal to travel from source to target.

Now, we send a signal from a certain node K. How long will it take for all nodes to receive the signal?
If it is impossible, return -1.

Input: times = [[2,1,1],[2,3,1],[3,4,1]], N = 4, K = 2
Output: 2

(1)   ----   1 ------ (2 )
                        .
                        .
                        1
                        .
                        .
(4)   ----   1 -----  (3)

Djikstra
Time: O(ElogV)
Space: O(V+E)

Bellman Ford
Time: O(VE)
Space: O(V)

Ref: https://leetcode.com/problems/network-delay-time/
"""
import heapq
import typing

class Solution:
    def networkDelayTime(self, times: typing.List[typing.List[int]], n: int, k: int) -> int:
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        if len(nodes) < n:  # Good check to ensure Graph is connected, i.e. no missing nodes.
            return -1

        # Dijkstra - Build Adjacent Graph
        edges = {x: [] for x in nodes}
        for a, b, w in times:
            edges[a].append((w, b))

        distance = {}
        H = [(0, k)]
        while H:
            currDist, currNode = heapq.heappop(H)
            distance[currNode] = currDist

            if len(distance) == n:
                break

            for neighborDist, neighborNode in edges[currNode]:
                if neighborNode not in distance:
                    heapq.heappush(H, (currDist + neighborDist, neighborNode))

        if len(distance) != n:
            return -1
        else:
            return max(distance.values())






