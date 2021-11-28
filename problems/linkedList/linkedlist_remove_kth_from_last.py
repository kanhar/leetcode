"""
Given a linked list, remove the n-th node from the end of list and return its head.

Example:

Given linked list: 1->2->3->4->5, and n = 2.

After removing the second node from the end, the linked list becomes 1->2->3->5.

Ref: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
"""
class Solution:
    def removeNthFromEnd(self, head, n):
        cur = lag = head

        for i in range(0,n):
            cur = cur.next

        if not cur:
            return head.next

        while cur.next: #Tricky. You want to be one behind for deletion.
            cur = cur.next
            lag = lag.next

        lag.next = lag.next.next

        return head