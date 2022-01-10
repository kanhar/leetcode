Time Complexity: O(n) where n is the largest array
Space Complexity: O(n) where N is the size of the largest array
def test(arr1, arr2, arr3 ):
    h = collections.defaultdict(int)
    for a in arr1:
        h[a]+=1
    for b in arr2:
        h[b]+=1
    for c in arr3:
        h[c]+=1
    
    return [x for x in h if h[x]==3 ]

A,B,C
Intersect(Intersect(A,B), C)


1,4,3,7
2,4,8,9
4,5,6,7

1,2,4

def intersect(arr1, arr2, arr3 ):
    h = collections.defaultdict(int)
    a = 0   
    b = 0
    c = 0
    res = []
    while a<len(arr1) and b<len(arr2) and c < len(arr3):
        if arr1[a]==arr2[b]==arr3[c]:
            res.append(arr1[a])
            a+=1
            b+=1
            c+=1
        else:
            if a < b:
                if a < c:
                    a is the smallest number
                else
                    c is the smallest number
            else:
                if b < c:
                    b is the smallest number
                else:       
                    c is the smallest number
            2 -- > 2
            3 -- > 6
    return res

def solve(arr1, arr2, arr3 ):
    return intersect(intersect(arr1,arr2), arr3)

