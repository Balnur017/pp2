
#create nected directories
import os
os.makedirs("data/students/info")

#list files and folders
files = os.listdir()

print(files)

#find files by extension
for file in os.listdir():
    if file.endswith(".txt"):
        print(file)

#move copy files between directories
import shutil
shutil.move("students.txt", "data/students/students.txt")
