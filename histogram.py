#import cv2
import numpy as np
from PIL import Image,ImageOps
from matplotlib import pyplot as plt
import matplotlib.image as mpimg


def plot_sidebyside(file):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle(file)

    
    img_array = Image.open(file)
    #im_invert = ImageOps.invert(img_array)
    ax1.imshow(img_array)
    
    img = plt.imread(file)
    ax2.hist(img.ravel(),256,[0,256])
    plt.show()
    return

def plot_img(file):
    img_array = plt.imread(file)
    img = Image.fromarray(img_array, 'L')
    #img.save('test.png')
    img.show()


files = ['clear.gif','cloudy.gif', 'moon.gif']
#plot_img(file)
plot_sidebyside(files[2])