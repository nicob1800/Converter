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


def org_files():
    global path
    global destination_path
    global suffix
    global Dname

    Fpath = Fpath.get()
    Dfolder = Dfolder.get()
    Fname = Fname.get()
    Nname = Dname.get()
    
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

def makewindow():
    global main
    main = tk.Tk()
    main.geometry("500x1000")
    #main.mainloop()

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
        frame = tk.Frame(main, width=300, height=300, relief=tk.SUNKEN, bg='grey', borderwidth=10)
        frame.place(relx=0, rely=0.04, relwidth=0.6, relheight=0.35)
        # Create label
        label = tk.Label(main, text="Organize Files", relief=tk.SUNKEN, bg="grey", borderwidth=5)
        label.place(relx=0.025, rely=0.0)

        labelf = tk.Label(frame, text="Select folder with folders")
        labelf.place(relx=0.025, rely=0.025)

        folder_path = tk.StringVar()

        # Create Entries
        folder_entry = tk.Entry(frame, textvariable=folder_path)
        folder_entry.place(relx=0.025, rely=0.125, relwidth=0.5)

        # Create buttons
        folderpath = tk.Button(frame, text="Browse Folder", command=lambda: browse_folder(folder_path), fg='blue')
        folderpath.place(relx=0.025, rely=0.225)

        # File Name
        namelabel = tk.Label(frame, text="File Name with extension:")
        namelabel.place(relx=0.025, rely=0.35)
        name = tk.Entry(frame, textvariable=Fname)
        name.insert(0, Fname.get())  # Set the initial value using .insert()
        name.place(relx=0.025, rely=0.45, relwidth=0.5)
        Fname.set("")

        # Destination Folder 
        dlabel = tk.Label(frame, text="Destination Folder name:")
        dlabel.place(relx=0.025, rely=0.55)
        destin = tk.Entry(frame, textvariable=Dfolder)
        destin.insert(0, Dfolder.get())  # Set the initial value using .insert()
        destin.place(relx=0.025, rely=0.65, relwidth=0.5)
        Dfolder.set("")

        # Destination file
        dnamelabel = tk.Label(frame, text="Destination File name:")
        dnamelabel.place(relx=0.025, rely=0.75)
        dname = tk.Entry(frame, textvariable=Dname)
        dname.insert(0, Dname.get())  # Set the initial value using .insert()
        dname.place(relx=0.025, rely=0.85, relwidth=0.5)
        Dname.set("")

        # Create Organize button
        organizer = tk.Button(frame, text="Organize Files", command=lambda: org_files)
        organizer.place(relx=0.6, rely=0.85, relwidth=0.3)


    orgframe()

def openij():
    #frame
    frame = tk.Frame(main, width=300, height=300, relief=tk.SUNKEN, bg='grey', borderwidth=10)
    frame.place(relx=0, rely=0.375, relwidth=0.6, relheight=0.15)
    ijlabel = tk.Label(frame, text="Open ImageJ", relief=tk.SUNKEN, bg="grey", borderwidth=5)
    ijlabel.place(relx=0.025, rely=0.025)

    def update_ijentry(value):
        global ijentry
        ijentry = value

    def browse_ij(entryvar):
        ijpath = fd.askopenfilename()
        entryvar.set(ijpath)
        update_ijentry(ijpath)

    imagej = tk.StringVar()
    ijentry = tk.Entry(frame, textvariable=imagej)
    ijentry.place(relx=0.025, rely=0.25)
    ijbrowse = tk.Button(frame, text="Browse ImageJ", command=lambda: browse_ij(imagej))
    ijbrowse.place(relx=0.025, rely=0.5)
    ijopen = tk.Button(frame, text="Open ImageJ", command=lambda: os.startfile(imagej.get()))
    ijopen.place(relx=0.6, rely=0.25, relwidth=0.3)

Fpath = ""
Fname = ""
Dfolder = ""
Nname = ""
ijentry = ""

makewindow()
organize()
openij()
main.mainloop()
print(Fpath)
print(Fname.get())
print(Dfolder.get())
print(Dname.get())

Fpath = Fpath.replace("/", "\\")
Fname = Fname.get()
Dfolder = Dfolder.get()
Dname = Dname.get()

videoLocation = input("Path to video: ")
fps = float(input("Frames per second: "))

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

