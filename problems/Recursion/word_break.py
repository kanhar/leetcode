"""

Ref: https://leetcode.com/problems/word-break/
"""

def getall(s, d):
    res = []
    for i in range(1, len(s) + 1):
        if s[:i] in d:
            res += [s[:i]] + getall(s[i:], d)
    return res


d = ["bed", "bat", "bath", "and", "hand", "beyond"]
s = "bedbathandbeyond";
print(getall(s, d) == ['bed', 'bat', 'hand', 'beyond', 'bath', 'and', 'beyond'])