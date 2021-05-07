import cv2
import numpy as np
from PIL import Image,ImageOps
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


def plot_sidebyside(file):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(file)

    
    img_array = Image.open(file)
    #im_invert = ImageOps.invert(img_array)
    ax1.imshow(img_array, cmap='gray', vmin=0, vmax=255)
    ax1.set_xlabel("x Pixel Position")
    ax1.set_ylabel("y Pixel Position")
    #img = plt.imread(file)
    img = cv2.imread(file, 0)
    ax2.hist(img.ravel(),256,[0,256])
    ax2.set_xlabel("Grey Level")
    ax2.set_ylabel("Number of Pixels")
    plt.show()
    return

def plot_img(file):
    img_array = plt.imread(file)
    img = Image.fromarray(img_array, 'L')
    #img.save('test.png')
    img.show()


files = ['clear.png','cloudy.png', 'moon.png']
#plot_img(file)
plot_sidebyside(files[2])