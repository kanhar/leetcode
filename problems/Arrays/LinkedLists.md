{: .no_toc}
# Linked Lists
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=9dbla3q1)

A linked list is a chain of nodes, each pointing to the next. You cannot jump to the middle, so almost every problem is solved by walking the list with one or two pointers and carefully rewiring arrows. Two habits remove most bugs: start with a **dummy node** in front of the real head, and **save `next` before you change it**.

Next: [Doubly Linked Lists](DoublyLinkedLists.md) and the [LRU Cache](../Misc/LRUCache.md).

- TOC
{:toc}

### [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/)

> Reverse a singly linked list.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Before"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>2</b>"]
        F0_2["<b>3</b>"]
        F0_3["<b>null</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
    end
    subgraph F1 ["After: every arrow flipped"]
        direction LR
        F1_0["<b>3</b>"]
        F1_1["<b>2</b>"]
        F1_2["<b>1</b>"]
        F1_3["<b>null</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
        F1_2 --> F1_3
    end
    F0 ==>|"reverse"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F1_0,F1_1,F1_2 n
    class F0_3,F1_3 empty
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

Here is the state of `prev` and `curr` after each pass of the loop. Orange is the node that was just flipped, blue is the next node to flip. Each pass does the same four things: save `temp = curr.next`, point `curr.next` at `prev`, move `prev` to `curr`, move `curr` to `temp`.

```mermaid
%%{init: {"flowchart": {"padding": 12, "nodeSpacing": 8, "rankSpacing": 22, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph S0 ["Start"]
        direction LR
        subgraph P0 ["prev"]
            direction LR
            P0_0["<b>None</b>"]
        end
        subgraph C0 ["curr"]
            direction LR
            C0_0["<b>1</b>"]
            C0_1["<b>2</b>"]
            C0_2["<b>3</b>"]
            C0_3["<b>4</b>"]
            C0_4["<b>None</b>"]
            C0_0 --> C0_1
            C0_1 --> C0_2
            C0_2 --> C0_3
            C0_3 --> C0_4
        end
        P0 ~~~ C0
    end
    subgraph S1 ["After pass 1"]
        direction LR
        subgraph P1 ["prev"]
            direction LR
            P1_0["<b>1</b>"]
            P1_1["<b>None</b>"]
            P1_0 --> P1_1
        end
        subgraph C1 ["curr"]
            direction LR
            C1_0["<b>2</b>"]
            C1_1["<b>3</b>"]
            C1_2["<b>4</b>"]
            C1_3["<b>None</b>"]
            C1_0 --> C1_1
            C1_1 --> C1_2
            C1_2 --> C1_3
        end
        P1 ~~~ C1
    end
    subgraph S2 ["After pass 2"]
        direction LR
        subgraph P2 ["prev"]
            direction LR
            P2_0["<b>2</b>"]
            P2_1["<b>1</b>"]
            P2_2["<b>None</b>"]
            P2_0 --> P2_1
            P2_1 --> P2_2
        end
        subgraph C2 ["curr"]
            direction LR
            C2_0["<b>3</b>"]
            C2_1["<b>4</b>"]
            C2_2["<b>None</b>"]
            C2_0 --> C2_1
            C2_1 --> C2_2
        end
        P2 ~~~ C2
    end
    subgraph S3 ["After pass 3"]
        direction LR
        subgraph P3 ["prev"]
            direction LR
            P3_0["<b>3</b>"]
            P3_1["<b>2</b>"]
            P3_2["<b>1</b>"]
            P3_3["<b>None</b>"]
            P3_0 --> P3_1
            P3_1 --> P3_2
            P3_2 --> P3_3
        end
        subgraph C3 ["curr"]
            direction LR
            C3_0["<b>4</b>"]
            C3_1["<b>None</b>"]
            C3_0 --> C3_1
        end
        P3 ~~~ C3
    end
    subgraph S4 ["After pass 4: curr is None, so return prev"]
        direction LR
        subgraph P4 ["prev"]
            direction LR
            P4_0["<b>4</b>"]
            P4_1["<b>3</b>"]
            P4_2["<b>2</b>"]
            P4_3["<b>1</b>"]
            P4_4["<b>None</b>"]
            P4_0 --> P4_1
            P4_1 --> P4_2
            P4_2 --> P4_3
            P4_3 --> P4_4
        end
        subgraph C4 ["curr"]
            direction LR
            C4_0["<b>None</b>"]
        end
        P4 ~~~ C4
    end
    S0 ==> S1
    S1 ==> S2
    S2 ==> S3
    S3 ==> S4
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class P0_0,C0_4,P1_1,C1_3,P2_2,C2_2,P3_3,C3_1,P4_4,C4_0 empty
    class C0_0,C1_0,C2_0,C3_0 a
    class C0_1,C0_2,C0_3,C1_1,C1_2,P2_1,C2_1,P3_1,P3_2,P4_1,P4_2,P4_3 n
    class P1_0,P2_0,P3_0,P4_0 hi
    style S0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style P0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style C0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style S1 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style P1 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style C1 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style S2 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style P2 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style C2 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style S3 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style P3 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style C3 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style S4 fill:#f1f8e9,stroke:#689f38,color:#33691e
    style P4 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style C4 fill:#fafafa,stroke:#bdbdbd,color:#37474f
```

The same pointer flip shows up on a tree: see [Binary Tree Upside Down](../Trees/PostOrder.md#binary-tree-upside-down).

**Key intuition 1:** Walk the list and flip each arrow to point backwards, keeping a pointer to the part you have already reversed.

**Key intuition 2:** Remember the next node BEFORE you flip the arrow, or you lose the rest of the list.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head

        while curr:
            temp = curr.next

            # Core Code
            curr.next = prev
            # curr.prev = temp would make this work for a doubly linked list
            prev = curr

            curr = temp

        return prev
```

</details>
<BR>

### [Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/)

> Merge two sorted linked lists into one sorted list.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Two sorted lists"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>3</b>"]
        F0_2["<b>5</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
    end
    subgraph F1 [" "]
        direction LR
        F1_0["<b>2</b>"]
        F1_1["<b>4</b>"]
        F1_2["<b>6</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
    end
    subgraph F2 ["Merged: always take the smaller front"]
        direction LR
        F2_0["<b>1</b>"]
        F2_1["<b>2</b>"]
        F2_2["<b>3</b>"]
        F2_3["<b>4</b>"]
        F2_4["<b>5</b>"]
        F2_5["<b>6</b>"]
        F2_0 --> F2_1
        F2_1 --> F2_2
        F2_2 --> F2_3
        F2_3 --> F2_4
        F2_4 --> F2_5
    end
    F0 ==>|"merge"| F1
    F1 ==> F2
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F1_0,F1_1,F1_2,F2_0,F2_1,F2_2,F2_3,F2_4,F2_5 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F2 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Compare the two front nodes, attach the smaller one, and move that list forward. Repeat until one list runs out, then attach the rest of the other.

**Key intuition 2:** Start from a dummy node so you never need a special case for the first node.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionMerge2:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        # A dummy head means no special case for the first node.
        dummy = ListNode()
        tail = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                tail.next = list1
                list1 = list1.next
            else:
                tail.next = list2
                list2 = list2.next

            tail = tail.next

        # One list ran out: attach the rest of the other.
        tail.next = list1 or list2
        return dummy.next
```

</details>
<BR>

### [Detect Cycle](https://leetcode.com/problems/linked-list-cycle/)

> Determine whether a linked list has a cycle.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Tortoise moves 1, hare moves 2"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>2</b>"]
        F0_2["<b>3</b>"]
        F0_3["<b>4</b>"]
        F0_4["<b>back to 2</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
    end
    subgraph F1 ["They must meet inside a cycle"]
        direction LR
        F1_0["<b>they meet: cycle found</b>"]
    end
    F0 ==>|"if there is a loop"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F0_3,F1_0 n
    class F0_4 hi
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Send two runners round the list: one steps 1, the other steps 2. If the track is a loop the fast one laps the slow one and they meet; if not, the fast one falls off the end.

**Key intuition 2:** This uses O(1) memory. The alternative, remembering every node you have seen in a set, is correct but uses O(n).

<details><summary markdown="span">Execute!</summary>

```python
class SolutionCycle:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head

        while slow and fast and fast.next:
            slow = slow.next
            fast = fast.next.next

            if slow == fast:
                return True

        return False
```

</details>
<BR>

### [Remove Duplicates from Sorted List](https://leetcode.com/problems/remove-duplicates-from-sorted-list/)

> Delete all duplicates from a sorted linked list so each value appears once.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Sorted list"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>1</b>"]
        F0_2["<b>2</b>"]
        F0_3["<b>3</b>"]
        F0_4["<b>3</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
    end
    subgraph F1 ["Skip a node when it equals the next"]
        direction LR
        F1_0["<b>1</b>"]
        F1_1["<b>2</b>"]
        F1_2["<b>3</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
    end
    F0 ==>|"remove duplicates"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F0_3,F0_4,F1_0,F1_1,F1_2 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Because the list is sorted, duplicates are always next to each other. Compare each node with the next one.

**Key intuition 2:** If they are equal, skip the next node by pointing past it. Otherwise move on.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionDupes:
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

### [Remove Nth Node From End of List](https://leetcode.com/problems/remove-nth-node-from-end-of-list/)

> Remove the nth node from the end of the list.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["List, remove 2nd from the end"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>2</b>"]
        F0_2["<b>3</b>"]
        F0_3["<b>4</b>"]
        F0_4["<b>5</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
    end
    subgraph F1 ["Lead pointer is 2 steps ahead; when it falls off the end, trail is just before the target"]
        direction LR
        F1_0["<b>1</b>"]
        F1_1["<b>2</b>"]
        F1_2["<b>3</b>"]
        F1_3["<b>5</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
        F1_2 --> F1_3
    end
    F0 ==>|"remove node 4"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F0_3,F0_4,F1_0,F1_1,F1_2,F1_3 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** You cannot count from the end, but you can keep two pointers n steps apart. When the front one reaches the end, the back one is exactly where you need to be.

**Key intuition 2:** Use a dummy node so removing the head works like removing any other node.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionNth:
    def removeNthFromEnd(self, head, n):
        cur = head
        lag = head

        for i in range(0, n):
            cur = cur.next

        # Example: [1,2], n=2.
        if not cur:
            return head.next

        # Tricky: you want to be one behind for deletion.
        while cur.next:
            cur = cur.next
            lag = lag.next

        lag.next = lag.next.next

        return head
```

</details>
<BR>

### [Add Two Numbers](https://leetcode.com/problems/add-two-numbers/)

> Two numbers are stored as linked lists with the digits in reverse order. Add them and return the sum in the same form.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["342 and 465, digits stored in reverse"]
        direction LR
        F0_0["<b>2</b>"]
        F0_1["<b>4</b>"]
        F0_2["<b>3</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
    end
    subgraph F1 [" "]
        direction LR
        F1_0["<b>5</b>"]
        F1_1["<b>6</b>"]
        F1_2["<b>4</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
    end
    subgraph F2 ["807, also in reverse (carry 1 moves on)"]
        direction LR
        F2_0["<b>7</b>"]
        F2_1["<b>0</b>"]
        F2_2["<b>8</b>"]
        F2_0 --> F2_1
        F2_1 --> F2_2
    end
    F0 ==>|"add digit by digit"| F1
    F1 ==> F2
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F1_0,F1_1,F1_2,F2_0,F2_1,F2_2 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F2 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Reverse order is a gift: the first node is the ones digit, which is where schoolbook addition starts. Add digit by digit.

**Key intuition 2:** Carry the overflow to the next column. Keep going while either list or a carry remains, so a final carry becomes a new node.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionAdd:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        carry = 0

        head = ListNode(None)
        curr = head

        while l1 or l2 or carry:
            if l1:
                carry += l1.val
                l1 = l1.next

            if l2:
                carry += l2.val
                l2 = l2.next

            curr.next = ListNode(carry % 10, None)
            curr = curr.next
            carry = carry // 10

        return head.next
```

</details>
<BR>

### [Intersection of Two Linked Lists](https://leetcode.com/problems/intersection-of-two-linked-lists/)

> Find the node where two singly linked lists meet, or return null.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Two lists sharing a tail"]
        direction LR
        F0_0["<b>a1</b>"]
        F0_1["<b>a2</b>"]
        F0_2["<b>c1</b>"]
        F0_3["<b>c2</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
    end
    subgraph F1 [" "]
        direction LR
        F1_0["<b>b1</b>"]
        F1_1["<b>b2</b>"]
        F1_2["<b>b3</b>"]
        F1_3["<b>c1</b>"]
        F1_4["<b>c2</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
        F1_2 --> F1_3
        F1_3 --> F1_4
    end
    subgraph F2 ["Answer: the shared node"]
        direction LR
        F2_0["<b>c1</b>"]
    end
    F0 ==> F1
    F1 ==>|"first common node"| F2
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F1_0,F1_1,F1_2,F2_0 n
    class F0_2,F0_3,F1_3,F1_4 hi
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F2 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** Two lists that merge share the same tail, but the lengths before the merge can differ, so walking them side by side misses the meeting point.

**Key intuition 2:** Let each pointer walk its own list and then jump to the head of the other list. Both walk the same total distance, so they line up at the intersection (or both reach null).

<details><summary markdown="span">Execute!</summary>

Using a set (easy to think of, O(n) extra memory):

```python
class SolutionIntersect:
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

Two pointers (O(1) extra memory):

```python
class SolutionIntersect2:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        a = headA
        b = headB

        while a is not b:
            # At the end of A, carry on along B.
            a = a.next if a else headB

            # And the other way round.
            b = b.next if b else headA

        # The intersection, or None if the lists never meet.
        return a
```

</details>
<BR>

### [Palindrome Linked List](https://leetcode.com/problems/palindrome-linked-list/)

> Determine whether a linked list reads the same forwards and backwards.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["List"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>2</b>"]
        F0_2["<b>2</b>"]
        F0_3["<b>1</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
    end
    subgraph F1 ["Reverse the second half, compare both halves"]
        direction LR
        F1_0["<b>1 2</b>"]
        F1_1["<b>1 2</b>"]
        F1_0 --> F1_1
    end
    F0 ==>|"is it a palindrome?"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F0_3,F1_0,F1_1 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** A palindrome mirrors around its middle. Find the middle with fast and slow pointers.

**Key intuition 2:** Reverse the second half in place, then compare it with the first half node by node. This combines three earlier tricks: fast/slow, reverse, compare.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionPalin:
    def isPalindrome(self, head: ListNode) -> bool:

        def solve(B):
            if B is None:
                return True

            # Tail up recursion.
            if not solve(B.next) or self.A.val != B.val:
                return False

            self.A = self.A.next
            return True

        self.A = head

        return solve(head)
```

</details>
<BR>

## Harder: come back to these

### [Reorder List](https://leetcode.com/problems/reorder-list/)

> Reorder L0 → L1 → … → Ln into L0 → Ln → L1 → Ln-1 → L2 → …, in place.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Before"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>2</b>"]
        F0_2["<b>3</b>"]
        F0_3["<b>4</b>"]
        F0_4["<b>5</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
        F0_2 --> F0_3
        F0_3 --> F0_4
    end
    subgraph F1 ["After: front, back, front, back"]
        direction LR
        F1_0["<b>1</b>"]
        F1_1["<b>5</b>"]
        F1_2["<b>2</b>"]
        F1_3["<b>4</b>"]
        F1_4["<b>3</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
        F1_2 --> F1_3
        F1_3 --> F1_4
    end
    F0 ==>|"interleave"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F0_3,F0_4,F1_0,F1_1,F1_2,F1_3,F1_4 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** It is three small problems glued together: find the middle (fast/slow), reverse the second half, then weave the two halves together.

**Key intuition 2:** Cut the list in two at the middle before weaving, or the last node will still point back into the list and create a cycle.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionReorder:
    def reorderList(self, head: ListNode) -> None:
        if not head:
            return

        # 1. Find the middle: when fast reaches the end, slow is halfway.
        slow = head
        fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 2. Reverse the second half in place.
        prev = None
        curr = slow
        while curr:
            tmp = curr.next
            curr.next = prev
            prev = curr
            curr = tmp

        # 3. Merge the two halves, alternating one node from each.
        first = head
        second = prev
        while second.next:
            tmp = first.next
            first.next = second
            first = tmp

            tmp = second.next
            second.next = first
            second = tmp
```

</details>
<BR>

### [Merge K Sorted Lists](https://leetcode.com/problems/merge-k-sorted-lists/)

> Merge k sorted linked lists into one sorted list.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["K sorted lists"]
        direction LR
        F0_0["<b>1</b>"]
        F0_1["<b>4</b>"]
        F0_0 --> F0_1
    end
    subgraph F1 [" "]
        direction LR
        F1_0["<b>2</b>"]
        F1_1["<b>5</b>"]
        F1_0 --> F1_1
    end
    subgraph F2 [" "]
        direction LR
        F2_0["<b>3</b>"]
        F2_1["<b>6</b>"]
        F2_0 --> F2_1
    end
    subgraph F3 ["One sorted list"]
        direction LR
        F3_0["<b>1</b>"]
        F3_1["<b>2</b>"]
        F3_2["<b>3</b>"]
        F3_3["<b>4</b>"]
        F3_4["<b>5</b>"]
        F3_5["<b>6</b>"]
        F3_0 --> F3_1
        F3_1 --> F3_2
        F3_2 --> F3_3
        F3_3 --> F3_4
        F3_4 --> F3_5
    end
    F0 ==> F1
    F1 ==> F2
    F2 ==>|"merge all"| F3
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F1_0,F1_1,F2_0,F2_1,F3_0,F3_1,F3_2,F3_3,F3_4,F3_5 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F2 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F3 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** The smallest remaining node is always at the front of one of the k lists. A min-heap of those k fronts always gives you the next one in O(log k).

**Key intuition 2:** Pop the smallest, attach it, and push that node's next node into the heap.

<details><summary markdown="span">Execute!</summary>

```python
import heapq

class SolutionMergeK:
    def mergeKLists(self, lists: List[ListNode]) -> ListNode:
        head = ListNode(None)
        res = head
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

### [Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/)

> Each node has a next pointer and a random pointer. Return a deep copy.

```mermaid
%%{init: {"flowchart": {"padding": 14, "nodeSpacing": 10, "rankSpacing": 34, "subGraphTitleMargin": {"top": 6, "bottom": 22}}, "themeVariables": {"fontSize": "22px"}}}%%
flowchart TB
    subgraph F0 ["Original: next arrows and random arrows"]
        direction LR
        F0_0["<b>A</b>"]
        F0_1["<b>B</b>"]
        F0_2["<b>C</b>"]
        F0_0 --> F0_1
        F0_1 --> F0_2
    end
    subgraph F1 ["Copy: new nodes, same shape"]
        direction LR
        F1_0["<b>A'</b>"]
        F1_1["<b>B'</b>"]
        F1_2["<b>C'</b>"]
        F1_0 --> F1_1
        F1_1 --> F1_2
    end
    F0 ==>|"deep copy"| F1
    classDef n fill:#f5f5f5,stroke:#9e9e9e,color:#424242
    classDef hi fill:#fff3e0,stroke:#e65100,stroke-width:3px,color:#bf360c
    classDef a fill:#e3f2fd,stroke:#1565c0,color:#0d47a1
    classDef g fill:#e8f5e9,stroke:#2e7d32,color:#1b5e20
    classDef p fill:#f3e5f5,stroke:#6a1b9a,color:#4a148c
    classDef r fill:#ffebee,stroke:#c62828,color:#b71c1c
    classDef y fill:#fff8e1,stroke:#f9a825,color:#5d4037
    classDef c fill:#e0f7fa,stroke:#00838f,color:#006064
    classDef txt fill:none,stroke:none,color:#e65100
    classDef ghost fill:none,stroke:none,color:transparent
    classDef empty fill:#ffffff,stroke:#bdbdbd,stroke-dasharray:4 3,color:#9e9e9e
    class F0_0,F0_1,F0_2,F1_0,F1_1,F1_2 n
    style F0 fill:#fafafa,stroke:#bdbdbd,color:#37474f
    style F1 fill:#f1f8e9,stroke:#689f38,color:#33691e
```

**Key intuition 1:** The hard part is a random pointer to a node you have not copied yet. Solve it by first creating a copy of every node and remembering original → copy.

**Key intuition 2:** Then fill in next and random for each copy by looking their targets up in that map.

<details><summary markdown="span">Execute!</summary>

```python
class SolutionCopy:
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

