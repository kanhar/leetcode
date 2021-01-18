'''
Pair Sums
Given a list of n integers arr[0..(n-1)], determine the number of different pairs of elements within it which sum to k.
If an integer appears in the list multiple times, each copy is considered to be different; that is, two pairs are considered different if one pair includes at least one array index
which the other doesn't, even if they include the same values.

Signature
    int numberOfWays(int[] arr, int k)
Input
    n is in the range [1, 100,000].
    Each value arr[i] is in the range [1, 1,000,000,000].
    k is in the range [1, 1,000,000,000].
Output
    Return the number of different pairs of elements which sum to k.

Example
n = 5
k = 6
arr = [1, 5, 3, 3, 3]
output = 4
There's one valid pair 1+5, and three different valid pairs 3+3 (the 3rd and 4th elements, 3rd and 5th elements, and 4th and 5th elements).
'''
import collections

def numberOfWays(arr, k):
    h = collections.defaultdict(list)
    for i,a in enumerate(arr):
        h[a].append(i)

    res = set()
    for i,a in enumerate(arr):
        if k-a in h:
            tmp = [tuple(sorted([i,x])) for x in h[k-a] if x != i ]
            for t in tmp:
                res.add(t)

    return num(res)

