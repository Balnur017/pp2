
numbers = [1, 2, 3, 4, 5]

#use map() and filter() for lists
squars = list(map(lambda x : x*x, numbers))

even = list(filter(lambda x: x % 2 == 0, numbers))

#Aggregate with reduce() (from functools)
from functools import reduce
result = reduce(lambda a, b: a + b, numbers)
print(result)

#Use enumerate() and zip() for paired iteration
names = ["Ali", "Madina", "Aruzhan"]
scores = [85, 90, 88]

for i , name in enumerate(names):
    print(i, name)
for name, score in zip(names, scores):
    print(name, score)

#Demonstrate type checking and conversions
x = "123"

print(type(x))

y = int(x)

print(type(y))
