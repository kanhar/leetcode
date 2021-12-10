"""
There are N network nodes, labelled 1 to N. Find shortest distance from node K to all nodes.

Ref: https://leetcode.com/problems/network-delay-time/
"""

import collections
import heapq

"""
Blind DFS: O(N^N +ElogE)
"""
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Setup
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        if len(nodes) < n:
            return -1

        edges = collections.defaultdict(list)
        for u, v, w in times:
            edges[u].append((w, v))

        # Core Algorithm
        g = {x: float('inf') for x in nodes}
        def solve(curr, currDist):
            if currDist < g[curr]:
                g[curr] = currDist
                for weight, neighbor in sorted(edges[curr]):
                    solve(neighbor, currDist + weight)

        solve(k, 0)

        # Result
        if max(g.values()) < float('inf'):
            return max(g.values())
        else:
            return -1

"""
Dijkstra's: O(N^2 +E)
Time: O(ElogV)
Space: O(V+E)
"""
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        if len(nodes) < n:
            return -1

        edges = collections.defaultdict(list)
        for u, v, w in times:
            edges[u].append((w, v))

        # Core Algorithm starts
        g = collections.defaultdict(int)
        heap = [(0, k)]

        while heap:
            dist, curr = heapq.heappop(heap)
            g[curr] = dist

            if len(g) == n:
                break

            for weight, neighbor in edges[curr]:
                if neighbor not in g:
                    heapq.heappush(heap, (dist + weight, neighbor))
                    # Core Algorithm Ends

        if len(g) != n:
            return -1
        else:
            return max(g.values())

"""
Bellman Ford Algorithm
"""
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Setup
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        if len(nodes) < n:
            return -1

        # Core Algorithm
        g = {x: float('inf') for x in nodes}
        g[k] = 0
        for _ in range(n):
            for u, v, w in times:
                g[v] = min(g[v], g[u]+w )

        # Result
        if max(g.values()) < float('inf'):
            return max(g.values())
        else:
            return -1

"""
Floyd Warshall. Can also be used to get graph-diameter
"""
class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        # Setup
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        if len(nodes) < n:
            return -1

        # Core Algorithm starts
        g = {x: {x: float('inf') for x in nodes} for x in nodes}
        for u,v,w in times:
            g[u][u]=g[v][v]=0
            g[u][v]=w
            
        for i in nodes:
            for u in nodes:
                for v in nodes:
                    g[u][v] = min(g[u][v], g[u][i] + g[i][v])
        # Core Algorithm ends

        # Result
        if max(g[k].values()) == float('inf'):
            return -1
        else:
            return max(g[k].values())

