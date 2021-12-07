"""
A linked list is given such that each node contains an additional random pointer which could point to
any node in the list or null.

Return a deep copy of the list.

The Linked List is represented in the input/output as a list of n nodes. Each node is represented
as a pair of [val, random_index] where:

val: an integer representing Node.val
random_index: the index of the node (range from 0 to n-1) where random pointer points to, or null if it does not point to any node.
Ref: https://leetcode.com/problems/copy-list-with-random-pointer/
"""
import collections

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        d = collections.defaultdict(lambda: Node(0, None, None))

        newHead = None
        while head:
            d[head].val = head.val
            d[head].next = d[head.next] if head.next else None
            d[head].random = d[head.random] if head.random else None

            if newHead == None:
                newHead = d[head]

            head = head.next

        return newHead
