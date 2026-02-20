class Student:
    # Class variable (shared by all objects)
    school_name = "SDU University"
    student_count = 0

    def __init__(self, name, age):
        # Instance variables (unique for each object)
        self.name = name
        self.age = age

        # Increase class variable when new object is created
        Student.student_count += 1

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Age: {self.age}")
        print(f"School: {Student.school_name}")
        print("-------------------")


# Creating objects
s1 = Student("Yelzhas", 17)
s2 = Student("Aruzhan", 18)

# Access instance method
s1.display_info()
s2.display_info()

# Access class variable
print("Total students:", Student.student_count)