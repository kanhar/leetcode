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
