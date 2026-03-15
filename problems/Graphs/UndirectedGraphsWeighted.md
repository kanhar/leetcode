{: .no_toc}
# Undirected Graphs  (Weighted)

![Caption](https://assets.leetcode.com/uploads/2019/09/20/1558_ex1.png)

- TOC
{:toc}

### [Path with maximal probability](https://leetcode.com/problems/path-with-maximum-probability/description/)

> Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.

<details><summary markdown="span">Execute!</summary>

```python
import heapq
from collections import defaultdict

class Solution:
    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:
        # Step 1: Build the Adjacency List
        # Format: { node: [(neighbor, probability), ...] }
        graph = self.build_graph(edges, succProb)
        
        # Step 2: Solve using a Max-Heap Dijkstra
        return self.dijkstra(graph, n, start_node, end_node)

    def build_graph(self, edges, succProb):
        graph = defaultdict(list)
        for i, (u, v) in enumerate(edges):
            prob = succProb[i]
            # Graph is undirected, so add both directions
            graph[u].append((v, prob))
            graph[v].append((u, prob))
        return graph

    def dijkstra(self, graph, n, start, end):
        # max_prob[i] stores the highest probability found to reach node i
        # Initialize with 0.0, except start_node which is 1.0 (100% chance)
        max_prob = [0.0] * n
        max_prob[start] = 1.0
        
        # Priority Queue: (-probability, current_node)
        # Note: Python's heapq is a min-heap. To simulate a max-heap, 
        # we store the probability as a negative value.
        pq = [(-1.0, start)]
        
        while pq:
            curr_p, u = heapq.heappop(pq)
            curr_p = -curr_p # Convert back to positive
            
            # If we reached the end, return the probability
            if u == end:
                return curr_p
            
            # If we've already found a higher probability path to u, skip this
            if curr_p < max_prob[u]:
                continue
                
            for v, edge_prob in graph[u]:
                # The probability of reaching neighbor v is (prob to u) * (prob u->v)
                new_prob = curr_p * edge_prob
                
                # Relaxation: if this new path is better, update and push to heap
                if new_prob > max_prob[v]:
                    max_prob[v] = new_prob
                    heapq.heappush(pq, (-new_prob, v))
                    
        return 0.0
```

</details>
<BR>

