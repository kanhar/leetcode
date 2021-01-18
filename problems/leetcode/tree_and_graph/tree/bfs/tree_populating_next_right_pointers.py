'''
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
'''

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        q = [root]
        qtmp = []
        while q:
            curr = q.pop(0)
            if curr is None:
                continue
            if q:                curr.next = q[0]
            if curr.left:        qtmp.append(curr.left)
            if curr.right:       qtmp.append(curr.right)

            if not q and qtmp:
                q = qtmp
                qtmp = []

        return root
