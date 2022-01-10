# LRU Cache
### [LRU Cache - Ordered Dict](https://leetcode.com/problems/lru-cache/)

Design and implement a data structure for Least Recently Used (LRU) cache.

<details><summary markdown="span">Let's see some code!</summary>

```python
class LRUCache:
    def __init__(self, capacity: int):
        self.count = 0
        self.capacity = capacity
        self.dic = collections.OrderedDict()

    def get(self, key: int) -> int:
        if key in self.dic:
            self.dic[key] = self.dic.pop(key)
            return self.dic[key]
        else:
            return -1

    def put(self, key: int, value: int) -> None:
        if key in self.dic:
            self.dic.pop(key)
            self.dic[key] = value
        else:
            if self.count < self.capacity:
                self.dic[key] = value
                self.count+=1
            else:
                self.dic.popitem(last=False)
                self.dic[key] = value
                self.count+=1
```

</details>
<BR>

### [LRU Cache - Custom with Heap](https://leetcode.com/problems/lru-cache/)

<details><summary markdown="span">Let's see some code!</summary>

```python
import heapq

class LRUCache:
    def __init__(self, capacity):
        self.dic = {}  # stores Keys
        self.heap = []  # stores time ordering of Keys.

        self.capacity = capacity
        self.count = 0
        self.counter = 0

    def get(self, key):
        if key not in self.dic:
            return -1
        else:
            self.updateHeap(key)
            return self.dic[key]

    def put(self, key, value):
        if key in self.dic:
            self.updateHeap(key)
            self.dic[key] = value
        elif self.count >= self.capacity:
            _, delKey = heapq.heappop(self.heap)
            del self.dic[delKey]
            self.addToHeap(key)
            self.dic[key] = value
        else:
            self.count += 1
            self.addToHeap(key)
            self.dic[key] = value

    def getOrdering(self):
        self.counter += 1
        return self.counter

    def addToHeap(self, key):
        heapq.heappush(self.heap, (self.getOrdering(), key))

    def updateHeap(self, key):
        for i in range(len(self.heap)):
            if self.heap[i][1] == key:
                self.heap[i] = (self.getOrdering(), key)

        heapq.heapify(self.heap)
```

</details>
<BR>
