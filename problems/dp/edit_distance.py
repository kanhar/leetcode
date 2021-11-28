"""
Given two strings word1 and word2, return the minimum number of operations required to convert word1 to word2.

You have the following three operations permitted on a word:

Insert a character
Delete a character
Replace a character


Example 1:

Input: word1 = "horse", word2 = "ros"
Output: 3
Explanation:
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')

Ref: https://leetcode.com/problems/edit-distance/
"""

#edit distance
#Levenshtein distance. lookup
from typing import List

def printMatrix(m):
    res = ""
    for i in range(len(m)):
        for j in range(len(m[i])):
            res=res+str(m[i][j])+ " "
        res = res+"\n"
    print(res)

h = {}
def del_r(s1, s2, c=0):
    if s1==s2:
        return c
        
    if( len(s1) == 0 and len(s2) != 0):
        return len(s2)+c
    
    if( len(s1) != 0 and len(s2) == 0):
        return len(s1)+c
        
    if s1[0]==s2[0]:    
        args = str([ s1[1:], s2[1:] ])
        if args in h:
            return h[args]
        else:
            h[args] = del_r( s1[1:], s2[1:], c)
            return h[args]      
    else:           
        left = del_r( s1[0:], s2[1:],c+1)   #del from s2
        rigt = del_r( s1[1:], s2[0:],c+1)   #del from s1
        #adding diag here, makes this also edit compatible.
        #diag = del_r( s1[1:], s2[1:],c+1)   #del from both ( or swap one with another, cost = 1 )  
        return min( left, rigt )

def del_d(s1,s2):    
    r = len(s1) + 1 # Add 1 to represent 0th column for DP
    c = len(s2) + 1   
    m = [[0 for _ in range(c)] for _ in range(r)]
                       
    for i in range(0,r):
        for j in range(0,c):
            top  = m[i][j-1]    # delete from top ( ==s1 )
            left = m[i-1][j]    # delete from left ( == s2 )
            diag = m[i-1][j-1]  # edit
                       
            if i == 0:
                m[0][j]=j
            elif j == 0:
                m[i][0]=i                     
            elif s1[i-1] == s2[j-1]:        #why i-1? cause of i offset in r,c             
                m[i][j]=diag                
            else:
                m[i][j]=1+min(left, top)    #adding diag here, makes this also edit compatible. 
    
    return m[r-1][c-1]



print('recursive')
print(del_r( "heat", "hit"))
print(del_r( "dog", "frog"))
print(del_r( "some", "thing"))
print(del_r( "abc", "cab"))

print('dynamic')
print(del_d( "heat", "hit"))
print(del_d( "dog", "frog"))
print(del_d( "some", "thing"))
print(del_d( "abc", "cab"))

print('LCS')
print(lcs( "heat", "hit"))
print(lcs( "dog", "frog"))
print(lcs( "some", "thing"))
print(lcs( "ab", "ba"))
