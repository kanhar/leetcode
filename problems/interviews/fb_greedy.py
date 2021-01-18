'''
Slow Sums
Suppose we have a list of N numbers, and repeat the following operation until we're left with only a single number:
Choose any two consecutive numbers and replace them with their sum. Moreover, we associate a penalty with each operation equal to the value of the new number,
 and call the penalty for the entire list as the sum of the penalties of each operation.
Note: Consecutive numbers means that their indices in the array are consecutive, not that their values are consecutive.
For example, given the list [1, 2, 3, 4, 5], we could choose 2 and 3 for the first operation, which would transform the list into [1, 5, 4, 5] and incur a penalty of 5.
The goal in this problem is to find the worst possible penalty for a given input.
Signature:
int getTotalTime(int[] arr)
Input:
An array arr containing N integers, denoting the numbers in the list.
Output format:
An int representing the worst possible total penalty.
Constraints:
1 ≤ N ≤ 106
1 ≤ Ai ≤ 107, where *Ai denotes the ith initial element of an array.
The sum of values of N over all test cases will not exceed 5 * 106.
Example
arr = [4, 2, 1, 3]
output = 23
First, add 4 + 2 for a penalty of 6. Now the array is [6, 1, 3]
Add 6 + 1 for a penalty of 7. Now the array is [7, 3]
Add 7 + 3 for a penalty of 10. The penalties sum to 23.
'''


def getTotalTime(arr):
    def solve(arr, idx = 0, accum = 0 ):
        global res
        if len(arr)== 1:
            res = accum
        else:
            mx = [0,1]
            for i in range(1, len(arr)):
                if arr[i-1] + arr[i] > arr[mx[0]] + arr[mx[1]]:
                    mx = [i-1, i]

            arr[mx[1]] = arr[mx[0]] + arr[mx[1]]
            arr[mx[0]] = float('-inf')
            accum += arr[mx[1]]

            tmp = [x for x in arr if x != float('-inf')]
            solve(tmp, idx + 1, accum)

    global res
    res = 0
    solve(arr)
    return res

print(88 == getTotalTime( [2, 3, 9, 8, 4]))

'''
Seating Arrangements
There are n guests attending a dinner party, numbered from 1 to n. The ith guest has a height of arr[i] inches.
The guests will sit down at a circular table which has n seats, numbered from 1 to n in clockwise order around the table. As the host, you will choose how to arrange the guests, one per seat. Note that there are n! possible permutations of seat assignments.
Once the guests have sat down, the awkwardness between a pair of guests sitting in adjacent seats is defined as the absolute difference between their two heights. Note that, because the table is circular, seats 1 and n are considered to be adjacent to one another, and that there are therefore n pairs of adjacent guests.
The overall awkwardness of the seating arrangement is then defined as the maximum awkwardness of any pair of adjacent guests. Determine the minimum possible overall awkwardness of any seating arrangement.
Signature
int minOverallAwkwardness(int[] arr)
Input
n is in the range [3, 1000].
Each height arr[i] is in the range [1, 1000].
Output
Return the minimum achievable overall awkwardness of any seating arrangement.
Example
n = 4
arr = [5, 10, 6, 8]
output = 4
If the guests sit down in the permutation [3, 1, 4, 2] in clockwise order around the table (having heights [6, 5, 8, 10], in that order), then the four awkwardnesses between pairs of adjacent guests will be |6-5| = 1, |5-8| = 3, |8-10| = 2, and |10-6| = 4, yielding an overall awkwardness of 4. It's impossible to achieve a smaller overall awkwardness.
'''

import math
import heapq
import copy

def getSum(arr):
    arr.append(arr[0])
    res = float('-inf')
    for i in range(1, len(arr)):
        res = max(res, abs(arr[i]-arr[i-1]) )
    return res


def minOverallAwkwardness(arr):
    minSum = float('inf')
    for i in range(len(arr)):
        cpy = copy.deepcopy(arr)
        cpy[0], cpy[i] = cpy[i], cpy[0]
        minSum = min(minSum,getSum(cpy))

    return minSum

print(4 == minOverallAwkwardness([5, 10, 6, 8]))
print(4 == minOverallAwkwardness([1, 2, 5, 3, 7]))