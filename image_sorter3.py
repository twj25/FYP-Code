import tkinter as tk
from PIL import Image, ImageTk
import shutil
import os

def slct_speckle():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")[-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Speckle/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_moon():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Moon/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return 

def slct_moon_exp():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Moon_Exposure/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_cloud_heavy():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/V_Cloudy/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_cloud():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Cloudy/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_alm_clear():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Almost_Clear/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_clear():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")
    file_name = file_name[len(file_name)-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Clear/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def slct_other():
    global current_image
    file_name = images[current_image]
    file_name = file_name.split("/")[-1]
    new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/Other/" + file_name
    shutil.move(images[current_image], new_dir)
    update_image()
    return

def update_image():
    global current_image
    current_image += 300
    photo2 = ImageTk.PhotoImage(Image.open(images[current_image]))
    img.config(image = photo2) 
    img.photo_ref = photo2
    return

# Create the master object
root = tk.Tk()
  
# Create the PIL image object
unsorted_path = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Unsorted/"
unsorted_files = os.listdir(unsorted_path)

images = []
for image in unsorted_files:
    cur_dir = unsorted_path + image
    #images.append(tk.PhotoImage(file=cur_dir))
    images.append(cur_dir)
current_image = 0

photo = ImageTk.PhotoImage(Image.open(images[current_image]))
img = tk.Label(root,image = photo)

# # Create an image label
# img_label = tk.Label(image=images[current_image])
# # Store a reference to a PhotoImage object, to avoid it
# # being garbage collected! This is necesary to display the image!
# img_label.image = images[current_image]

#img_label.grid(columnspan=5,row=0, column=0)
img.grid(columnspan=8, row=0, column= 0)
 
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
 
# The mainloop
tk.mainloop()