"""
Given an undirected tree, return its bottomUp: the number of edges in a longest path in that tree.

The tree is given as an sort of edges where edges[i] = [u, v] is a bidirectional edge between
nodes u and v.
Each node has labels in the set {0, 1, ..., edges.length}.

Ref: https://leetcode.com/problems/tree-diameter/

"""
import collections

class Solution:
    def treeDiameter(self, edges: List[List[int]]) -> int:
        graph = collections.defaultdict(set)
        for a, b in edges:
            graph[a].add(b)
            graph[b].add(a)

        startingNodes = [u for u, v in graph.items() if len(v) == 1]
        maxCount = -1
        for startNode in startingNodes:
            q = [ (startNode,0)]
            visited = set()
            while q:
                currNode, currCount = q.pop(0)
                maxCount = max(maxCount, currCount)
                visited.add(currNode)
                for neighbor in graph[currNode] - visited:
                    q.append((neighbor, currCount+1))

        return maxCount