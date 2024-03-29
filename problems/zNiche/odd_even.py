"""
Given a singly linked list, group all odd nodes together followed by the even nodes.
Please note here we are talking about the node number and not the value in the nodes.

You should try to do it in place. The program should run in O(1) space complexity and O(nodes) time complexity.

Example 1:

Input: 1->2->3->4->5->NULL
Output: 1->3->5->2->4->NULL

Ref: https://leetcode.com/problems/odd-even-linked-list/
"""

class Solution:
    def oddEvenList(self, head):
        if head:
            odd = head
            even = head.next
            evenHead = even

            while even and even.next:
                odd.next = odd.next.next
                even.next = even.next.next
                odd = odd.next
                even = even.next

            odd.next = evenHead
            return head