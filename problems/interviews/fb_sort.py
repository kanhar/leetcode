'''
Balanced Split
Given a set of integers (which may include repeated integers), determine if there's a way to split the set into two subsets A and B such that
the sum of the integers in both sets is the same, and all of the integers in A are strictly smaller than all of the integers in B.
Signature
bool balancedSplitExists(int[] arr)
Input
All integers in array are in the range [0, 1,000,000,000].
Output
Return true if such a split is possible, and false otherwise.
Example 1
arr = [1, 5, 7, 1]
output = true
We can split the set into A = {1, 1, 5} and B = {7}.
Example 2
arr = [12, 7, 6, 7, 6]
output = false
We can't split the set into A = {6, 6, 7} and B = {7, 12} since this doesn't satisfy the requirement that all integers in A are smaller than all integers in B.
'''

def balancedSplitExists(arr):

    def solve(arr, mid):
        if mid not in range(len(arr)):
            return False
        left  = sum(arr[:mid])
        right = sum(arr[mid:])
        if left == right:
            return arr[mid-1] != arr[mid]
        elif left < right:
            return solve(arr, mid + 1)
        else:
            return solve(arr, mid - 1)

    return solve(sorted(arr), (len(arr)-1)//2 )


'''
Counting Triangles
Given a list of N triangles with integer side lengths, determine how many different triangles there are. Two triangles are considered to be the same if they can both be placed on the plane such that their vertices occupy exactly the same three points.
Signature
int countDistinctTriangles(int[][] triangles)
int countDistinctTriangles(Triangle[] triangles)
Input
In some languages triangles is an Nx3 array where triangles[i] is a length-3 array that contains the side lengths of the ith triangle. In other languages, triangles is a list of structs/objects that each represent a single triangle with side lengths a, b, and c.
It's guaranteed that all triplets of side lengths represent real triangles.
All side lengths are in the range [1, 1,000,000,000]
1 <= N <= 1,000,000
Output
Return the number of distinct triangles in the list.
Example 1
triangles = [[2, 2, 3], [3, 2, 2], [2, 5, 6]]
output = 2
The first two triangles are the same, so there are only 2 distinct triangles.
Example 2
triangles = [[8, 4, 6], [100, 101, 102], [84, 93, 173]]
output = 3
All of these triangles are distinct.
Example 3
triangles = [[5, 8, 9], [5, 9, 8], [9, 5, 8], [9, 8, 5], [8, 9, 5], [8, 5, 9]]
output = 1
'''

def countDistinctTriangles(arr):
    h = set()
    for a in arr:
        h.add(tuple(sorted(a)))
    return len(h)

