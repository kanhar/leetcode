{: .no_toc}
# Matrices
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=9dunhxke)

- TOC
{:toc}

### [Rotate Matrix](https://leetcode.com/problems/rotate-image/)

> Rotate Matrix 90 degrees, in place.
> [See also](https://stackoverflow.com/questions/42519/how-do-you-rotate-a-two-dimensional-array)
<details><summary markdown="span">Let's see some code!</summary>

```python
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
```

</details>
<BR>

### [Sparse Matrix Multiplication](https://leetcode.com/problems/sparse-matrix-multiplication/)

> Multiply large matrices. 
> Remember, multiplying an m×n matrix by an n×p matrix, result is an mxp matrix
> Haven't found an optimization (yet) for sparse matrices

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def multiply(self, A, B):
        def dotProduct(x, y):
            return sum(a * b for a, b in zip(x, y))

        # To multiply an m×n matrix by an n×p matrix, the n's must be the same,
        # and the result is an m×p matrix.

        # Inner expression is column, outside rows
        res = [[0 for x in range(len(B[0]))] for y in range(len(A))]

        for i in range(len(A)):
            for j in range(len(B[0])):
                res[i][j] = dotProduct(A[i], [x[j] for x in B])

        return res
```

</details>
<BR>

### [Traverse Matrix in a Spiral](https://leetcode.com/problems/spiral-matrix/)
> Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order.
 
<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def spiralOrder(self, m: List[List[int]]) -> List[int]:
        def add(t1):
            nonlocal r, c
            r, c = r + t1[0], c + t1[1]

        def sub(t1):
            nonlocal r, c
            r, c = r - t1[0], c - t1[1]

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        res = []
        count = 0
        total = len(m) * len(m[0])

        curr = 0
        r, c = 0, 0
        while count < total:
            res.append(m[r][c])
            m[r][c] = 'z'
            count += 1
            add(directions[curr])

            if r not in range(len(m)) or c not in range(len(m[0])) or m[r][c] == 'z':
                sub(directions[curr])
                curr = (curr + 1) % 4
                add(directions[curr])

        return res

class Solution:
    def spiralOrder(self, m: List[List[int]]) -> List[int]:

        def solve(m, accum = [] ):
            if len(m)==0:
                return accum
            else:
                accum += list(m.pop(0))
                m = list(zip(*m))[::-1]
                return solve(m, accum)

        return solve(m)
```
</details>
<BR>

### [Traverse Matrix Diagonally](https://leetcode.com/problems/diagonal-traverse/)

> Traverse Matrix diagonally.

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def findDiagonalOrder(self, matrix: List[List[int]]) -> List[int]:
        m = len(matrix)
        n = len(matrix[0])
        start = [(0,i) for i in range(n)] + [(j,n-1) for j in range(1,m)]
        
        res = []
        count = 0
        for r,c in start:
            tmp = []
            while r in range(m) and c in range(n):
                tmp.append(matrix[r][c])
                r+=1
                c-=1
            
            if count %2 ==0:
                tmp.reverse()
                
            count+=1
            res+= tmp
        
        return res
```

</details>
<BR>