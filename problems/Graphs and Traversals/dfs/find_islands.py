"""
Given a 2d grid map of '1's (land) and '0's (water), count the number of islands. An island is surrounded by water and is formed by connecting adjacent lands horizontally
 or vertically. You may assume all four edges of the grid are all surrounded by water.

Example 1:

Input:
11110
11010
11000
00000

Output: 1
"""
class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        def dfs(grid,r,c):
            if r not in range(0,len(grid)) or c not in range(0,len(grid[r])) or grid[r][c] in [ '0', 'v']:
                return
            else:
                grid[r][c] = 'v' # i.e. visited
                dfs(grid, r+1, c)
                dfs(grid, r-1, c)
                dfs(grid, r, c+1)
                dfs(grid, r, c-1)
        count = 0

        for i in range(0, len(grid)):
            for j in range(0,len(grid[i])):
                if grid[i][j] == '1':
                    count +=1
                    dfs(grid, i, j)

        return count
