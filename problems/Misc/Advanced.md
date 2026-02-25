{: .no_toc}
# Advanced

- TOC
{:toc}
  
### [Matrix Longest Increasing Path](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

> Given an integer matrix, find the length of the longest increasing path.

<details><summary markdown="span">Execute!</summary>

```python
import collections

class Solution:
    def longestIncreasingPath(self, m):
        edges = collections.defaultdict(list)
        indeg = collections.defaultdict(int)

        for i in range(len(m)):
            for j in range(len(m[0])):
                neighbors = [(i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)]
                for x, y in neighbors:
                    if x in range(len(m)) and y in range(len(m[i])) and m[x][y] > m[i][j]:
                        edges[(i, j)].append((x, y))
                        indeg[(x, y)] += 1

        # Step 2: Topological sorting with Kahn's algorithm. Notice that we move BFS Level by Level.
        q = [(i, j) for i in range(len(m)) for j in range(len(m[0])) if (i, j) not in indeg]
        max_path_len = 0
        res = []
        while q:
            max_path_len += 1
            q_tmp = []
            while q:
                node = q.pop(0)
                for neighbor in edges[node]:
                    indeg[neighbor] -= 1
                    if indeg[neighbor] == 0:
                        q_tmp.append(neighbor)

            q = q_tmp

        return max_path_len


class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        def solve(r, c, accum):
            if r not in range(len(matrix)) or c not in range(len(matrix[0])):
                return
            else:
                self.max = max(self.max, len(accum))
                if len(accum) != 0 and matrix[r][c] <= accum[-1]:
                    return

                tmp = matrix[r][c]
                matrix[r][c] = float('-inf')
                solve(r + 1, c, accum + [tmp])
                solve(r - 1, c, accum + [tmp])
                solve(r, c + 1, accum + [tmp])
                solve(r, c - 1, accum + [tmp])
                matrix[r][c] = tmp

        self.max = 1
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                solve(i, j, [])

        return self.max

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
