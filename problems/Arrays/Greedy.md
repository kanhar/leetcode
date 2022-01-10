{: .no_toc}
# Greedy Algorithms

- TOC
{:toc}

### [Integer-->Roman Numerals](https://leetcode.com/problems/integer-to-roman/)

> Integer to Roman numerals. 14 --> XIV

<details><summary markdown="span">Let's see some code!</summary>

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

<details><summary markdown="span">Let's see some code!</summary>

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
