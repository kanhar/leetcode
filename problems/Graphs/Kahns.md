{: .no_toc}
# Kahns Algorithm - Topological Sort
Practise here: [Leetcode](https://leetcode.com/list?selectedList=9l6pf80h)

- TOC
{:toc}

### [Course Dependency](https://leetcode.com/problems/course-schedule-ii)

>Given the total number of courses and a list of prerequisite pairs, return the ordering of courses
you should take to finish all courses.
> Time: O(V+E) <BR>
> Space: O(V+E) <BR>

> See also https://leetcode.com/problems/course-schedule/

<details><summary markdown="span">Execute!</summary>

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

### [Evaluate Lexicographical Order](https://leetcode.com/problems/alien-dictionary/)
> You are given a list of strings words from the alien language's dictionary, where the strings in words
are sorted lexicographically by the rules of this new language.
> Return a string of the unique letters in the new alien language sorted in lexicographically increasing
order by the new language's rules. If there is no solution, return "". If there are multiple solutions,
return any of them.

<details><summary markdown="span">Execute!</summary>

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
    def alienOrder(self, words: List[str]) -> str:
        edges = collections.defaultdict(set)
        indeg = {x: 0 for word in words for x in word}  # Or: { x:0 for x in ''.join(words)}

        for w1, w2 in zip(words, words[1:]):
            for a, b in zip(w1, w2):
                orderingFound = False
                if a != b:
                    if b not in edges[a]:
                        edges[a].add(b)
                        indeg[b] += 1
                    orderingFound = True
                    break
            
            # Cycle Detection - Invalid Dict Order, i.e. if w1 > w2 but still no valid ordering found. 
            if orderingFound is False and len(w1) > len(w2):
                return ""

        q = [x for x in indeg if indeg[x] == 0]
        res = []
        while q:
            curr = q.pop()
            res.append(curr)
            for d in edges[curr]:
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

### [Kanhar Sort - Sort Integers](https://leetcode.com/problems/maximum-gap/)

I like to jokingly call this Kanhar Sort, faster than Merge, Heap and Quick sort.

A modified version of Kahn's algorithm for sorting integer arrays, without duplicates.

See [Arrays->SortingAlgorithms.html#kanhar-sort-](https://kanhar.github.io/leetcode/problems/Arrays/SortingAlgorithms.html#kanhar-sort-)
