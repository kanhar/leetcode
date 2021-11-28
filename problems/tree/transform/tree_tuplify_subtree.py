"""
Given two non-empty binary trees s and t, check whether tree t has exactly the same structure and node values with a subtree of s.
A subtree of s is a tree consists of a node in s and all of this node's descendants. The tree s could also be considered as a subtree of itself.

Example 1:
Given tree s:

     3
    / \
   4   5
  / \
 1   2
Given tree t:
   4
  / \
 1   2
Return true, because t has the same structure and node values with a subtree of s.

Ref: https://leetcode.com/problems/subtree-of-another-tree/
"""
import collections

class Solution(object):
    def isSubtree(self, s, t):
        def check(a, b):
            if a == b == None:
                return True
            elif None in [a, b] or a.val != b.val:
                return False
            else:
                return check(a.left, b.left) and check(a.right, b.right)

        #s >> t
        def checkAll(s, t):
            if not s:
                return False
            elif check(s, t):
                return True
            else:
                return dfs(s.left, t) or dfs(s.right, t)

        return checkAll(s, t)


class Solution(object):
    def isSubtree(self, s, t):
        def tuplify(root):
            if root:
                return (root.val, tuplify(root.left), tuplify(root.right))

        def tuplifyAll(root):
            if root:
                tuple = root.val, tuplifyAll(root.left), tuplifyAll(root.right)
                self.res[tuple].append(root)
                return tuple

        self.res = collections.defaultdict(list)
        tuplifyAll(s)
        return tuplify(t) in self.res