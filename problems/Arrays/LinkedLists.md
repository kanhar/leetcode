{: .no_toc}
# Linked Lists
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=9dbla3q1)

- TOC
{:toc}

### [Deep Copy](https://leetcode.com/problems/copy-list-with-random-pointer/)

> A linked list is given such that each node contains an additional random pointer which could point to
any node in the list or null. Return a deep copy of the list.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        d = collections.defaultdict(lambda: Node(0, None, None))

        newHead = None
        while head:
            d[head].val = head.val
            d[head].next = d[head.next] if head.next else None
            d[head].random = d[head.random] if head.random else None

            if newHead == None:
                newHead = d[head]

            head = head.next

        return newHead
```

</details>
<BR>

### [Detect Cycle](https://leetcode.com/problems/linked-list-cycle/)

> Given a linked list, determine if it has a cycle in it.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head
        while slow and fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False

```

</details>
<BR>


### [Intersection](https://leetcode.com/problems/intersection-of-two-linked-lists/) <BR>

> Write a program to find the node at which the intersection of two singly linked lists begins. Else return null

<details><summary markdown="span">Let's see some code!</summary>

```python
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
```

</details>
<BR>

### [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

> Merge k sorted linked lists and return it as one sorted list.

<details><summary markdown="span">Let's see some code!</summary>

```python
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
```

</details>
<BR>

### [Palindrome](https://leetcode.com/problems/palindrome-linked-list/)

> Given a singly linked list, determine if it is a palindrome.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def isPalindrome(self, head: ListNode) -> bool:

        def solve(B):
            if B is None:
                return True
            else:
                # Tail up recursion
                if not solve(B.next) or self.A.val != B.val:
                    return False
                else:
                    self.A = self.A.next
                    return True

        self.A = head

        return solve(head)
```

</details>
<BR>

### [Remove Nth Node from end of list](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

> Given a linked list, remove the n-th node from the end of list and return its head.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def removeNthFromEnd(self, head, n):
        cur = lag = head

        for i in range(0,n):
            cur = cur.next

        if not cur:             # Ex: [1,2], n=2.
            return head.next

        while cur.next:         # Tricky. You want to be one behind for deletion.
            cur = cur.next
            lag = lag.next

        lag.next = lag.next.next

        return head
```

</details>
<BR>

### [Remove Duplicates](https://leetcode.com/problems/remove-duplicates-from-sorted-list/)

> Given a sorted linked list, delete all duplicates such that each element appear only once.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:

        curr = head
        while curr:
            while curr and curr.next and curr.val == curr.next.val:
                curr.next = curr.next.next

            curr = curr.next

        return head
```

</details>
<BR>

### [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list)

> Reverse a singly linked list. [See also](https://medium.com/outco/reversing-a-linked-list-easy-as-1-2-3-560fbffe2088)

<details><summary markdown="span">Let's see some code!</summary>

```python
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
```

</details>
<BR>