{: .no_toc}
# Graph  
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90ojkbn2)

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


### [Is Graph Connected?](https://leetcode.com/problems/all-paths-from-source-lead-to-destination/)

> Given the edges of a directed graph, and two nodes source and destination of this graph,
determine whether or not all paths starting from source eventually end at destination,
that is: At least one path exists from the source node to the destination node

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    #What is different here is that the graph may have cycles
    def leadsToDestination(self, n: int, edges: List[List[int]], source: int, dest: int) -> bool:
        def dfs(source, dest, seen = set()):
            if source == dest and len(graph[source])==0: #To prevent cycles.
                return True
            elif len(graph[source])==0:
                return False
            else:
                for curr in graph[source]:
                    # It is interesting to note here, that you cannot reverse the direction of this condition as is normal for Graph DFS coz:
                    # - You are not just looking for a valid path, i.e. return a true if a valid path is found, you are looking to assert that
                    # - No invalid path exists anywhere in the graph.
                    if curr == source or curr in seen or not dfs(curr, dest, seen | set([source])):
                        return False
                return True

        graph = collections.defaultdict(set)
        for a, b in edges:
            graph[a].add(b)

        return dfs(source, dest)
```

</details>
<BR>


</details>
<BR>

