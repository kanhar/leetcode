"""
Given a reference of a node in a connected undirected graph.

Return a deep copy (clone) of the graph.

Each node in the graph contains a val (int) and a list (List[Node]) of its neighbors.

class Node {
    public int val;
    public List<Node> neighbors;
}

Ref: https://leetcode.com/problems/clone-graph/
"""
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

