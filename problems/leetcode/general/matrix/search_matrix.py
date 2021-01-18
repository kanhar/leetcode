'''
Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:

Integers in each row are sorted from left to right.
The first integer of each row is greater than the last integer of the previous row.
Example 1:

Input:
matrix = [
  [1,   3,  5,  7],
  [10, 11, 16, 20],
  [23, 30, 34, 50]
]
target = 3
Output: true
Ref: https://leetcode.com/problems/search-a-2d-matrix/
'''

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:

        def bsearch(arr, target, left=0, right=None):
            if right is None:
                right = len(arr)-1

            if left > right:
                return False
            else:
                mid = (left+right)//2
                if arr[mid] == target:
                    return True
                elif target > arr[mid]:
                    return bsearch(arr,target,mid+1,right)
                else:
                    return bsearch(arr,target,left,mid-1)

        start = 0
        end = len(matrix) - 1

        while start <= end:
            mid = (start+end)//2
            if len(matrix[mid])==0:
                return False
            elif bsearch( matrix[mid], target ):
                return True
            elif target < matrix[mid][0]:
                end = mid-1
            else:
                start = mid+1

        return False


'''
Write an efficient algorithm that searches for a value in an m x n matrix. This matrix has the following properties:

Integers in each row are sorted in ascending from left to right.
Integers in each column are sorted in ascending from top to bottom.
Example:

Consider the following matrix:

[
  [1,   4,  7, 11, 15],
  [2,   5,  8, 12, 19],
  [3,   6,  9, 16, 22],
  [10, 13, 14, 17, 24],
  [18, 21, 23, 26, 30]
]
Given target = 5, return true.

Given target = 20, return false.'''
class Solution:
    def searchMatrix(self, matrix, target):
        def dfs(m, r,c):
            if r in range(0,len(m)) and c in range(0,len(m[0])):
                if m[r][c] == target:
                    return True
                elif m[r][c] > target:  #move down
                    return dfs(m,r-1,c)
                elif m[r][c] < target:  #move right
                    return dfs(m,r,c+1)
            else:
                return False

        if len(matrix) == 0 or len(matrix[0]) == 0:
            return False
        else:
            return dfs(matrix ,len(matrix)-1, 0)