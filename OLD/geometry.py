import matplotlib.pyplot as plt
import numpy as np 
import math
import csv
from PIL import Image

def test(org_cord):
    new_cord = (1,2)
    return new_cord

def step_one(org_cord): # input is pixel coordiates of original array (i,j)
    coefficients = np.ones([3,2])

    i = org_cord[0]
    j = org_cord[1]
   
    f = i/127
    g = j/127
    std_cord = (f,g)
    return std_cord

def step_two(std_cord):
    f = std_cord[0]
    g = std_cord[1]

    if f == 0:
        f = 0.000001
    az = math.atan(g/f)
    el = math.sqrt(f**2 + g**2)

    azel_cord = (az, el)
    return azel_cord

def step_three(azel_cord):
    az = azel_cord[0]
    el = azel_cord[1]

    
    

org_cords_arr = np.empty((255,255),dtype=object)

len_x,len_y = org_cords_arr.shape
# Convert from pixel_num to x,y tuple WITH loop
for cur_y in range(len_y):
    for cur_x in range(len_x):
        org_cords_arr[cur_x][cur_y] = (cur_x + 1 - round(len_x/2),cur_y + 1 - round(len_y/2))
        #xy_arr[cur_x][cur_y] = 1


# Convert from pixel_num to x,y tuple WITHOUT loop
# conv_to_cord = np.vectorize(convert_to_x_y)
# new_xy_arr = conv_to_cord(xy_arr)

step_one_func = np.vectorize(step_one, otypes=[object])
std_cords_arr = step_one_func(org_cords_arr)

stp1vals = std_cords_arr.tolist()
with open('stp1vals.csv', 'w') as f:
    writer = csv.writer(f, lineterminator="\n")
    for tup in stp1vals:
        writer.writerow(tup)

step_two_func = np.vectorize(step_two, otypes=[object])
azel_cords_arr = step_two_func(std_cords_arr)

stp2vals = azel_cords_arr.tolist()
with open('stp2vals.csv', 'w') as f:
    writer = csv.writer(f, lineterminator="\n")
    for tup in stp2vals:
        writer.writerow(tup)


# img_array = plt.imread("T072142A269_.gif")
# img = Image.fromarray(img_array, 'L')
# img.save('test.png')
# img.show()




