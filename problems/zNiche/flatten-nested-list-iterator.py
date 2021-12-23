"""

Iterators, have two properties, hasNext() ( also known as peek() ) and next().
Imagine if an iterator has in its next() another iterator. How would you flatten it?

Ref: https://leetcode.com/problems/flatten-nested-list-iterator/
"""

class NestedIterator(object):
    def __init__(self, nestedList):
        self.flatList = []
        self.i = 0

        self.flatten(nestedList)

    def flatten(self, nestedList):
        for item in nestedList:
            if item.isInteger():
                self.flatList.append(item.getInteger())
            else:
                self.flatten(item.getList())

    def next(self):
        tmp = self.flatList[self.i]
        self.i += 1
        return tmp

    def hasNext(self):
        return self.i < len(self.flatList)