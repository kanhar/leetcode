'''
Given a binary tree, you need to compute the length of the diameter of the tree.
The diameter of a binary tree is the length of the longest path between any two nodes in a tree.
This path may or may not pass through the root.

Example:
Given a binary tree
          1
         / \
        2   3
       / \
      4   5
Return 3, which is the length of the path [4,2,1,3] or [5,2,1,3].
https://leetcode.com/problems/diameter-of-binary-tree/
'''
class Solution:
    def diameterOfBinaryTree(self, root: TreeNode, max_d=0) -> int:
        def depth(root):
            return 0 if root is None else max(depth(root.left), depth(root.right))+1

        def diam_at(root):
            return 0 if root is None else depth(root.left) + depth(root.right)

        return 0 if root is None else max(max_d, diam_at(root), self.diameterOfBinaryTree(root.left), self.diameterOfBinaryTree(root.right))


class Solution:
    def diameterOfBinaryTree(self, root: TreeNode, max_d=0) -> int:
        def solve(root):
            if root is None:
                return 0
            else:
                left  = solve(root.left)
                right = solve(root.right)
                self.res = max(self.res, left + right)
                return max(left, right) + 1
        self.res = 0
        solve(root)
        return self.res


'''
Given a non-empty binary tree, find the maximum path sum.

For this problem, a path is defined as any sequence of nodes from some starting node to any node in the tree along the parent-child connections. The path must contain at least one node and does not need to go through the root.

Example 1:

Input: [1,2,3]

       1
      / \
     2   3

Output: 6
Ref: https://leetcode.com/problems/binary-tree-maximum-path-sum/
'''
class Solution(object):
    def maxPathSum(self, root):

        def get_sum(root):
            if root is None:
                return 0
            else:
                ls = get_sum(root.left)
                rs = get_sum(root.right)

                ls = max(ls,0)
                rs = max(rs,0)

                self.max = max(self.max, ls + rs + root.val)
                return max(ls, rs) + root.val

        self.max = float('-inf')
        get_sum(root)
        return self.max

'''
Given an undirected tree, return its diameter: the number of edges in a longest path in that tree.

The tree is given as an array of edges where edges[i] = [u, v] is a bidirectional edge between nodes u and v.  Each node has labels in the set {0, 1, ..., edges.length}.

Ref: https://leetcode.com/problems/tree-diameter/
'''

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
