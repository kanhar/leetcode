'''

Reverse to Make Equal
Given two arrays A and B of length N, determine if there is a way to make A equal to B by reversing any subarrays from array B any number of times.
Signature
bool areTheyEqual(int[] arr_a, int[] arr_b)
Input
All integers in array are in the range [0, 1,000,000,000].
Output
Return true if B can be made equal to A, return false otherwise.
Example
A = [1, 2, 3, 4]
B = [1, 4, 3, 2]
output = true
After reversing the subarray of B from indices 1 to 3, array B will equal array A.
'''

import math
import collections

def reverse(arr, i, j):
    while i < j:
        arr[i], arr[j] = arr[j], arr[i]
        h[arr[i]], h[arr[j]] = h[arr[j]], h[arr[i]]
        i+=1
        j-=1

def are_they_equal(array_a, array_b):
    global h
    h = collections.defaultdict(lambda x: -1)
    for i,b in enumerate(array_b):
        h[b] = i

    for i in range(len(array_a)):
        a = array_a[i]
        b = array_b[i]
        if a != b:
            if a not in h or h[a] < i:
                return False

            reverse(array_b, i, h[a])
    return True

print(True == are_they_equal([5, 1, 2, 3, 4], [1, 2, 3, 4, 5]  ))
print(True == are_they_equal([1,4], [4,1]  ))
print(True == are_they_equal([1,3,3,4], [3,3,1,4]  ))
print(True == are_they_equal([1,3,3,4], [1,4,3,3]  ))