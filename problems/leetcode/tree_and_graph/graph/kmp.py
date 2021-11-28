'''
Implement strStr().

Return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

Example 1:

Input: haystack = "hello", needle = "ll"
Output: 2
Example 2:

Input: haystack = "aaaaa", needle = "bba"
Output: -1
'''
class Solution:

    def indexOf(self, t, p):
        def getLongestProperPrefix(p):
            # arrarra -> [0, 0, 0, 1, 2, 3, 4]
            # amar ->    [0, 0, 1, 0]
            # aaoiaa ->  [0, 1, 0, 0, 1, 2]
            arr = [0]
            j = 0
            for i in range(1, len(p)):
                while j > 0 and p[j] != p[i]:
                    j = arr[j - 1]
                if p[j] == p[i]:
                    j += 1
                arr.append(j)
            print(arr)
            return arr

        def getMatches(t,p):
            kmp = getLongestProperPrefix(p)
            res = []
            j = 0
            for i in range(len(t)):
                while j > 0 and t[i] != p[j]:
                    j = kmp[j - 1]
                if t[i] == p[j]:
                    j += 1
                if j == len(p):
                    res.append(i - (j - 1))
                    j = kmp[j - 1]
            return res

        ans = getMatches(t,p)
        return ans if ans != [] else [-1]

    def strStr(self, string: str, pattern: str) -> int:
        return self.indexOf(string, pattern)[0] if pattern else 0
