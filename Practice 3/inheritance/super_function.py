class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()


# Python also has a super() function that will make the child class inherit all the methods and properties from its parent:
class Student(Person):
  def __init__(self, fname, lname):
    super().__init__(fname, lname)

# By using the super() function, you do not have to use the name of the parent element,
# it will automatically inherit the methods and properties from its parent.