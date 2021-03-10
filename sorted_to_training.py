from matplotlib import pyplot as plt
import cv2
import csv
import numpy as np
import random
import glob
from C_2D_CNN import CNN

def import_data(dataset, location, class_idenfier):
    base_path = 'C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/'
    path = base_path + location + '/*.gif'

    
    for filename in glob.glob(path): #assuming gif

        # Read image data
        img_array = plt.imread(filename)

        # Compress and flatten
        compressed_img = cv2.resize(img_array, dsize=(64, 64))
        #compressed_img = compressed_img.flatten()

        # Assign class identifier as the first digit of each line
        training_array= [class_idenfier,compressed_img]
        dataset.append(training_array)

    return dataset


training_dataset = []


training_dataset = import_data(training_dataset,"Moon",0)
training_dataset = import_data(training_dataset,"V_Cloudy",1)
training_dataset = import_data(training_dataset,"Cloudy",2)
training_dataset = import_data(training_dataset,"Almost_Clear",3)
training_dataset = import_data(training_dataset,"Clear",4)


random.shuffle(training_dataset)

newCNN = CNN(0.5,[64,128],128,'relu',5)
newCNN.load_evaluation_data(training_dataset, 80)
score = newCNN.CNN_2D_evaluate()
accuracy = score[1] * 100.0
test_loss = score[0]


