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

Floyd-Warshall
Time: O(n^3)
Space: O(n^2)

Ref: https://leetcode.com/problems/network-delay-time/
# Bellman Ford: Single Source Shortest Path ( can handle negative weight cycles )
"""


class Solution:

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        if len(nodes) != n:
            return -1

        # Bellman Ford
        distance = {x: float('inf') for x in nodes}
        distance[k] = 0
        for _ in range(0, n - 1):
            for source, dest, weight in times:
                distance[dest] = min(distance[dest], distance[source] + weight)

        for source, dest, weight in times:
            if distance[dest] > distance[source] + weight:
                return -1

        if max(distance.values()) == float('inf'):
            return -1
        else:
            return max(distance.values())
