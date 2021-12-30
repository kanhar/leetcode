"""
You are given an n x n 2D matrix representing an image.

Rotate the image by 90 degrees (clockwise).

Note:

You have to rotate the image in-place, which means you have to modify the input 2D matrix directly. DO NOT allocate another 2D matrix and do the rotation.

Example 1:

Given input matrix =
[
  [1,2,3],
  [4,5,6],
  [7,8,9]
],

rotate the input matrix in-place such that it becomes:
[
  [7,4,1],
  [8,5,2],
  [9,6,3]
]

Ref: https://leetcode.com/problems/rotate-image/
Ref: https://leetcode.com/problems/rotate-image/discuss/18884/Seven-Short-Solutions-(1-to-7-lines)
Ref: https://stackoverflow.com/questions/42519/how-do-you-rotate-a-two-dimensional-array
"""
class Solution:
    def rotate(self, A):
        A.reverse()
        for i in range(len(A)):
            for j in range(i):
                A[i][j], A[j][i] = A[j][i], A[i][j]

class Solution:
    def rotate(self, A):
        n = len(A)
        for i in range(n//2):
            for j in range(n//2 + n%2):
                tmp = A[i][j]
                A[i][j] = A[~j][i]
                A[~j][i] = A[~i][~j]
                A[~i][~j] = A[j][~i]
                A[j][~i] = tmp