{: .no_toc}
# Matrices
Practise here: [Leetcode](https://leetcode.com/list/?selectedList=9dunhxke)

- TOC
{:toc}

### Diagonal Traverse

> Traverse Matrix diagonally. 
> [Leetcode](https://leetcode.com/problems/diagonal-traverse/)

<details><summary markdown="span">Let's see some code!</summary>

```python
class Solution:
    def findDiagonalOrder(self, matrix: List[List[int]]) -> List[int]:
        m, n = len(matrix), len(matrix and matrix[0])

        res = []
        count = 0

        # get top row + right col ( rightmost edge is counted twice, hence --> for i in range(n-1))
        indices = [(0, i) for i in range(n - 1)] + [(j, n - 1) for j in range(m)]
        while indices:
            (r, c) = indices.pop(0)

            tmp = []
            while r < m and c >= 0:
                tmp.append(matrix[r][c])
                r += 1
                c -= 1

            if count % 2 == 0:
                tmp.reverse()

            count += 1
            res += tmp

        return res
```

</details>
<BR>

### Rotate Matrix

> Rotate Matrix 90 degrees, in place.
> [Leetcode](https://leetcode.com/problems/rotate-image/)
> Ref: https://leetcode.com/problems/rotate-image/discuss/18884/Seven-Short-Solutions-(1-to-7-lines)
> Ref: https://stackoverflow.com/questions/42519/how-do-you-rotate-a-two-dimensional-array
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

### Sparse Matrix Multiplication

> Multiple large matrices
> [Leetcode](https://leetcode.com/problems/sparse-matrix-multiplication/)
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

### Spiral Matrix
> Given a matrix of m x n elements (m rows, n columns), return all elements of the matrix in spiral order.
> [Leetcode](https://leetcode.com/problems/spiral-matrix/)
 
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