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
    main.geometry("500x1000")
    #main.mainloop()

def organize():
    def browse_folder(entry_var):
        selected_folder = fd.askdirectory()
        entry_var.set(selected_folder)
    
    def org_files():
        folder_path = Fpath.get()
        file_name = Fname.get()
        dest_folder_name = Dfolder.get()
        dest_file_name = Dname.get()

        path = os.path.join(folder_path, dest_folder_name)
        os.makedirs(path, exist_ok=True)

        occurrences = 0
        for root, dirs, files in os.walk(folder_path):
            if file_name in files:
                occurrences += 1
                parts = root.split("_")
                suffix = parts[-1]
                source_path = os.path.join(root, file_name)
                if len(suffix) == 1:
                    suffix = f"0{suffix}"
                destination_path = os.path.join(path, f"{dest_file_name}_{suffix}.tif")

                try:
                    shutil.copy(source_path, destination_path)
                    print(f"From {root}, file '{file_name}' copied to '{destination_path}'")
                except shutil.SameFileError:
                    print("Same file error")
                except FileNotFoundError:
                    print(f"File '{file_name}' not found in '{root}'")

        print(f"The file '{file_name}' was found {occurrences} times.")
        print(f"\033[1;31;40m{path}\033[m")
        print("Files organized")

    global Fpath
    global Fname
    global Dfolder
    global Dname
    
    Fpath = tk.StringVar()
    Fname = tk.StringVar()
    Dfolder = tk.StringVar()
    Dname = tk.StringVar()

    main_frame = tk.Frame(main, width=300, height=300, relief=tk.SUNKEN, bg='grey', borderwidth=10)
    main_frame.place(relx=0, rely=0.04, relwidth=0.6, relheight=0.35)
    
    tk.Label(main, text="Organize Files", relief=tk.SUNKEN, bg="grey", borderwidth=5).place(relx=0.025, rely=0.0)
    tk.Label(main_frame, text="Select folder with folders").place(relx=0.025, rely=0.025)
    
    folder_path_entry = tk.Entry(main_frame, textvariable=Fpath)
    folder_path_entry.place(relx=0.025, rely=0.125, relwidth=0.5)
    tk.Button(main_frame, text="Browse Folder", command=lambda: browse_folder(Fpath), fg='blue').place(relx=0.025, rely=0.225)
    
    tk.Label(main_frame, text="File Name with extension:").place(relx=0.025, rely=0.35)
    file_name_entry = tk.Entry(main_frame, textvariable=Fname)
    file_name_entry.place(relx=0.025, rely=0.45, relwidth=0.5)
    
    def createdir():
        os.makedirs(f"{Fpath.get()}/{Dfolder.get()}", exist_ok=True)
        ss = Message(main_frame, text=f"Folder successfully created at {Fpath.get()}/{Dfolder.get()}")
        ss.place(relx=0.6, rely=0.75)
        main_frame.after(3000, ss.destroy)

    tk.Label(main_frame, text="Destination Folder name:").place(relx=0.025, rely=0.55)
    dest_folder_entry = tk.Entry(main_frame, textvariable=Dfolder)
    dest_folder_entry.place(relx=0.025, rely=0.65, relwidth=0.5)
    tk.Button(main_frame, text="Create Folder", command=lambda: createdir()).place(relx=0.6, rely=0.65, relwidth=0.3)


    tk.Label(main_frame, text="Destination File name:").place(relx=0.025, rely=0.75)
    dest_file_entry = tk.Entry(main_frame, textvariable=Dname)
    dest_file_entry.place(relx=0.025, rely=0.85, relwidth=0.5)
    
    tk.Button(main_frame, text="Organize Files", command=org_files).place(relx=0.6, rely=0.85, relwidth=0.3)

def openij():
    #frame
    frame = tk.Frame(main, width=300, height=300, relief=tk.SUNKEN, bg='grey', borderwidth=10)
    frame.place(relx=0, rely=0.4, relwidth=0.6, relheight=0.15)
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
    

def video_maker():
    def make_video(name, fps, videopath):
        global path
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
    global videopath
    global name
    global fps
    fps = tk.StringVar()
    name = tk.StringVar()
    videopath = tk.StringVar()

    main_frame = tk.Frame(main, width=300, height=300, relief=tk.SUNKEN, bg='grey', borderwidth=10)
    main_frame.place(relx=0, rely=0.56, relwidth=0.6, relheight=0.15)

    fps_var = tk.StringVar()
    name_var = tk.StringVar()
    videopath_var = tk.StringVar()

    fps_input = tk.Entry(main_frame, textvariable=fps_var)
    fps_input.place(relx=0.025, rely=0.025)

    def browse_folder(entry_var):
        selected_folder = fd.askdirectory()
        entry_var.set(selected_folder)

    videopath_entry = tk.Entry(main_frame, textvariable=videopath_var, width=10)
    videopath_entry.place(relx=0.025, rely=0.25, relwidth=0.5)
    tk.Entry(main_frame, textvariable=name_var, width=10).place(relx=0.025, rely=0.5, relwidth=0.4)
    
    def create():
        video_name = name_var.get()
        fps_value = float(fps_var.get())
        videopath = videopath_var.get()
        os.chdir(videopath)
        make_video(video_name, fps_value, videopath)
    
    framesinpath_button = tk.Button(main_frame, text="Set Frames", command=lambda: browse_folder(videopath_var))
    framesinpath_button.place(relx=0.6, rely=0.25, relwidth=0.3)
    
    tk.Button(main_frame, text="Make Video", command=create).place(relx=0.025, rely=0.7, relwidth=0.3)


Fpath = ""
Fname = ""
Dfolder = ""
Nname = ""
ijentry = ""

makewindow()
organize()
openij()
video_maker()
main.mainloop()
print(fps)
print(name)
print(videopath)



print("Video created")
input("Press Enter to exit...")

