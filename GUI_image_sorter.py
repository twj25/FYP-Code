import tkinter as tk
from PIL import Image, ImageTk
import shutil
import os
import sys
import easygui

def slct_speckle():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")[-1]
    new_dir = base_path + "Sorted/Speckle/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_moon():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = base_path + "Sorted/Moon/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return 

def slct_moon_exp():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = base_path + "Sorted/Moon_Exposure/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_cloud_heavy():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = base_path + "Sorted/V_Cloudy/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_cloud():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = base_path + "Sorted/Cloudy/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_alm_clear():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = base_path + "Sorted/Almost_Clear/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_clear():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = base_path + "Sorted/Clear/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_other():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")[-1]
    new_dir = base_path + "Sorted/Other/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def update_image():
    global current_image
    current_image += 5
    try:
        photo2 = ImageTk.PhotoImage(Image.open(images[current_image]))
    except:
        easygui.msgbox("You've labelled enough data! Please close the GUI to continue", title="simple gui")
        return
    img.config(image = photo2) 
    img.photo_ref = photo2
    return

def run_GUI(source):
    Location = source[0]
    Frequency = source[1]
    Year = source[2]
    Month = source[3]
  
    # Create the PIL image object
    global base_path
    #base_path = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/"
    base_path = "C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Final System Data/{}/{}/{}/{}/".format(Location,Frequency,Year,Month)
    unsorted_path = base_path + 'Unsorted/'
    unsorted_files = os.listdir(unsorted_path)

    classes = ["Moon", "Moon_Exposure", "Cloudy", "V_Cloudy", "Almost_Clear", "Clear", "Speckle", "Other"]
    for clas in classes:
        dir = base_path + "Sorted/" + clas
        if not os.path.isdir(dir):
            os.makedirs(dir)

    global images
    images = []
    for image in unsorted_files:
        cur_dir = unsorted_path + image
        #images.append(tk.PhotoImage(file=cur_dir))
        images.append(cur_dir)

    global current_image
    current_image = 0
    photo = ImageTk.PhotoImage(Image.open(images[current_image]))
    global img
    img = tk.Label(root,image = photo)
    img.grid(columnspan=8, row=0, column= 0)

    # The mainloop
    tk.mainloop()
    return


# Create the master object
root = tk.Tk()

# Create Buttons
btn_speckle = tk.Button(root, width=12, height=3, text="Speckle", command = slct_speckle)
btn_speckle.grid(row=1, column=0)

btn_moon = tk.Button(root, width=12, height=3, text="Moon Cover", command = slct_moon)
btn_moon.grid(row=1, column=1)

btn_moon_exp = tk.Button(root, width=12, height=3, text="Moon Exposure", command = slct_moon_exp)
btn_moon_exp.grid(row=1, column=2)

btn__hv_cloud = tk.Button(root, width=12, height=3, text="Heavy Cloud", command = slct_cloud_heavy)
btn__hv_cloud.grid(row=1, column=3)

btn_cloud = tk.Button(root, width=12, height=3, text="Cloud", command = slct_cloud)
btn_cloud.grid(row=1, column=4)

btn_alm_clear = tk.Button(root, width=12, height=3, text="Almost Clear", command = slct_alm_clear)
btn_alm_clear.grid(row=1, column=5)

btn_clear = tk.Button(root, width=12, height=3, text="Completely Clear", command = slct_clear)
btn_clear.grid(row=1, column=6)

btn_other = tk.Button(root, width=12, height=3, text="Other", command = slct_other)
btn_other.grid(row=1, column=7)