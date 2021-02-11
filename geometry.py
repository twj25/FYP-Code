import matplotlib.pyplot as plt
import numpy as np 
import math
from PIL import Image

def convert_to_pix_num(x,y):
    pix_num = (255*y)+x + 1
    return pix_num


def convert_to_x_y(pix_num):
    x = pix_num % 255 - 1
    y = math.floor(pix_num / 255)
    return [x,y]

def step_one(org_cord): # input is pixel coordiates of original array (i,j)
    coefficients = np.ones([3,2])

    i,j = convert_to_x_y(org_cord)
    homogen_ij_matrix = np.array([1,i,j])
    f,g = np.matmul(homogen_ij_matrix,coefficients)
    std_cord = convert_to_pix_num(f,g)
    return std_cord


org_cords_arr = np.arange(1,65026)
org_cords_arr = org_cords_arr.reshape(255,255)

conv_to_cord = np.vectorize(convert_to_x_y)
xy_arr = conv_to_cord(org_cords_arr)

step_one_func = np.vectorize(step_one)
std_cords_arr = step_one_func(org_cords_arr)


np.savetxt("test.csv", std_cords_arr, delimiter=",")


# img_array = plt.imread("T072142A269_.gif")
# img = Image.fromarray(img_array, 'L')
# img.save('test.png')
# img.show()


