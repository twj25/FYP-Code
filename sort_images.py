import tkinter as tk
import os


def initilise_unsorted_files():
    unsorted_path = "C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Test/"
    unsorted_files = os.listdir(unsorted_path)
    unsorted_count = 0
    return

def class_moon():


    return 

def class_cloud_heavy():


    return



current_file = unsorted_path + unsorted_files[unsorted_count]

window = tk.Tk()

window.rowconfigure([0, 1], minsize=50, weight=1)
window.columnconfigure([0, 1, 2], minsize=50, weight=1)

frame1 = tk.Frame(master=window, width=100, height=100, bg="blue")
photo = tk.PhotoImage(file = current_file)
label = tk.Label(image = photo)
label.pack()

frame2 = tk.Frame(master=window, width=50, height=50, bg="yellow")
btn_moon = tk.Button(
    text="Moon Cover",
    width=25,
    height=5,
    bg="blue",
    fg="yellow",
    command=class_moon
)
button1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

frame3 = tk.Frame(master=window, width=50, height=50, bg="yellow")
button2 = tk.Button(
    text="Click me!",
    width=25,
    height=5,
    bg="yellow",
    fg="blue",
)
button2.pack(fill=tk.BOTH, side=tk.RIGHT, expand=True)


window.mainloop()