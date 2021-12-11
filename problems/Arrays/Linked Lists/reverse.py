"""
Reverse a singly linked list.

Example:

Input: 1->2->3->4->5->NULL
Output: 5->4->3->2->1->NULL

Ref: https://leetcode.com/problems/reverse-linked-list
Ref: https://medium.com/outco/reversing-a-linked-list-easy-as-1-2-3-560fbffe2088
"""
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        current = head
        leading = head
        previous = None

        while current:
            leading = leading.next

            current.next = previous     # Current points backward
            previous = current          # Backwards becomes forward.

            current = leading           # New Current becomes original forward

        return previous