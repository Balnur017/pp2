
#creating file.txt and write something
file = open("students.txt", "w")

file.write("Name: Izatulla Balnur\n")
file.write("Age: 17\n")
file.write("City: Almaty\n")

file.close()

#read and print file contents
file = open("students.txt", "r")

content = file.read()
print(content)

file.close()

#append new lines and verify content
file = open("students.txt", "a")

file.write("University: KBTU\n")
file.write("Major: Computer Science\n")

file.close()

file = open("students.txt", "r")
print(file.read())
file.close()

#Copy and back up files using shutil
import shutil

shutil.copy("students.txt", "students_backup.txt")

#delete files safely
import os

if os.path.exists("students_backup.txt"):
    os.remove("students_backup.txt")
    print("file deleted")
else:
    print("file not found")
