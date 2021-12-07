"""
Design and implement a data structure for Least Recently Used (LRU) cache.

get(key) - Get the value (will always be positive) of the key if the key exists in the cache, otherwise return -1.
put(key, value) - Set or insert the value if the key is not already present.
When the cache reached its capacity, it should invalidate the least recently used item before inserting a new item.

The cache is initialized with a positive capacity.

Follow up:
Could you do both operations in O(1) time complexity?

Ref: https://leetcode.com/problems/lru-cache/
Ref: To do yourself: https://github.com/timurridjanovic/lru-cache/tree/master/lru_cache_min_heap
"""
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
