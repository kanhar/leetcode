'''
Minimizing Permutations
In this problem, you are given an integer N, and a permutation, P of the integers from 1 to N, denoted as (a_1, a_2, ..., a_N).
You want to rearrange the elements of the permutation into increasing order, repeatedly making the following operation:

If N = 3, and P = (3, 1, 2), we can do the following operations:
Select (1, 2) and reverse it: P = (3, 2, 1).
Select (3, 2, 1) and reverse it: P = (1, 2, 3).
output = 2

'''
def reverse(arr, i, j):
    arr = list(arr)
    while i < j:
        arr[i], arr[j] = arr[j], arr[i]
        i+=1
        j-=1
    return ''.join(arr)

def minOperations(arr):
    def solve(source, dest):
        visited = set()
        q = [ ( source, 0) ]
        res = []
        while q:
            curr, count = q.pop(0)
            if curr not in visited:
                visited.add(curr)
                if curr == dest:
                    res.append(count)
                else:
                    for i in range(1, len(curr)):
                        for j in range(0,i+1):
                            q.append(  (reverse(curr,j,i ), count + 1)  )

        return min(res) if res != [] else 0

    arr = [str(x) for x in arr]
    return solve( ''.join(arr), ''.join( sorted(arr) ) )

print(minOperations([3,1,2]) == 2)
print(minOperations([1,2,5,4,3]) == 1)








