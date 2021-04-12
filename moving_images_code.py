import shutil
import os

unsorted_path = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Unsorted/"
unsorted_files = os.listdir(unsorted_path)
images = []
for image in unsorted_files:
    cur_dir = unsorted_path + image
    #images.append(tk.PhotoImage(file=cur_dir))
    images.append(cur_dir)

current_image = 0
file_name = images[current_image]
file_name = file_name.split("/")[-1]
new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Clustered/" + file_name
shutil.copy(images[current_image], new_dir)