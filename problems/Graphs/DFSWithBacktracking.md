{: .no_toc}
# Depth First Search
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90ojkbn2)

- TOC
{:toc}
  
### [Permutations](https://leetcode.com/problems/permutations/)

> Given a collection of distinct integers, return all possible permutations.
> Perm(n,r) = n! / ( n-r )!
> Comb(n,r) = n! / ( k! / (n-k)! )

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):
    def permute(self, arr: List[int]) -> List[List[int]]:
        def perm(arr, accum = [], visited = set()):
            if len(accum) == len(arr):
                self.res.add(tuple(accum))
            else:
                for i in range(len(arr)):
                    if i not in visited:
                        perm(arr, accum + [arr[i]], visited | set([i]))

        self.res = set()
        perm(arr)
        return self.res
```

Or...

```python
class Solution(object):
    def permute(self, nums):        
        def perm(a,k=0):
            if len(a)==k:
                self.path.append(list(a))                
            else:
                for i in range(k,len(a)):
                    a[i],a[k] = a[k],a[i]
                    perm(a,k+1)
                    a[k],a[i] = a[i],a[k]
        
        self.path = []
        perm(nums)                
        return self.path        
```

</details>
<BR>

### [Robot Room Cleaner](https://leetcode.com/problems/robot-room-cleaner/)

> This is a fun problem. Read LC description.

<details><summary markdown="span">Execute!</summary>

```python
class Solution(object):       
    def cleanRoom(self, robot):
        def rewind():
            robot.turnRight()
            robot.turnRight()
            robot.move()
            robot.turnRight()
            robot.turnRight()
        
        # going clockwise : 0: 'up', 1: 'right', 2: 'down', 3: 'left'
        def move(cell, d):
            return (cell[0] + directions[d][0], cell[1] + directions[d][1])
            
        def solve(cell = (0, 0), d = 0):
            visited.add(cell)
            robot.clean()
            
            for i in range(4):
                curr_d = (d + i) % 4
                curr_cell = move(cell, curr_d)
                
                if not curr_cell in visited:
                    if robot.move():
                        solve(curr_cell, curr_d)
                        rewind()
                        
                # turn the robot following chosen direction : clockwise
                robot.turnLeft()
    
        # going clockwise : 0: 'up', 1: 'right', 2: 'down', 3: 'left'
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        visited = set()
        solve()# so back to that cell and then turn right from your last explored direction.
```

</details>
<BR>