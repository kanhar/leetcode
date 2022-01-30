{: .no_toc}
# Dijkstra, Bellman Ford, Floyd-Warshall - Shortest Path
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=90obk211)

- TOC
{:toc}

### [Network Delay Time](https://leetcode.com/problems/network-delay-time/)

>There are N network nodes, labelled 1 to N. Find shortest distance from node K to all nodes.

<details><summary markdown="span">Execute!</summary>

```python

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
            return -1   # could indicate a negative weight Cycle
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
                g[v] = min(g[v], g[u] + w)

        # Negative Weight Cycle Detection
        if g[v] < 0:
            return -1

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

        # Negative Weight Cycle Detection
        if g[u][u] < 0:
            return -1

        # Result
        if max(g[k].values()) == float('inf'):
            return -1
        else:
            return max(g[k].values())
```

</details>
<BR>

### [Tree Diameter](https://leetcode.com/problems/tree-diameter/)
> Given an undirected tree, return its bottomUp: the number of edges in a longest path in that tree.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def treeDiameter(self, times: List[List[int]]) -> int:
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        g = {x: {x: float('inf') for x in nodes} for x in nodes}
        for a, b in times:
            g[a][b] = g[b][a] = 1
            g[a][a] = g[b][b] = 1

        maxVal = -1
        for i in nodes:
            for a in nodes:
                for b in nodes:
                    g[a][b] = min(g[a][b], g[a][i] + g[i][b])
                    if g[a][b] != float('inf'):
                        maxVal = max(maxVal, g[a][b])

        return maxVal

import collections

class Solution:
    def treeDiameter(self, edges: List[List[int]]) -> int:
        graph = collections.defaultdict(set)
        for a, b in edges:
            graph[a].add(b)
            graph[b].add(a)

        startingNodes = [u for u, v in graph.items() if len(v) == 1]
        maxCount = -1
        for startNode in startingNodes:
            q = [ (startNode,0)]
            visited = set()
            while q:
                currNode, currCount = q.pop(0)
                maxCount = max(maxCount, currCount)
                visited.add(currNode)
                for neighbor in graph[currNode] - visited:
                    q.append((neighbor, currCount+1))

        return maxCount
```

</details>
<BR>

