{: .no_toc}
# Undirected Graphs  (Weighted)

![Caption](https://assets.leetcode.com/uploads/2019/09/20/1558_ex1.png)

- TOC
{:toc}

### [Path with maximal probability](https://leetcode.com/problems/path-with-maximum-probability/description/)

> Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:
        graph = defaultdict(set) 
        for (u, v), p in zip(edges, succProb):
            graph[u].add((p, v)); graph[v].add((p, u))

        visited = {} 
        heap = [(-1.0, start_node)]
        
        while heap:
            p, curr = heapq.heappop(heap)
            p = -p

            if curr == end_node:
                return p

            visited[curr] = p

            for weight, neighbor in graph[curr]:
                if neighbor not in visited:
                    heapq.heappush(heap, (-(p * weight), neighbor))

        return 0.0
```

</details>
<BR>

