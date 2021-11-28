# initialize a dict with Default Values
a = dict(zip(['Mon', 'Tue', 'Wed', 'Thu', 'Fri'], [x for x in range(1, 6)]))
s = "someword"
b = dict(zip(list(s), [False] * len(s)))
print(a, "\n", b)
import collections

a = {}
a = collections.defaultdict(lambda: False, a)
print("equal to false", a["hi"], list(a.values()), list(a.keys()))
# tmp = {k:v for k,v in visited.items() if v==True}
# see return statement below
# return [res[i] for i in sorted(res)]


# dynamically add to set

s = set([1, 2]) | set([3])
print(s)

# dict
d1 = dict({1: 'apple', 2: 'ball'})
d2 = dict({3: 'bat'})
d = {**d1, **d2}
print(d)

# priority queue
from queue import PriorityQueue

q = PriorityQueue()
q.put((1, 4, 'ten'))
q.put((1, 3, 'one'))
q.put((5, 1, 'five'))
while not q.empty():
    print(q.get())

# reverse
x = "abc"
y = x[::-1]
print(x, y)

# Ref: https://leetcode.com/problems/single-number/
import collections
from typing import List


class Solution:
    # Given a non-empty sort of integers, every element appears twice except for one. Find that single one
    def singleNumber(self, nums: List[int]) -> int:
        return next(iter({k: v for (k, v) in collections.Counter(nums).items() if v == 1}))

    def singleNumber2(self, nums: List[int]) -> int:
        return sorted(collections.Counter(nums).items(), key=lambda x: x[1])[0][0]


def topKFrequentQueue(items, k):
    q = queue.PriorityQueue()
    for k, v in items:
        q.put((-v, k))
    res = []
    for i in range(k):
        res.append(q.get()[1])
    return res


def isNumber(self, s):
    import re

    pattern = "^([+-])?((\d+(\.\d*)?)|(\.\d+))(e[+-]?\d+)?$"
    s = s.strip()
    return re.search(pattern, s) is not None


def getall(s, d):
    res = []
    for i in range(1, len(s) + 1):
        if s[:i] in d:
            res += [s[:i]] + getall(s[i:], d)
    return res


d = ["bed", "bat", "bath", "and", "hand", "beyond"]
s = "bedbathandbeyond";
print(getall(s, d) == ['bed', 'bat', 'hand', 'beyond', 'bath', 'and', 'beyond'])


# print(2**5, 1<<5) #Really that is 2^0 (aka 1 ) <<5
# print(100/2 == 100>>1 )

def p(n):
    return format(n, '#032b')


# 10
# 100
# 10000
def ispowerof2(num):
    return ((num & (num - 1)) == 0) and num > 0


print(p(15))
print(ispowerof2(16))
print(int.bit_length(16) - 1)

import copy


def emptyMatrix(R, C):
    return [[0 for i in range(C)] for j in range(R)]  # @UnusedVariable


def copyMatrix(A):
    B = copy.deepcopy(A)
    return B


# You have an sort [2, 1, 8, 3, 8, 7, 8]. You need to return an index of the maximum value uniformly.
import random


def GetMax(arr):
    m = max(arr)
    count = 0
    for i in range(0, len(arr)):
        if arr[i] == m:
            count = count + 1

    r = int(random.random() * count)
    res = [x for x in arr if x == m]
    return res[r]


print(GetMax([2, 1, 8, 3, 8, 7, 8]))

# Only a pre-post order traversal can transform a tree. Not an inorder. Guess why?
# low + (high - low) / 2 -> Version 2. Always better

# Reverse sort
nums = [1, 2, 3]
nums[:] = nums[::-1]

class TreeNode:

    def __init__(self, value=None, left=None, right=None, parent=None):
        self.right = right
        self.left = left
        self.val = value
        self.parent = parent

    def toStr(self, depth=0):
        ret = ""

        if self.right != None:
            ret += self.right.toStr(depth + 1)

        if( self.val is not None):
            ret += "\n" + ("   "*depth) + str(self.val)

        if self.left != None:
            ret += self.left.toStr(depth + 1)

        return ret

def create(arr, start=0, end=None):
    if end is None:
        end = len(arr)-1

    if start > end:
        return None
    mid         = int((start + end) / 2)
    return TreeNode(arr[mid], create(arr, start, mid - 1), create(arr, mid + 1, end))

def inOrder(root):
    res = []
    tmp = root
    def solve(root):
        if root:
            solve(root.left)
            res.append(root.val)
            solve(root.right)

    solve(tmp)
    return res

def preOrder(root):
    res = []
    tmp = root
    def solve(root):
        if root:
            res.append(root.val)
            solve(root.right)
            solve(root.right)

    solve(tmp)
    return res

def postOrder(root):
    res = []
    tmp = root
    def solve(root):
        if root:
            solve(root.right)
            solve(root.left)
            res.append(root.val)

    solve(tmp)
    return res

arr = [x for x in range(1,8)]
tree = create(arr)
print(tree.toStr())

print(inOrder(tree))
print(preOrder(tree))
print(postOrder(tree))