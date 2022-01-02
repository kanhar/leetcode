{: .no_toc}
# Kahns Algorithm - Topological Sort
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9lu7fe4c)

- TOC
{:toc}

### Course Dependency

>Given the total number of courses and a list of prerequisite pairs, return the ordering of courses
you should take to finish all courses.
> [Leetcode](https://leetcode.com/problems/course-schedule-ii) <BR>
> Time: O(V+E) <BR>
> Space: O(V+E) <BR>

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def findOrder(self, numCourses: int, prereq: typing.List[typing.List[int]]) -> List[int]:
        nodes = [x for x in range(numCourses)]
        edges = collections.defaultdict(list)
        indeg = {x: 0 for x in nodes}
        for course, dep in prereq:
            edges[course].append(dep)
            indeg[dep] += 1

        q = [x for x in indeg if indeg[x] == 0]
        res = []

        while q:
            curr = q.pop(0)
            res.append(curr)
            for neighbor in edges[curr]:
                indeg[neighbor] -= 1
                if indeg[neighbor] == 0:
                    q.append(neighbor)

        if len(res) == len(nodes):
            return reversed(res)
        else:
            return []
```

</details>
<BR>

### Dictionary Alien
> You are given a list of strings words from the alien language's dictionary, where the strings in words
are sorted lexicographically by the rules of this new language.
> Return a string of the unique letters in the new alien language sorted in lexicographically increasing
order by the new language's rules. If there is no solution, return "". If there are multiple solutions,
return any of them.
> [Leetcode](https://leetcode.com/problems/alien-dictionary/)

<details><summary markdown="span">Let's see some code!</summary>

```text
    Loop like so:
    zip:
    -> "wrt",  "wrf",  "er",   "ett",  "rftt"
    -> "wrf",  "er",   "ett",  "rftt"
    results in:
    --> wrt wrf
    --> wrf er
    --> er ett
    --> ett rftt

    Then zip (wrf er):
        w --> e (w comes before e)
        <Hard Break after first find, since no further inference can be made>
```

```python
class Solution:
    def alienOrder(self, words: typing.List[str]) -> str:
        adj = collections.defaultdict(set)
        indeg = {x: 0 for word in words for x in word}  # Or: { x:0 for x in ''.join(words)}

        for w1, w2 in zip(words, words[1:]):
            for a, b in zip(w1, w2):
                orderingFound = False
                if a != b:
                    if b not in adj[a]:
                        adj[a].add(b)
                        indeg[b] += 1
                    orderingFound = True
                    break

            if orderingFound is False and len(w1) > len(w2):  # Invalid Dict order.
                return ""

        q = [x for x in indeg if indeg[x] == 0]
        res = []
        while q:
            curr = q.pop()
            res.append(curr)
            for d in adj[curr]:
                indeg[d] -= 1
                if indeg[d] == 0:
                    q.append(d)

        if len(res) < len(indeg):
            return ""  # indicates cycle
        else:
            return ''.join(res)
```

</details>
<BR>


### Matrix Longest Increasing Path

> Given an integer matrix, find the length of the longest increasing path.
> [Leetcode](https://leetcode.com/problems/longest-increasing-path-in-a-matrix/)

<details><summary markdown="span">Let's see some code!</summary>

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

