import shutil
import os
import cv2
import numpy as np
import glob

Fpath = input("Path to Folders: ")
Fname = input("File name: ")
Dfolder = input("New folder name: ")
Nname = input("New name: ")

def org_files():
    global path
    global destination_path
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
    pass

org_files()
print("org files done")

def make_video():
    print("make video started")
    output_file = "video.mp4"
    tiff_files = [f for f in os.listdir(path) if f.endswith('.tif')]
    tiff_files.sort()

    first_frame = cv2.imread(os.path.join(path, tiff_files[0]))
    height, width, layers = first_frame.shape
    fps = 2

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    print("one part done")
    for tiff_file in tiff_files:
        tiff_path = os.path.join(path, tiff_file)
        frame = cv2.imread(tiff_path)
        video_writer.write(frame)
    print("done successfully")

    video_writer.release()


print("starting")
make_video()

