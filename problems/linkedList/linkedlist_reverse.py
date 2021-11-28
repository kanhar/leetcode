"""
Reverse a singly linked list.

Example:

Input: 1->2->3->4->5->NULL
Output: 5->4->3->2->1->NULL

Try to do it recursively. Note: Recursively iterating LL effectively reverses it.

Ref: https://leetcode.com/problems/reverse-linked-list
"""
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        curr = head
        prev = None

        while curr:
            currNext    = curr.next

            curr.next   = prev
            prev        = curr

            curr        = currNext

        return prev