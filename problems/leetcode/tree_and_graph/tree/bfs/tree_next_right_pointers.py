'''
You are given a perfect binary tree where all leaves are on the same level, and every parent has two children. The binary tree has the following definition:

struct Node {
  int val;
  Node *left;
  Node *right;
  Node *next;
}
Populate each next pointer to point to its next right node. If there is no next right node, the next pointer should be set to NULL.

Initially, all next pointers are set to NULL.
'''

class Solution:
    def connect(self, root: 'Node') -> 'Node':
        if not root:
            return None

        if root.right:
            root.left.next = root.right
            if root.next:
                root.right.next = root.next.left

        self.connect(root.left)
        self.connect(root.right)

        return root

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
    #q iterates level by level, q_tmp stores results of level. Interesting.
    #Compare with in order iterative.
    def connect(self, root):
        if root:
            root_c= root

            q     = [root]
            q_tmp = []
            while q:
                curr = q.pop(0)
                if q:
                    curr.next = q[0]

                if curr.left:
                    q_tmp.append(curr.left)
                if curr.right:
                    q_tmp.append(curr.right)

                if not q and q_tmp:
                    q, q_tmp = q_tmp, []

            return root_c
