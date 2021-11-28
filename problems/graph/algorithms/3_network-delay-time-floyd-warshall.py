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
# Floyd-Warshall:  Finds the shortest path between all pairs of nodes
"""

class Solution(object):

    def networkDelayTime(self, times, N, K):
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        if len(nodes) < N:  # Good check to ensure Graph is connected, i.e. no missing nodes.
            return -1

        matrix = {x: {x: float('inf') for x in nodes} for x in nodes}
        for a, b, w in times:
            matrix[a][b] = w

        for n in nodes:  # Set distance of all nodes to zero
            matrix[n][n] = 0

        for k in nodes:
            for a in nodes:
                for b in nodes:
                    matrix[a][b] = min(matrix[a][b], matrix[a][k] + matrix[k][b])

        if max(matrix[K].values()) == float('inf'):
            return -1
        else:
            return max(matrix[K].values())


"""
Given an undirected tree, return its bottomUp: the number of edges in a longest path in that tree.

The tree is given as an sort of edges where edges[i] = [u, v] is a bidirectional edge between nodes u and v.  Each node has labels in the set {0, 1, ..., edges.length}.

Ref: https://leetcode.com/problems/tree-diameter/

"""


class Solution:
    def treeDiameter(self, times: List[List[int]]) -> int:
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        matrix = {x: {x: float(inf) for x in nodes} for x in nodes}
        for a, b in times:
            matrix[a][b] = 1
            matrix[b][a] = 1

        for n in nodes:  # Set distance of all K's to zero
            matrix[n][n] = 0

        for k in nodes:
            for a in nodes:
                for b in nodes:
                    matrix[a][b] = min(matrix[a][k] + matrix[k][b], matrix[a][b])

        return max([max(m) for m in matrix.values()])
