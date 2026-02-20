#Example1
class A:
    def method_a(self):
        print("Method A")

class B:
    def method_b(self):
        print("Method B")

class C(A, B):
    pass

obj = C()
obj.method_a()
obj.method_b()

#example2
class Addition:
    def add(self, a, b):
        return a + b

class Multiplication:
    def multiply(self, a, b):
        return a * b

class Calculator(Addition, Multiplication):
    pass

calc = Calculator()
print(calc.add(3, 4))
print(calc.multiply(3, 4))

#Example3
class A:
    def show(self):
        print("Class A")

class B:
    def show(self):
        print("Class B")

class C(A, B):
    pass

obj = C()
obj.show()  # Class A

#Example4
class Base1:
    def greet(self):
        print("Hello from Base1")

class Base2:
    def greet(self):
        print("Hello from Base2")

class Child(Base1, Base2):
    def greet(self):
        super().greet()

c = Child()
c.greet()

#Example5
class Writer:
    def write(self):
        print("Writing code")

class Speaker:
    def speak(self):
        print("Speaking English")

class Programmer(Writer, Speaker):
    pass

p = Programmer()
p.write()
p.speak()