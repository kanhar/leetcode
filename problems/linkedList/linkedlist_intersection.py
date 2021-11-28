"""
Write a program to find the node at which the intersection of two singly linked lists begins. Else return null
"""

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        h = collections.defaultdict(list)
        a = headA
        while a:
            h[a] = 1
            a = a.next

        b = headB
        while b:
            if b in h:
                return b
            b = b.next
        return None