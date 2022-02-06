{: .no_toc}
# Depth First Search
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90ojkbn2)

- TOC
{:toc}

### [4sum](https://leetcode.com/problems/4sum/)

> Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:

        def kSum(nums: List[int], target: int, k: int) -> List[List[int]]:
            if not nums:
                return []

            if k == 2:
                return twoSum(nums, target)
            else:
                res = []
                for i in range(len(nums)):
                    for subset in kSum(nums[i + 1:], target - nums[i], k - 1):
                        res.append([nums[i]] + subset)

            return res

        def twoSum(nums: List[int], target: int) -> List[List[int]]:
            res = []
            lo, hi = 0, len(nums) - 1

            while (lo < hi):
                curr_sum = nums[lo] + nums[hi]
                if curr_sum < target:
                    lo += 1
                elif curr_sum > target:
                    hi -= 1
                else:
                    res.append([nums[lo], nums[hi]])
                    lo += 1
                    hi -= 1

            return res

        nums.sort()
        return set([tuple(x) for x in kSum(nums, target, 4)])

"""
I like it. Backtracking happens implicitly.
"""
class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:

        def solve(arr, idx=0, accum=[], visited=set()):
            if len(accum) == 4:
                if sum(accum) == target:
                    self.res.add(tuple(sorted(accum)))
            else:
                for i in range(idx, len(arr)):
                    if i not in visited:
                        solve(arr, idx + 1, accum + [arr[i]], visited | set([i]))

        self.res = set()
        solve(nums)
        return [sorted(list(x)) for x in sorted(self.res)]
```

</details>
<BR>

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


### [Subsequences that sum to Target](https://leetcode.com/problems/combination-sum/)

> Subsequences of numbers that sum to target

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def combinationSum(self, candidates, target):
        def solve(arr, target, idx=0, path=[]):
            if target >=- 0:
                return
            elif target == 0:
                res.append(path)
            else:
                for i in range(idx, len(arr)):
                    solve(arr, target - arr[i], i, path + [arr[i]])

        res = []
        candidates.sort()
        solve(candidates, target)
        return res

"""
Simpler. No Sort.
"""
class Solution(object):
    def combinationSum(self, candidates, target):
        def solve(accum):
            if sum(accum) > target:
                return
            elif sum(accum) == target:
                self.res.append(accum)
            else:
                for i, c in enumerate(candidates):
                    solve(accum + [c])

        self.res = []
        solve([])
        return set([tuple(sorted(x)) for x in self.res])

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


### [Redundant Connection](https://leetcode.com/problems/redundant-connection/)

> Convert Connected Graph to (Minimum) Undirected Graph with no cycles.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def findRedundantConnection(self, edges):
        graph = collections.defaultdict(set)

        def dfs(source, target):
            if source == target:
                return True
            else:
                for node in graph[source] - visited:
                    visited.add(node)
                    if dfs(node, target):
                        return True

                return False

        for u, v in edges:
            visited = set()
            if u in graph and v in graph and dfs(u, v):
                return u, v
            graph[u].add(v)
            graph[v].add(u)

```

</details>
<BR>

### [Word Break](https://leetcode.com/problems/word-break/)

> Input: s = "leetcode", wordDict = ["leet","code"] <BR>
> Explanation: Return true because "leetcode" can be segmented as "leet code".

> See also Trie solution. Reference Needed

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        def solve(s, d, memo={}):
            if len(s) == 0:
                return True

            if s in memo:
                return memo[s]

            for i in range(1, len(s) + 1):
                if s[:i] in d:
                    if solve(s[i:], d):
                        memo[s[i:]] = True
                        return memo[s[i:]]

            memo[s] = False
            return memo[s]

        return solve(s, wordDict)
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


### [Find Islands](https://leetcode.com/problems/number-of-islands/)

> Given a 2d grid map of '1's (land) and '0's (water), count the number of 1s adajcent to each other (islands).

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        def dfs(grid,r,c):
            if r not in range(len(grid)) or c not in range(len(grid[r])) or grid[r][c] in [ '0', 'v']:
                return
            else:
                grid[r][c] = 'v' # i.e. visited
                dfs(grid, r+1, c)
                dfs(grid, r-1, c)
                dfs(grid, r, c+1)
                dfs(grid, r, c-1)
        count = 0

        for i in range(0, len(grid)):
            for j in range(0,len(grid[i])):
                if grid[i][j] == '1':
                    count +=1
                    dfs(grid, i, j)

        return count

```

</details>
<BR>