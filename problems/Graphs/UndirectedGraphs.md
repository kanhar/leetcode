{: .no_toc}
# Undirected Graphs  

- TOC
{:toc}

### [Clone Graph](https://leetcode.com/problems/clone-graph/)

> Given a reference of a node in a connected undirected graph. Return a deep copy (clone) of the graph.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def cloneGraph(self, node: Optional['Node'], visited = {}) -> Optional['Node']:        
        # Works but infinite loop if graph has cycle
        if node:
            tmp = Node(node.val, [])
            tmp.neighbors = [ self.cloneGraph(x) for x in node.neighbors ]
            return tmp
        
class Solution:
    def cloneGraph(self, node: Optional['Node'], visited = {}) -> Optional['Node']:        
        # Does not prevent Cycle but works
        if node:
            if node in visited:
                return visited[node]
            else:
                visited[node] = Node(node.val, [])
                visited[node].neighbors = [ self.cloneGraph(x) for x in node.neighbors ]
                return visited[node]
```

</details>
<BR>

### [Redundant Connection](https://leetcode.com/problems/redundant-connection/)

> Convert Connected Graph to (Minimum) Undirected Graph with no cycles.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:        
        def isconnected(u, v, visited):
            if u == v:
                return True
            visited.add(u)
            for x in graph[u] - visited:                
                if isconnected(x, v, visited):
                    return True
            return False
                    
        graph = collections.defaultdict(set)
        for u, v in edges:
            if isconnected(u, v, visited= set()):
                return [u, v]
            graph[u].add(v)
            graph[v].add(u)

```
</details>
<BR>



