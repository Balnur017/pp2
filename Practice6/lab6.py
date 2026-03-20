
'''
#1
n = int(input())
a = list(map(int, input().split()))

sum = 0
for i in a:
    sum += i**2

print(sum)

#2
n = int(input())
a = list(map(int, input().split()))

def count_even(x):
    if x % 2 == 0:
        return True
    else:
        return False
        

ev = filter(count_even, a)
c = 0
for x in ev:
    c+=1 
print(c)

#3
n = int(input())
l = list(input().split())

y = enumerate(l)
y = list(y)
first = True
for i in y:
    if not first:
        print(" ", end = "")
    first = False
    print(f"{i[0]}:{i[1]}", end = " ")

#4
n = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))

x = zip(A, B)
x = tuple(x)
sum = 0
for i in x:
    sum += i[0]*i[1]

print(sum)

#5
s = input()
l = []
for i in s:
    if i == "a" or i == "e" or i == "o" or i == "u" or i == "i" or i == "A" or i == "E" or i == "O" or i == "U" or i == "I":
        l.append(i)

if any(l):
    print("Yes")
else:
    print("No")

#6
n = int(input())
l = list(map(int, input().split()))

if all((x >= 0 for x in l)):
    print("Yes")
else:
    print("No")

#7
n = int(input())
lis = input().split()

print(max(lis, key = len))

#8
n = int(input())
l = set(map(int, input().split()))

print(*sorted(l))

#9
n = int(input())
K = list(input().split())
V = list(input().split())
q = input()

s = zip(K, V)
s = dict(s)
if q in s:
    print(s[q])
else:
    print("Not found")
'''
#10        
n = int(input())
l = list(map(int, input().split()))

print(sum(map(bool, l)))
