'''
Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.

Example:

Input:
[
  1->4->5,
  1->3->4,
  2->6
]
Output: 1->1->2->3->4->4->5->6
'''

import heapq
class Solution:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        res = head = ListNode(None)
        heap = []
        for k in range(len(lists)):
            if lists[k] is not None:
                heapq.heappush(heap, (lists[k].val, k))

        while heap:
            curr, k = heapq.heappop(heap)
            res.next = ListNode(curr)
            res = res.next

            lists[k] = lists[k].next
            if lists[k] is not None:
                heapq.heappush(heap, (lists[k].val, k))

        return head.next