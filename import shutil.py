import shutil
import os

Fpath = input("Path to Folders: ")
Fname = input("File name: ")
Dfolder = input("New folder name: ")
Nname = input("New name: ")

# Create the destination folder if it doesn't exist
path = os.path.join(Fpath, Dfolder)
os.makedirs(path, exist_ok=True)

# Find occurrences of the specified file name in directories
occurrences = 0
for root, dirs, files in os.walk(Fpath):
    if Fname in files:
        occurrences += 1
        i = occurrences
        source_path = os.path.join(root, Fname)
        destination_path = os.path.join(path, f"{Nname}_{i}.tif")
        
        try:
            shutil.copy(source_path, destination_path)
            print(f"File '{Fname}' copied to '{destination_path}'")
        except shutil.SameFileError:
            print("Same file error")
        except FileNotFoundError:
            print(f"File '{Fname}' not found in '{root}'")
        
# Print the total number of occurrences
print(f"The file '{Fname}' was found {occurrences} times.")
