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
    def cloneGraph(self, node: 'Node', cloned = {}) -> 'Node':
        if node is None:
            return None
        elif node in cloned:
            return cloned[node]
        else:
            cloned[node] = Node(node.val,[])
            cloned[node].neighbors = [self.cloneGraph(x, cloned) for x in node.neighbors]
            return cloned[node]
```

</details>
<BR>

### [Redundant Connection](https://leetcode.com/problems/redundant-connection/)

> Convert Connected Graph to (Minimum) Undirected Graph with no cycles.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def findRedundantConnection(self, edges):
        graph = collections.defaultdict(list)

        def is_connected(start, target, visited):
            if start == target:
                return True
            
            visited.add(start)
            
            for neighbor in graph[start]:
                if neighbor not in visited:
                    if is_connected(neighbor, target, visited):
                        return True
            return False

        for u, v in edges:
            # Check if u and v are already reachable through the existing graph
            if is_connected(u, v, set()):
                return [u, v]
            
            # If not connected, add the edge to the graph
            graph[u].append(v)
            graph[v].append(u)

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

### [Equation Satisfiabiliy](https://leetcode.com/problems/satisfiability-of-equality-equations/)


> Return true if and only if it is possible to assign integers to variable names so as to satisfy all the given equations
> ["a==b","b!=a"], Output: False

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        def canMeet(a, b, visited = set()):
            if a == b:
                return True
            else:
                for node in graph[a] - visited:
                    if canMeet(node, b, visited | set([a]) ):
                        return True
                return False

        graph = collections.defaultdict(set)
        notEquals = []

        for eq in equations:
            if eq[1:3] == '!=':
                a, b = eq.split('!=')
                notEquals.append((a, b))
            else:
                a, b = eq.split('==')
                graph[a].add(b)
                graph[b].add(a)

        for a, b in notEquals:
            if canMeet(a, b):
                return False
        return True
```

</details>
<BR>

### [Evaluate Equation Division](https://leetcode.com/problems/evaluate-division)

> Summary: If a/b = 2 and b/c = 3, what is a/c? 

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def calcEquation(self, equations, values, queries):
        def dfs(a, b, visited, currVal):
            if a not in graph or b not in graph or a in visited:
                return -1.0
            if a == b:
                return currVal

            visited.add(a)
            for i,j in graph[a]-visited:
                tmp = dfs(i, b, visited, j * currVal)
                if tmp != -1.0:
                    return tmp
            
            return -1.0

        graph = collections.defaultdict(set)

        for (a, b), val in zip(equations, values):
            graph[a].add((b, 1 * val))
            graph[b].add((a, 1 / val))

        return [dfs(a, b, set(), 1.0) for a, b in queries]
```

</details>
<BR>
