{: .no_toc}
# Undirected Graphs  

![Caption](https://assets.leetcode.com/uploads/2021/05/02/reduntant1-2-graph.jpg)

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

![Caption](https://assets.leetcode.com/uploads/2021/05/02/reduntant1-1-graph.jpg) 

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:        
        def canMeet(curr,target, visited):
            if curr==target:
                return True
            visited.add(curr)
            for neighbor in graph[curr] :
                if neighbor not in visited:
                    if canMeet(neighbor, target, visited):
                        return True

            return False

        graph = collections.defaultdict(set)
        for u,v in edges:
            if canMeet(u,v, set()):
                return [u,v]
            graph[u].add(v)
            graph[v].add(u)
```

Union find only works with undirected graphs. It asks the question if your highest order boss, is shared with another node, you must be in the same org. 


```
class Solution:
    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        # Initialize each node as its own parent (its own set)
        parent = list(range(len(edges) + 1))

        def find(i):
            if parent[i] == i:
                return i
            # Path compression: makes future lookups nearly O(1)
            parent[i] = find(parent[i])
            return parent[i]

        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False # They are already in the same set!

        for u, v in edges:
            if not union(u, v):
                return [u, v]

```
</details>
<BR>



