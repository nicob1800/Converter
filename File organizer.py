import shutil
import os

Fpath = input("Path to Folders: ")
Fname = input("File name: ")
Dfolder = input("New folder name: ")
Nname = input("New name: ")

letters = ['A', 'B', 'C', 'D']
numbers = ['01', '02', '03', '04']

path = os.path.join(Fpath, Dfolder)

source_path = f"{Fpath}\{Dfolder}\{Nname}"

print(source_path)
os.mkdir(path)
os.mkdir(source_path)

occurrences = 0
namenum = 3
typed = f"0{namenum}"


for root, dirs, files in os.walk(Fpath):
    if Fname in files:
        occurrences += 1
        

print(f"The file '{Fname}' was found {occurrences} times.")


