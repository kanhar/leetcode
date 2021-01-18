'''
Given a singly linked list, determine if it is a palindrome.

Example 1:

Input: 1->2
Output: false

Ref: https://leetcode.com/problems/palindrome-linked-list/
'''

# Key intuition here is that a regular recursion of a linked lists effectively iterates it in reverse.
class Solution:
    def isPalindrome(self, head: ListNode) -> bool:

        def solve(B):
            if B is None:
                return True
            else:
                if not solve(B.next) or self.A.val != B.val:
                    return False
                else:
                    self.A = self.A.next
                    return True

        self.A = head

        return solve(head)