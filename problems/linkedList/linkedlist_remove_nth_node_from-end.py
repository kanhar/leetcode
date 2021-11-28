"""
Given a linked list, remove the n-th node from the end of list and return its head.

Example:

Given linked list: 1->2->3->4->5, and n = 2.

After removing the second node from the end, the linked list becomes 1->2->3->5.
"""

class Solution:
    def removeNthFromEnd(self, head, n):
        slow = curr = head
        for i in range(n):
            curr = curr.next
        if not curr:            # Ex: [1,2], n=2.
            return slow.next

        while curr.next:        # Ideal for deletion, cause Slow points to Object to be deleted.
            curr = curr.next
            slow = slow.next

        slow.next = slow.next.next

        return head
