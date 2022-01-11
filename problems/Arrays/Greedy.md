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

### [Get Random](https://leetcode.com/problems/insert-delete-getrandom-o1/)

> Not really a greedy algorithm, but placing here until I can figure out where to place this
> category of algorithms.

<details><summary markdown="span">Let's see some code!</summary>

```python
class RandomizedSet:
    def __init__(self):
        self.h = collections.defaultdict(int)
        self.arr= []
        
    def insert(self, val: int) -> bool:
        if val not in self.h:
            self.arr.append(val)
            self.h[val] = len(self.arr)-1
            return True
        else:
            return False

    def remove(self, val: int) -> bool:
        if val in self.h:            
            # Get ready to delete element from Array and hash
            idx =  self.h[val]
            idxLast = len(self.arr)-1
            del self.h[val]
            
            if idx==idxLast:
                self.arr.pop()
                return True
            
            # Put item to delete at end of array.
            self.arr[idx], self.arr[idxLast] = self.arr[idxLast], self.arr[idx]
            self.arr.pop()
            self.h[self.arr[idx]] = idx
            return True
        else:
            return False

    def getRandom(self) -> int:
        if len(self.arr):
            r = int(random.random() * len(self.arr))
            return self.arr[r]

# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()
```

</details>
<BR>


### [Capacity To Ship Packages Within D Days](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/)

> TBD: Solve when free.