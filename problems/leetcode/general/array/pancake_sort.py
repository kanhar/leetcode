'''
Given an array A, we can perform a pancake flip: We choose some positive integer k <= A.length, then reverse the order of the first k elements of A.
We want to perform zero or more pancake flips (doing them one after another in succession) to sort the array A.

Return the k-values corresponding to a sequence of pancake flips that sort A.  Any valid answer that sorts the array within 10 * A.length flips will be judged as correct.

Example 1:

Input: [3,2,4,1]
Output: [4,2,4,3]
Explanation:
We perform 4 pancake flips, with k values 4, 2, 4, and 3.
Starting state: A = [3, 2, 4, 1]
After 1st flip (k=4): A = [1, 4, 2, 3]
After 2nd flip (k=2): A = [4, 1, 2, 3]
After 3rd flip (k=4): A = [3, 2, 1, 4]
After 4th flip (k=3): A = [1, 2, 3, 4], which is sorted.

Ref: https://leetcode.com/problems/pancake-sorting/
'''

def flip(arr, k):
    i=0
    while(i < k):
        tmp = arr[i]
        arr[i] = arr[k]
        arr[k] = tmp
        i = i + 1
        k = k -1
    return arr

def find_max_index(arr,k):
    max_v = arr[0]
    max_i = 0
    for i in range(0,k+1):
        if arr[i] > max_v:
            max_v = arr[i]
            max_i = i
    
    return max_i

def pancake_sort(arr):    
    i = len(arr)-1  
    while(i > 0):        
        k = find_max_index(arr, i)    
        arr = flip(arr, k)        
        arr[0],arr[i] = arr[i],arr[0] #apparently this should not be a swap, but a flip 
        i = i-1    
    return arr

print(pancake_sort([4,1,5,6,7,0,2,3]))