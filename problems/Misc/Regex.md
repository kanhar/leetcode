{: .no_toc}
# Regex
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xftxlv)

- TOC
{:toc}

### [Implement Atoi](https://leetcode.com/problems/string-to-integer-atoi/)

> Implement atoi: Key idea is keep processing number until valid.

<details><summary markdown="span">Execute!</summary>

```python
import re
class Solution:
    def myAtoi(self, str):
        MAX_INT =  2**31 - 1
        MIN_INT = -2**31

        #^ --> Starting of String, followed by 0 or 1 (+-), followed by 0* zeroes followed by atleast one digit
        regex = re.search('^[-+]?\d+', str.strip())
        if regex:
            num = int(regex[0])
            if MIN_INT <= num <= MAX_INT:
                return num
            else:
                return MIN_INT if num < MIN_INT else MAX_INT
        else:
            return 0

```

</details>
<BR>

### [Decode-String](https://leetcode.com/problems/decode-string/)

> Given an encoded string, return its decoded string.
> [See also](https://kanhar.github.io/leetcode/problems/Arrays/Stacks.html#decode-string)

>> Alternatively, could we use this [technique](https://stackoverflow.com/questions/35329934/python-3-4-regular-expressions-for-matching-innermost-curly-brackets)?  
>> You could but interesting to note why not explicitly required in `(\d+)\[([a-zA-Z]+)\]`
<details><summary markdown="span">Execute!</summary>

```python
import re
class Solution:
    def decodeString(self,s):
        pattern = "(\d+)\[([a-zA-Z]+)\]"
        
        # Start with innermost parentheses
        # Ex: "3[a2[c]]"
        # (num, alpha) = (2,c)
        # s = 3[a + c*2 + ]
        # s = 3[acc]
        # s = accaccacc
        
        while True:
            match = re.search(pattern, s)
            if not match:
                break
            
            num, alpha = match.groups()

            print(num, alpha)
            start = match.start()
            end   = match.end()

            s     = s[:start] + alpha * int(num)  + s[end:]
        return s
```

</details>
<BR>


### [Parse valid IP.](https://leetcode.com/problems/validate-ip-address/)

> Parse valid IP, Ipv4 and IPv6.

<details><summary markdown="span">Execute!</summary>

```python
import re
class Solution:
    def validIPAddress(self, IP):
        def isIPv4(s):
            try: return str(int(s)) == s and 0 <= int(s) <= 255
            except: return False

        def isIPv6(s):
            regex = re.search("^[0-9a-fA-F]{1,4}$", s)
            if not regex:
                return False
            try: return int(regex[0], 16) in range( 0, int('FFFF', 16) )    #cool trick
            except: return False

        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return "IPv4"
        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return "IPv6"


        return "Neither"
```

</details>
<BR>

### [Catastrophic Backtracking](https://en.wikipedia.org/wiki/ReDoS)

> Let's see [what happens](https://www.rexegg.com/regex-explosive-quantifiers.html#example) when we try to match the string AAAC with that pattern ^(A+)*B.

> See also, a real world example via this [.NET Fiddle](https://dotnetfiddle.net/0PSP3l)

> Also instructive to understand how Regex works. Unrealistic to implement in an interview, it is
> nice to be able to see how a combinatorial explosion can result in this algorithm
> Ref: [Leetcode: regular-expression-matching](https://leetcode.com/problems/regular-expression-matching/)

<details><summary markdown="span">My regex Implementation in Python</summary>

```python
import functools

class Solution(object):
    @functools.lru_cache(maxsize=1024)
    def isMatch(self, t, p):
        if not p and not t:
            return True
        elif t and not p:
            return False
        elif p and not t and p[-1] != '*':
            return False
        else:
            firstCharMatches  = len(t)> 0 and p[0] in [t[0],'.']
            if len(p) > 1 and p[1] == '*':
                zeroOrMore = self.isMatch(t, p[2:])
                oneOrMore  = firstCharMatches and self.isMatch(t[1:], p) 
                return oneOrMore or zeroOrMore
            else:
                return firstCharMatches and self.isMatch(t[1:], p[1:])
```

</details>
<BR>