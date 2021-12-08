"""
Given a binary tree

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.

Ref: https://leetcode.com/problems/populating-next-right-pointers-in-each-node-ii/
"""

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        q = [root]
        qChildren = []

        while q:
            curr = q.pop(0)
            if not curr:
                continue

            if q:
                curr.next = q[0]

            if curr.left:
                qChildren.append(curr.left)
            if curr.right:
                qChildren.append(curr.right)

            if not q and qChildren:
                q, qChildren = qChildren, q

        return root