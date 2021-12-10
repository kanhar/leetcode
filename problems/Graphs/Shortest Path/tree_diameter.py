"""
Given an undirected tree, return its bottomUp: the number of edges in a longest path in that tree.

The tree is given as an sort of edges where edges[i] = [u, v] is a bidirectional edge between
nodes u and v.
Each node has labels in the set {0, 1, ..., edges.length}.

Ref: https://leetcode.com/problems/tree-diameter/

"""
class Solution:
    def treeDiameter(self, times: List[List[int]]) -> int:
        nodes = set([x[0] for x in times] + [x[1] for x in times])
        g = {x: {x: float('inf') for x in nodes} for x in nodes}
        for a, b in times:
            g[a][b] = g[b][a] = 1
            g[a][a] = g[b][b] = 1

        maxVal = -1
        for i in nodes:
            for a in nodes:
                for b in nodes:
                    g[a][b] = min(g[a][b], g[a][i] + g[i][b])
                    if g[a][b] != float('inf'):
                        maxVal = max(maxVal, g[a][b])

        return maxVal