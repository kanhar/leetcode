{: .no_toc}
# Undirected Graphs  (Weighted)

![Caption](https://assets.leetcode.com/uploads/2019/09/20/1558_ex1.png)

- TOC
{:toc}

Weighted edges have a cost. Two classics use a min-heap to always pick the cheapest next step: **Dijkstra** (cheapest path from a start) and **Prim** (cheapest way to connect everything).

**Key intuition 1:** Both are greedy: keep a heap of candidate edges and always take the cheapest one that reaches a new node.

**Key intuition 2:** The only difference is what goes in the heap. Dijkstra pushes the **total cost from the start** (`cost + weight`). Prim pushes just the **cost of the one bridge** (`weight`).

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 36, "rankSpacing": 44, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "20px"}}}%%
flowchart TB
    subgraph G ["The graph"]
        direction LR
        gA(("A"))
        gB(("B"))
        gC(("C"))
        gD(("D"))
        gA ---|"2"| gB
        gB ---|"2"| gC
        gA ---|"3"| gC
        gC ---|"1"| gD
    end
    subgraph J ["Dijkstra from A: pushes the total cost from the start"]
        direction TB
        jA["A<br/>0"]
        jB["B<br/>2"]
        jA --- jB
        jC["C<br/>3"]
        jD["D<br/>4"]
        jC --- jD
        jg1(("."))
        jC --- jg1
        jA --- jC
    end
    subgraph P ["Prim from A: pushes only the cost of the one bridge"]
        direction TB
        pA(("A"))
        pB["B<br/>bridge 2"]
        pg2(("."))
        pB --- pg2
        pC["C<br/>bridge 2"]
        pD["D<br/>bridge 1"]
        pC --- pD
        pg3(("."))
        pC --- pg3
        pB --- pC
        pA --- pB
        pg4(("."))
        pA --- pg4
    end
        G ==> J
        G ==> P
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class gA,gB,gC,gD,jB,jC,jD,pB,pC,pD n
    class jA,pA hi
    class jg1,pg2,pg3,pg4 ghost
    style G fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style J fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    style P fill:#f1f8e9,stroke:#689f38,color:#33691e
    linkStyle 6 stroke:none
    linkStyle 8 stroke:none
    linkStyle 10 stroke:none
    linkStyle 13 stroke:none
```

On the same graph the two build different trees. Dijkstra reaches C directly for 3, because going through B would cost 2 + 2 = 4, so it keeps A-C. Prim only compares bridges into the tree: once B is in, B-C costs 2, which beats A-C at 3, so it takes B-C. Prim's tree weighs 2 + 2 + 1 = 5, Dijkstra's weighs 2 + 3 + 1 = 6, and that difference is the whole distinction between them.

### [Path with maximal probability](https://leetcode.com/problems/path-with-maximum-probability/description/)

> Given two nodes start and end, find the path with the maximum probability of success to go from start to end and return its success probability.

**Key intuition 1:** It is Dijkstra with multiplication instead of addition: the best path to a node is found first. Python's heap is a min-heap, so push the NEGATIVE probability.

**Key intuition 2:** Probabilities are at most 1, so adding another edge can never make the path better. That is what makes the greedy choice safe, just as non-negative costs make it safe for ordinary Dijkstra.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def maxProbability(self, n: int, edges: list[list[int]], succProb: list[float], start_node: int, end_node: int) -> float:
        graph = defaultdict(set)
        for (u, v), p in zip(edges, succProb):
            graph[u].add((p, v));
            graph[v].add((p, u))

        visited = collections.defaultdict(int)
        heap = [(-1.0, start_node)]

        while heap:
            cost, curr = heapq.heappop(heap)
            cost = -cost

            visited[curr] = cost
            if curr == end_node:
                break

            for weight, neighbor in graph[curr]:
                if neighbor not in visited:
                    heapq.heappush(heap, (-(cost * weight), neighbor))

        return visited.get(end_node, 0.0)
```

</details>
<BR>

### [Connecting Cities at Minimum cost](https://leetcode.com/problems/connecting-cities-with-minimum-cost/)
Return the minimum cost to connect all n nodes such that there is at least one path between each pair of cities. 

**Key intuition 1:** You want the cheapest set of roads that connects every city: a minimum spanning tree. Start anywhere and repeatedly add the cheapest edge that reaches a city not yet connected (Prim).

**Key intuition 2:** If you finish with fewer than n cities connected, the graph is split in pieces: return -1.

<details><summary markdown="span">Using Prim's algorithm</summary>

The fundamental difference between Dijkstra’s Algorithm (for shortest paths) and Prim’s Algorithm (for Minimum Spanning Trees) is how they prioritize the "next" node to visit. In Dijkstra's, you care about the total distance from the start. In Prim's, you only care about the cost of the immediate bridge to an unvisited node.

Using the original example:
![Dijkstra example graph](../../images/djikstra.jpeg)

Prims would render:
![Prim](../../images/prims.jpg)

```python
class Solution:
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        graph = collections.defaultdict(list)
        for u, v, w in connections:
            graph[u].append((w, v))
            graph[v].append((w, u))

        # We store the edge weight used to reach each node
        visited = {}
        k = 1
        heap = [(0, k)]

        while heap:
            cost, curr = heapq.heappop(heap)
            if curr in visited:
                continue
            visited[curr] = cost

            if len(visited) == n:
                break

            for weight, neighbor in graph[curr]:
                if neighbor not in visited:
                    # Key divergence from djikstra which would be `cost + weight`
                    heapq.heappush(heap, (weight, neighbor))

        return sum(visited.values()) if len(visited) == n else -1
```
</details>
<BR>
