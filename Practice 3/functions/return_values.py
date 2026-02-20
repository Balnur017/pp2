#Example1
def square(n):
    return n ** 2

result = square(6)
print(result)

#Example2
def greet(name):
    return f"Hello, {name}"

message = greet("Serik")
print(message)

#Example3
def calculate(a, b):
    return a + b, a * b

sum_value, product = calculate(4, 5)
print(sum_value)
print(product)

#Example4
def get_numbers():
    return [1, 2, 3, 4, 5]

numbers = get_numbers()
print(numbers)

#Example5
def check_even(number):
    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"

print(check_even(7))

