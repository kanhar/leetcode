{: .no_toc}
# Integers
Practise here: [Leetcode](https://leetcode.com/list?selectedList=90xf0762)

- TOC
{:toc}

### Divide two integers

> Given two integers dividend and divisor, divide two integers without using multiplication,
division and mod operator.
> [Leetcode](https://leetcode.com/problems/divide-two-integers/)

<details><summary markdown="span">Let's see some code!</summary>

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

### Integer add 1

> Given a non-empty sort of digits representing a non-negative integer, plus one to the integer.
> [Leetcode](https://leetcode.com/problems/plus-one/)

<details><summary markdown="span">Let's see some code!</summary>

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

### Integer Reverse

> Given a 32-bit signed integer, reverse digits of an integer.
> [Leetcode](https://leetcode.com/problems/reverse-integer/)

<details><summary markdown="span">Let's see some code!</summary>

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

### Power

> Implement pow(x, n), which calculates x raised to the power n./ 
> [Leetcode](https://leetcode.com/problems/powx-n/)

<details><summary markdown="span">Let's see some code!</summary>

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

### Sqrt

> Implement int sqrt(int x).
> [Leetcode](https://leetcode.com/problems/sqrtx/)

<details><summary markdown="span">Let's see some code!</summary>

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