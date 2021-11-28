
"""
Given a singly linked list L: L0→L1→…→Ln-1→Ln,
reorder it to: L0→Ln→L1→Ln-1→L2→Ln-2→…

You may not modify the values in the list's nodes, only nodes itself may be changed.

Given 1->2->3->4->5, reorder it to 1->5->2->4->3.

Solution:
1. Get Mid point
2. Reverse List from mid to end
3. Merge two (sorted arrays) of some sort (pun)
"""
class Solution:
    def reorderList(self, head: ListNode) -> None:
        if not head:
            return

            # find the middle of linked list [Problem 876]
        # in 1->2->3->4->5->6 find 4
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            # reverse the second part of the list [Problem 206]
        # convert 1->2->3->4->5->6 into 1->2->3->4 and 6->5->4
        # reverse the second half in-place
        prev = None
        curr = slow
        while curr:
            tmp = curr.next

            curr.next = prev
            prev = curr

            curr = tmp

            # merge two sorted linked lists [Problem 21]
        # merge 1->2->3->4 and 6->5->4 into 1->6->2->5->3->4
        first = head
        second = prev
        while second.next:
            tmp = first.next
            first.next = second
            first = tmp

            tmp = second.next
            second.next = first
            second = tmp
