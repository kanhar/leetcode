{: .no_toc}
# Bloom Filters
Practise here: [Leetcode]()

- TOC
{:toc}


### [Find Missing Number](https://leetcode.com/problems/missing-number/discuss/1637159/python-solution-using-bloom-filters-cheeky-but-ultimately-a-good-learning-exercise) <BR>

> Despite the widespread use of Bloom filters in industry, I find it frustrating that no problem on leetcode requires them - so here i go - sub-optimally forcing the solution to fit the problem, this is the only one I could find where I can "test out" how the Bloom filter strategy would work - what kind of memory it would require, and get a feel for the variables, m, k and e where m is the number of bits in bit array, k is the number of hash functions and e is the false positive error rate.

<details><summary markdown="span">Execute!</summary>

```python
import hashlib
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        
        # Custom Hash - Just for practice. Not very good. 
        def hash1(val):   
            nonlocal MAX            
            primes = [ 3, 17, 23]
            curr = 0            
            for s in str(val):
                for p in primes:
                    curr += ord(s)**p      
                
            return curr % MAX
        
        def hash2(val):   
            nonlocal MAX            
            hashValue = hashlib.md5(str(val).encode())                  
            return int (hashValue.hexdigest(), 16) % MAX

        def hash3(val):   
            nonlocal MAX            
            hashValue = hashlib.sha3_384(str(val).encode())                  
            return int (hashValue.hexdigest(), 16) % MAX
        
        def hash4(val):   
            nonlocal MAX            
            hashValue = hashlib.sha512(str(val).encode())                  
            return int (hashValue.hexdigest(), 16) % MAX
        
        MAX = 10000
        hashList = [ hash1, hash2, hash3, hash4]
        bits = [[0] * MAX for x in range(len(hashList))]
    
        totalMemory = getsizeof(bits)+ getsizeof(bits[0]) +  getsizeof(bits[0][0])*MAX
        print ("Memory used for 2D Array Indexing: ", getsizeof(bits))
        print ("Memory used for (nested) 1D Array Indexing: ", getsizeof(bits[0]))
        print ("Memory used for (nested) integer in array: ", getsizeof(bits[0][0]))   
        print ("Memory used for (nested) integer in array (total): ", getsizeof(bits[0][0])*MAX )    
        print ("Total Memory (bytes)  for Bloom Filter: ", totalMemory )
        print ("Total Memory (kbytes)  for Bloom Filter: ", totalMemory / 1024 )
        
        for n in nums:    
            for h, func in enumerate(hashList):
                bits[h][func(n)] = 1
                
        for i in range(0, max(nums)+2):
            for h, func in enumerate(hashList):
                if bits[h][func(i)] == 0:
                    return i

        return -1
```

</details>
<BR>
