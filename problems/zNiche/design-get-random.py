"""
Design a data structure that can insert, delete and return an element at random

Ref: https://leetcode.com/problems/insert-delete-getrandom-o1/
"""

class RandomizedSet:

    def __init__(self):
        self.h = collections.defaultdict(int)
        self.arr = []

    def insert(self, val: int) -> bool:
        if val not in self.h:
            self.arr.append(val)
            self.h[val] = len(self.arr) - 1
            return True
        else:
            return False

    def remove(self, val: int) -> bool:
        if val in self.h:
            # Get ready to delete element from Array and hash
            idx = self.h[val]
            idxLast = len(self.arr) - 1
            del self.h[val]

            if idx == idxLast:
                self.arr.pop()
                return True

            # Put item to delete at end of array.
            self.arr[idx], self.arr[idxLast] = self.arr[idxLast], self.arr[idx]
            self.arr.pop()
            self.h[self.arr[idx]] = idx
            return True
        else:
            return False

    def getRandom(self) -> int:
        if len(self.arr):
            r = int(random.random() * len(self.arr))
            return self.arr[r]

# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()