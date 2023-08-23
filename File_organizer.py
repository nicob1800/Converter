import shutil
import os
import cv2
import numpy as np
import glob
from PIL import Image

Fpath = input("Path to Folders: ")
Fname = input("File name: ")
Dfolder = input("New folder name: ")
Nname = input("New name: ")

def org_files():
    global path
    global destination_path
    global suffix
    
    # Create the destination folder if it doesn't exist
    path = os.path.join(Fpath, Dfolder)
    os.makedirs(path, exist_ok=True)

    # Find occurrences of the specified file name in directories
    occurrences = 0
    for root, dirs, files in os.walk(Fpath):
        if Fname in files:
            occurrences += 1
            i = occurrences
            parts = root.split("_")
            suffix = parts[-1]
            #lastdigits = root % 10
            source_path = os.path.join(root, Fname)
            destination_path = os.path.join(path, f"{Nname}_{suffix}.tif")
            
            try:
                shutil.copy(source_path, destination_path)
                print(f"From {root}, file '{Fname}' copied to '{destination_path}'")
            except shutil.SameFileError:
                print("Same file error")
            except FileNotFoundError:
                print(f"File '{Fname}' not found in '{root}'")
            
    # Print the total number of occurrences
    print(f"The file '{Fname}' was found {occurrences} times.")
    print(f"\033[1;31;40m{path}\033[m")


def make_video():
    global path
    videopath = input("Path to the video frames: ") #comment out later
    name = input("Name of the video: ")
    img_array = []
    for filename in glob.glob(f"{path}/*.tif"):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)

    out = cv2.VideoWriter(f"{name}.mp4",cv2.VideoWriter_fourcc(*'mp4v'), 2, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    
    out.release()
    print(f"\033[1;31;40m{out}\033[m")

org_files()
print("Files organized")

make_video()
