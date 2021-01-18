'''
Ex: "1:ABC" --> BCD
'''

def move(ch, d):
    if ch.islower():
        d = d % 26
        start, end = ord('a'),  ord('z')
    elif ch.isupper():
        d = d % 26
        start, end = ord('A'),  ord('Z')
    elif ch.isdigit():
        d = d % 10
        start, end = ord('0'),  ord('9')
    else:
        return ch

    num = ord(ch) + d
    diff = num - end
    if diff <= 0:
        return chr(num)
    else:
        return chr(diff + start-1)

def solve(input):
    arr = input.split(':')
    if len(arr) != 2:
        return
    else:
        d = int(arr[0])
        s = arr[1]

        res = []
        for ch in s:
            res += move(ch, d)

        return ''.join(res)

print(solve("1:abczsr"))
print(solve("27:ABCZ"))
print(solve("1:ABCZ09"))