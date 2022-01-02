{: .no_toc}
# Regex
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xftxlv)

- TOC
{:toc}

### Atoi

> Implement atoi: Key idea is keep processing number until valid.
> [Leetcode](https://leetcode.com/problems/string-to-integer-atoi/)

<details><summary markdown="span">Let's see some code!</summary>

```python
import re
class Solution:
    def myAtoi(self, str):
        MAX_INT =  2**31 - 1
        MIN_INT = -2**31

        #^ --> Starting of String, followed by 0 or 1 (+-), followed by 0* zeroes followed by atleast one digit
        regex = re.search('^[-+]?0*\d+', str.strip())
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

### Decode-String

> Given an encoded string, return its decoded string.
> [Leetcode](https://leetcode.com/problems/decode-string/)

<details><summary markdown="span">Let's see some code!</summary>

```python
import re
class Solution:
    def decodeString(self,s):
        pattern = "(\d+)\[([a-zA-Z]+)\]"

        while True:
            match = re.search(pattern, s)
            if not match:
                break

            num, alpha = match.groups()
            start = match.start()
            end   = match.end()

            s     = s[:start] + alpha * int(num)  + s[end:]
        return s
```

</details>
<BR>


### Parse valid IP.

> Parse valid IP, Ipv4 and IPv6.
> [Leetcode](https://leetcode.com/problems/validate-ip-address/)

<details><summary markdown="span">Let's see some code!</summary>

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
