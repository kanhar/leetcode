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
import collections

class LRUCache:
    def __init__(self, capacity):
        self.dic = collections.OrderedDict()
        self.capacity = capacity
        self.count = 0

    def get(self, key):
        if key not in self.dic:
            return -1
        else:
            self.dic[key] = self.dic.pop(key)    # set key as the newest one
            return self.dic[key]

    def put(self, key, value):
        if key in self.dic:
            self.dic.pop(key)
        elif self.count >= self.capacity:
            self.dic.popitem(last=False)
        else:
            self.count += 1

        self.dic[key] = value
