'''
Parse valid IP.

Example 1:
Input: "172.16.254.1"

Output: "IPv4"

Explanation: This is a valid IPv4 address, return "IPv4".
Example 2:
Input: "2001:0db8:85a3:0:0:8A2E:0370:7334"

Output: "IPv6"

Explanation: This is a valid IPv6 address, return "IPv6".

Ref: https://leetcode.com/problems/validate-ip-address/
'''

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