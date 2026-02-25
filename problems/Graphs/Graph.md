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
