import shutil
import os

Fpath = input("Path to Folders: ")
Fname = input("File name: ")
Dfolder = input("New folder name: ")
Nname = input("New name: ")

letters = ['A', 'B', 'C', 'D']
numbers = ['01', '02', '03', '04']
path = os.path.join(Fpath, Dfolder)

try:
    os.rmdir(path)
except:
    pass

#END OF COPY METHOD


#print(source_path)
os.mkdir(path)

print(path)


#copy_source = 


occurrences = 0
namenum = 3
typed = f"0{namenum}"


for root, dirs, files in os.walk(Fpath):
    if Fname in files:
        occurrences += 1

i = occurrences

if i >= 0:

    source_path = f"{Fpath}\Timepoint_{i}\{Fname}"
    destination_path = f"{Fpath}\{Dfolder}"

    try:
        shutil.copy(source_path, destination_path)
        os.rename(Fname, f"{Nname}{i}")

    except shutil.SameFileError:
        print("Same file error")
    
    i -= 1
        

print(f"The file '{Fname}' was found {occurrences} times.")


