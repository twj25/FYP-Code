from matplotlib import pyplot as plt
import cv2
from PIL import Image
import numpy as np
import random
import glob
from C_CNN import CNN

def import_data(location, class_idenfier):
    base_path = 'C:/Users/tomjo/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/'
    path = base_path + location + '/*.gif'

    image_list = []
    for filename in glob.glob(): #assuming gif
        img_array = plt.imread(filename)
        compressed_img = cv2.resize(img_array, dsize=(64, 64))
        compressed_img = compressed_img.flatten()

        # This code here generates a random number an assigns it as the first digit to create a dummy training dataset
        rand = round(random.randint(1,8)/2)
        training_array= np.insert(compressed_img, 0 ,rand)
        image_list.append(training_array)


import_data("Moon",0)


x = 1