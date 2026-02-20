# A function is a block of code which only runs when it is called.
# A function can return data as a result.
# A function helps avoiding code repetition.

# In Python, a function is defined using the def keyword, followed by a function name and parentheses:
def my_function():
  print("Hello from a function") # This creates a function named my_function that prints "Hello from a function" when called.
my_function # To call a function, write its name
my_function
my_function # You can call the same function multiple times


# A function name must start with a letter or underscore
# A function name can only contain letters, numbers, and underscores
# Function names are case-sensitive (myFunction and myfunction are different)

# Valid names:
# calculate_sum()
# _private_function()
# myFunction2()


# Why use functions ?
# Imagine you need to convert temperatures from Fahrenheit to Celsius several times in your program. 
# Without functions, you would have to write the same calculation code repeatedly:
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)

# With functions, you write the code once and reuse it:
def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

# Functions can send data back to the code that called them using the return statement.
# When a function reaches a return statement, it stops executing and sends the result back:
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)

# Or you can use returned value directly
def get_greeting():
  return "Hello from a function"

print(get_greeting())

def my_function():
  pass  # Function definitions cannot be empty. 
# If you need to create a function placeholder without any code, use the pass statement