'''
Given the edges of a directed graph, and two nodes source and destination of this graph, determine whether or not all paths starting from source eventually end at destination, that is:

At least one path exists from the source node to the destination node
If a path exists from the source node to a node with no outgoing edges, then that node is equal to destination.
The number of possible paths from source to destination is a finite number.
Return true if and only if all roads from source lead to destination.

Ref: https://leetcode.com/problems/all-paths-from-source-lead-to-destination/

    0
   /    \
  \/      /\
  1          2
Source - Destination: 0--> 2
Not all paths go from 0 to 2. And must assert no cycles ( Ex: Path from 2 back to 2 or 0 )
'''

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
                    #It is interesting to note here, that you cannot reverse the direction of this condition as is normal for Graph DFS coz:
                    # - You are not just looking for a valid path, i.e. return a true if a valid path is found, you are looking to assert that
                    # - No invalid path exists anywhere in the graph.
                    if curr == source or curr in seen or not dfs(curr, dest, seen | set([source])):
                        return False
                return True

        graph = collections.defaultdict(set)
        for a, b in edges:
            graph[a].add(b)

        return dfs(source, dest)