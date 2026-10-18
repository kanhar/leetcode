#https://medium.com/@Pinterest_Engineering/sharding-pinterest-how-we-scaled-our-mysql-fleet-3f341e96ca6f
def p(n):
    return format(n, '#064b')

shrd = (3429,16)    #16 == 0xFFFF
typ  = (1,10)       #10 == 0x3FF
row  = (7075733,36) #36 == 32+4 = 0xFFFF FFFF F

bitcount = shrd[1] + typ[1]+row[1]

shrd_b = shrd[0] << (bitcount - shrd[1]) #46
typ_b  = typ[0]  << (bitcount - shrd[1] - typ[1]) #36
row_b  = row[0]  << 0

nums = [shrd_b, typ_b, row_b]
res  = sum(nums)
print(*([p(x) for x in nums]),sep = "\n")
print(res)

print(res >> 46 & 0xFFFF)       #2**16-1
print(res >> 36 & 0x3FF)        #2**10-1
print(res >> 0  & 0xFFFFFFFFF)  #2**36-1

#System Design. Tiny Url
# 7 Characters URL
# 62 range (a-zA-Z0-9)
# 62^7 = 3.5e12 (trillion)
# 2^(x-1) > 3.5e12: x = 43
# So we need 43 bits
# Take md5 hash of a long url (128 bits ). Take arbitrarily first 43 bits (y)
# y base 62. Should give you 7 characters in range (0-61). Map those to a-zA-Z0-9



