import shutil
import os
import cv2
import glob
import tkinter as tk
from tkinter import *
from tkinter import messagebox as mb    # importing the messagebox module from tkinter  
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
import time

def makewindow():
    global main
    main = tk.Tk()
    main.geometry("500x500")
    #main.mainloop()

def print_values():
    print(Fpath)
    print(Fname.get())
    print(Dfolder.get())
    print(Dname.get())

def organize():
    def update_global_variable(value):
        global selected_directory
        selected_directory = value

    def browse_folder(entry_var):
        global Fpath
        selected_folder = fd.askdirectory()
        entry_var.set(selected_folder)
        update_global_variable(selected_folder)
        Fpath = selected_folder
    
    global Fname
    global Dfolder
    global Dname
    Dfolder = tk.StringVar()
    Fname = tk.StringVar()
    Dname = tk.StringVar()
    Fpath = tk.StringVar()
    def orgframe():
        global folder_path
        global path
        global destination_path
        global suffix

        Fpath.set("")
        Dfolder.set("")
        Dname.set("")


        folder_path = Fpath.get()  # Get the value from the StringVar Fpath
        destination_folder = Dfolder.get()


        frame = tk.Frame(main, width=300, height=300, relief=tk.SUNKEN, bg='grey', borderwidth=10)
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        # Create label
        label = tk.Label(frame, text="Organize Files")
        label.place(relx=0.025, rely=0.05)

        folder_path = tk.StringVar()

        # Create Entries
        folder_entry = tk.Entry(frame, textvariable=folder_path)
        folder_entry.place(relx=0.025, rely=0.125, relwidth=0.5)

        # Create buttons
        folderpath = tk.Button(frame, text="Browse Folder", command=lambda: browse_folder(folder_path), fg='blue')
        folderpath.place(relx=0.025, rely=0.2)

        print_button = tk.Button(frame, text="Print Values", command=print_values)
        print_button.place(relx=0.025, rely=0.8)

        # File Name
        namelabel = tk.Label(frame, text="File Name with extension:")
        namelabel.place(relx=0.025, rely=0.275)
        name = tk.Entry(frame, textvariable=Fname)
        name.insert(0, Fname.get())  # Set the initial value using .insert()
        name.place(relx=0.025, rely=0.35, relwidth=0.5)
        Fname.set("")

        # Destination Folder 
        dlabel = tk.Label(frame, text="Destination Folder name:")
        dlabel.place(relx=0.025, rely=0.425)
        destin = tk.Entry(frame, textvariable=Dfolder)
        destin.insert(0, Dfolder.get())  # Set the initial value using .insert()
        destin.place(relx=0.025, rely=0.5, relwidth=0.5)
        Dfolder.set("")

        # Destination file
        dnamelabel = tk.Label(frame, text="Destination File name:")
        dnamelabel.place(relx=0.025, rely=0.575)
        dname = tk.Entry(frame, textvariable=Dname)
        dname.insert(0, Dname.get())  # Set the initial value using .insert()
        dname.place(relx=0.025, rely=0.65, relwidth=0.5)
        Dname.set("")


    orgframe()

Fpath = ""
Fname = ""
Dfolder = ""
Nname = ""

makewindow()
organize()

main.mainloop()
#Fpath = str(Fpath)
#Fname = str(Fname)
#Dfolder = str(Dfolder)
#Nname = str(Dname)
print(Fpath)
print(Fname.get())
print(Dfolder.get())
print(Dname.get())

Fpath = Fpath.replace("/", "\\")
Fname = Fname.get()
Dfolder = Dfolder.get()
Dname = Dname.get()



imageJ = input("Path to imageJ: ")
os.startfile(imageJ)

videoLocation = input("Path to video: ")
fps = float(input("Frames per second: "))


def org_files():
    global path
    global destination_path
    global suffix
    
    # Create the destination folder if it doesn't exist
    path = os.path.join(Fpath, Dfolder)
    #os.makedirs(path, exist_ok=True)

    # Find occurrences of the specified file name in directories
    occurrences = 0
    for root, dirs, files in os.walk(Fpath):
        if Fname in files:
            occurrences += 1
            i = occurrences
            parts = root.split("_")
            suffix = parts[-1]
            print(suffix)
            #lastdigits = root % 10
            source_path = os.path.join(root, Fname)
            if len(suffix) == 1:
                suffix = f"0{suffix}"
            print(suffix)

            destination_path = os.path.join(path, f"{Nname}_{suffix}.tif")
            print(destination_path)

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
    print("Files organized")

org_files()



os.chdir(videoLocation)

def make_video():
    global path
    videopath = input("Path to the video frames: ")
    name = input("Name of the video: ")
    img_array = []
    
    # Get the list of image files
    image_files = glob.glob(f"{videopath}/*.jpg")
    print(image_files)  # Print the list to debug
    
    if not image_files:
        print("No image files found matching the specified pattern.")
        return
    
    # Calculate the size based on the first image in the list
    first_image = cv2.imread(image_files[0])
    height, width, layers = first_image.shape
    size = (width, height)
    
    for filename in image_files:
        img = cv2.imread(filename)
        img_array.append(img)

    out = cv2.VideoWriter(f"{name}.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
 
    for i in range(len(img_array)):
        out.write(img_array[i])
    
    out.release()
    print(f"\033[1;31;40m{out}\033[m")






make_video()
print("Video created")
input("Press Enter to exit...")
