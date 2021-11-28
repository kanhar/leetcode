"""
A linked list is given such that each node contains an additional random pointer which could point to any node in the list or null.

Return a deep copy of the list.

The Linked List is represented in the input/output as a list of n nodes. Each node is represented as a pair of [val, random_index] where:

val: an integer representing Node.val
random_index: the index of the node (range from 0 to n-1) where random pointer points to, or null if it does not point to any node.
Ref: https://leetcode.com/problems/copy-list-with-random-pointer/
"""

class Solution:
    def copyRandomList(self, head):
        if head is not None:
            d = collections.defaultdict(lambda: Node(0,None,None))
            d[None] = None  #to avoid if else conditions beloe
            curr = head
            while curr:
                d[curr].val = curr.val
                d[curr].next = d[curr.next]     if curr.next else None
                d[curr].random = d[curr.random] if curr.random else None
                curr = curr.next
            return d[head]