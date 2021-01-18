'''
Given an array where elements are sorted in ascending order, convert it to a height balanced BST.

For this problem, a height-balanced binary tree is defined as a binary tree in which the depth of the two subtrees of every node never differ by more than 1.

Example:

Given the sorted array: [-10,-3,0,5,9],

One possible answer is: [0,-3,9,-10,null,5], which represents the following height balanced BST:

      0
     / \
   -3   9
   /   /
 -10  5
'''
class Solution:
    def sortedArrayToBST(self, arr: List[int], start = 0, end = None) -> TreeNode:
        if end is None:
            end = len(arr)-1

        if start > end:
            return None
        else:
            mid = (start+end)//2
            return TreeNode(arr[mid], self.sortedArrayToBST(arr, start, mid - 1), self.sortedArrayToBST(arr, mid + 1, end))


