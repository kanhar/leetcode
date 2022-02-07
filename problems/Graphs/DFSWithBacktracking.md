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
        # Take a U-Turn, move back. U-turn, face where you were originally facing.
        def rewind():
            robot.turnRight()
            robot.turnRight()
            robot.move()
            robot.turnRight()
            robot.turnRight()
           
        def solve(cell, d ):
            visited.add(cell)
            robot.clean()
            
            for i in range(4):
                c_d = (d + i) % 4
                curr_cell = (cell[0] + directions[c_d][0], cell[1] + directions[c_d][1])
                
                if not curr_cell in visited:
                    if robot.move():
                        solve(curr_cell, c_d)
                        rewind()
                        
                # Important to maintain spiral order
                robot.turnLeft()
    
        # going clockwise : 0: 'up', 1: 'right', 2: 'down', 3: 'left'
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        visited = set()
        start = (0,0)
        d = 0
        
        solve(start, 0 )
```

</details>
<BR>


### [Word Search](https://kanhar.github.io/leetcode/problems/Trees/Tries.html#word-search)

See use of Backtracking here: [Tries.html#word-search](https://kanhar.github.io/leetcode/problems/Trees/Tries.html#word-search)