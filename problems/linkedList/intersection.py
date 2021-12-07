"""
Write a program to find the node at which the intersection of two singly linked lists begins. Else return null

Ref: https://leetcode.com/problems/intersection-of-two-linked-lists/
"""

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        d = {}
        while headA:
            d[headA] = 1
            headA = headA.next

        while headB:
            if headB in d:
                return headB
            headB = headB.next

        return None