"""
You are given a binary tree in which each node contains an integer value.

Find the number of paths that sum to a given value.

The path does not need to start or end at the root or a leaf, but it must go downwards (traveling only from parent nodes to child nodes).

The tree has no more than 1,000 nodes and the values are in the range -1,000,000 to 1,000,000.

Example:

root = [10,5,-3,3,2,null,11,3,-2,null,1], sum = 8

      10
     /  \
    5   -3
   / \    \
  3   2   11
 / \   \
3  -2   1

Return 3. The paths that sum to 8 are:

1.  5 -> 3
2.  5 -> 2 -> 1
3. -3 -> 11

Ref: https://leetcode.com/problems/path-sum-iii/
Ref: Contrast with https://leetcode.com/problems/maximum-size-subarray-sum-equals-k/
"""
import collections


class Solution:
    def pathSum(self, root: TreeNode, target: int) -> int:
        def find_paths(root, target):
            if not root:
                return 0

            return int(root.val == target) + find_paths(root.left, target-root.val) + find_paths(root.right, target-root.val)

        if not root:
            return 0

        return find_paths(root, target) + self.pathSum(root.left, target) + self.pathSum(root.right, target)


class Solution:
    def pathSum(self, root: TreeNode, sum: int) -> int:
        def preorder(node: TreeNode, curr_sum) -> None:
            if not node:
                return

            curr_sum += node.val        # current prefix sum
            if curr_sum == k:
                self.totalCount += 1

            # number of times the curr_sum − k has occurred already,
            # determines the number of times a path with sum k has occurred up to the current node
            self.totalCount += h[curr_sum - k]

            # Add the current sum into hashmap to use it during the child nodes processing only
            h[curr_sum] += 1
            preorder(node.left, curr_sum)
            preorder(node.right, curr_sum)
            h[curr_sum] -= 1
            # ^ remove current sum from hashmap - to not use it during the parallel subtree processing

        totalCount, k = 0, sum
        h = collections.defaultdict(int)
        preorder(root, 0)
        return self.totalCount