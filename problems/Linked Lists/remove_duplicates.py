"""
Given a sorted linked list, delete all duplicates such that each element appear only once.

Example 1:

Input: 1->1->2
Output: 1->2

Ref: https://leetcode.com/problems/remove-duplicates-from-sorted-list/
"""

class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:

        curr = head
        while curr:
            while curr and curr.next and curr.val == curr.next.val:
                curr.next = curr.next.next

            curr = curr.next

        return head