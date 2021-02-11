import matplotlib.pyplot as plt
import numpy as np 
import math
import csv
from PIL import Image

def convert_to_pix_num(x,y):
    pix_num = (255*y)+x + 1
    return pix_num


def convert_to_x_y(pix_num):
    x = pix_num % 255 - 1
    y = math.floor(pix_num / 255)
    cord = (x,y)
    return cord

def step_one(org_cord): # input is pixel coordiates of original array (i,j)
    coefficients = np.ones([3,2])

    i,j = convert_to_x_y(org_cord)
    homogen_ij_matrix = np.array([1,i,j])
    f,g = np.matmul(homogen_ij_matrix,coefficients)
    std_cord = convert_to_pix_num(f,g)
    return std_cord



# basic_cords_arr = np.arange(1,65026)
# xy_arr = basic_cords_arr.reshape(255,255)
# xy_arr.astype(object)

# basic_cords_arr = np.arange(1,26)
# xy_arr = basic_cords_arr.reshape(5,5)
# xy_arr.astype(object)

xy_arr = np.empty((255,255),dtype=object)

index_x,index_y = xy_arr.shape
# Convert from pixel_num to x,y tuple WITH loop
for cur_y in range(index_y):
    for cur_x in range(index_x):
        xy_arr[cur_x][cur_y] = (cur_x + 1,cur_y + 1)
        #xy_arr[cur_x][cur_y] = 1


# Convert from pixel_num to x,y tuple WITHOUT loop
# conv_to_cord = np.vectorize(convert_to_x_y)
# new_xy_arr = conv_to_cord(xy_arr)

# step_one_func = np.vectorize(step_one)
# std_cords_arr = step_one_func(org_cords_arr)

test = xy_arr.tolist()
with open('test.csv', 'w') as f:
    writer = csv.writer(f, lineterminator="\n")
    for tup in test:
        writer.writerow(tup)
# np.savetxt("test.csv", xy_arr, delimiter=",")



# img_array = plt.imread("T072142A269_.gif")
# img = Image.fromarray(img_array, 'L')
# img.save('test.png')
# img.show()




