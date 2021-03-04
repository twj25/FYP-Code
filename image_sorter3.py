import tkinter as tk
from PIL import Image, ImageTk
import os

def slct_moon():
    update_image()
    return 

def slct_cloud_heavy():
    update_image()
    return

def slct_cloud():
    update_image()
    return

def slct_alm_clear():
    update_image()
    return

def slct_clear():
    update_image()
    return

def update_image():
    global current_image
    current_image += 1
    photo2 = ImageTk.PhotoImage(Image.open(images[current_image]))
    img.config(image = photo2) 
    img.photo_ref = photo2
    return

# Create the master object
root = tk.Tk()
  
# Create the PIL image object
unsorted_path = "C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Test/"
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
img.grid(columnspan=5, row=0, column= 0)
 
# Create Buttons 
btn_moon = tk.Button(root, width=15, height=3, text="Moon Cover", command = slct_moon)
btn_moon.grid(row=1, column=0)

btn__hv_cloud = tk.Button(root, width=15, height=3, text="Heavy Cloud", command = slct_cloud_heavy)
btn__hv_cloud.grid(row=1, column=1)

btn_cloud = tk.Button(root, width=15, height=3, text="Cloud", command = slct_cloud)
btn_cloud.grid(row=1, column=2)

btn_alm_clear = tk.Button(root, width=15, height=3, text="Almost Clear", command = slct_alm_clear)
btn_alm_clear.grid(row=1, column=3)

btn_clear = tk.Button(root, width=15, height=3, text="Completely Clear", command = slct_clear)
btn_clear.grid(row=1, column=4)
 
# The mainloop
tk.mainloop()