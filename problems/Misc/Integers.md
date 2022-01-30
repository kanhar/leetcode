{: .no_toc}
# Integers
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xf0762)

- TOC
{:toc}

### [Divide two integers](https://leetcode.com/problems/divide-two-integers/)

> Given two integers dividend and divisor, divide two integers without using multiplication,
division and mod operator.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def divide(self, a: int, b: int) -> int:

        # Answer of -2147483648/-1 should be 2147483648
        # However 2147483648 is too big, 2^31 == 2147483648 (one more than possible 2^31-1)
        # Therefore abs(2^31) == 2147483648-1 = 2147483647
        # This is an edge case scenario. The lowest value a 32 bit can contain is -2147483648
        if a == -2147483648 and b == -1:
            return 2147483647

        sign = (a < 0) == (b < 0)
        a, b = abs(a), abs(b)
        res = 0
        while a >= b:
            tmp = b
            val = 1
            while a >= b:
                a -= b
                res += val

                b = b << 1
                val = val << 1
            b = tmp

        return res if sign == 1 else 0 - res
```

</details>
<BR>

### [Integer add 1](https://leetcode.com/problems/plus-one/)

> Given a non-empty sort of digits representing a non-negative integer, plus one to the integer.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        res = []
        carry = 0

        for i in range(len(digits)-1,-1,-1):
            d = digits[i] + carry
            if i == len(digits)-1:
                d = d + 1

            if d > 9:
                carry = 1
                d = d - 10
            else:
                carry = 0

            res = [d] + res

        if carry==1:
            res = [carry] + res

        return (res)
```

</details>
<BR>

### [Integer Reverse](https://leetcode.com/problems/reverse-integer/)

> Given a 32-bit signed integer, reverse digits of an integer.

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def reverse(self, x: int) -> int:

        sign = -1 if x < 0 else 1

        num = abs(x)
        res = 0
        while num != 0:
            d = num %10
            res = res * 10 + d
            num = int(num /10 )

        if res > 2**31 - 1 or res < -2**31:
            return 0 #Cannot do this check earlier. Think why.

        return sign * res
```

</details>
<BR>

### [Implement Power(x,n)](https://leetcode.com/problems/powx-n/)

> Implement pow(x, n), which calculates x raised to the power n./ 

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def myPow(self, num, power):
        if not power:
            return 1
        elif power < 0:
            return 1 / self.myPow(num, -power)
        elif power % 2 == 1:
            return num * self.myPow(num, power-1)
        else:
            return self.myPow(num*num, power/2)
```

</details>
<BR>

### [Implement Sqrt(x)](https://leetcode.com/problems/sqrtx/)

> Implement int sqrt(int x).

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def mySqrt(self, x: int) -> int:
        l = 0
        r = x
        while l <= r:
            mid = (r + l) // 2
            square = mid * mid
            next_sq = (mid + 1) * (mid + 1)
            if square <= x < next_sq:
                return mid
            elif square > x:
                r = mid - 1
            else:
                l = mid + 1
        return square
```

</details>
<BR>


### [Integer-->Roman Numerals](https://leetcode.com/problems/integer-to-roman/)

> Integer to Roman numerals. 14 --> XIV

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def intToRoman(self, num: int) -> str:
        d ={'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 }
        d['IV'] = d['V']- d['I'] #4 
        d['IX'] = d['X']- d['I'] #9
        d['XL'] = d['L']- d['X'] #40
        d['XC'] = d['C']- d['X'] #90  
        d['CD'] = d['D']- d['C'] #400
        d['CM'] = d['M']- d['C'] #900    
        
        h = {v: k for k, v in d.items()}
        h = dict(sorted(h.items(), key=lambda item: item[0], reverse=True))
        
        #Flip above to:
        # {1000: 'M', 900: 'CM', 500: 'D', 400: 'CD', 100: 'C', 90: 'XC', 50: 'L', 40: 'XL', 10: 'X', 9: 'IX', 5: 'V', 4: 'IV', 1: 'I'}
        
        res = ""        
        for k,v in h.items():
            res += (num//k) * v
            num %= k
        
        return res
```

</details>
<BR>

### [Roman Numerals-->Integer](https://leetcode.com/problems/roman-to-integer/)

> Integer to Roman numerals. XIV --> 14

<details><summary markdown="span">Execute!</summary>

```python
class Solution:
    def romanToInt(self, word: str) -> int:
        
        d ={'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 }
        d['IV'] = d['V']- d['I'] #4 
        d['IX'] = d['X']- d['I'] #9
        d['XL'] = d['L']- d['X'] #40
        d['XC'] = d['C']- d['X'] #90  
        d['CD'] = d['D']- d['C'] #400
        d['CM'] = d['M']- d['C'] #900          
        
        total = 0
        for i in range(len(word)):
            if i != len(word)-1 and str(word[i]+word[i+1]) in d:
                total += d[str(word[i]+word[i+1])]
                i+=2
            else:
                total += d[str(word[i])]
                i+=1
        
        return total
```

</details>
<BR>
