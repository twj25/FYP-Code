from matplotlib import pyplot as plt
import cv2
import csv
import numpy as np
import random
import glob
from PIL import Image
from C_2D_CNN import CNN

def import_data(dataset, location, class_idenfier):
    base_path = 'C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/'
    path = base_path + location + '/*.gif'

    for filename in glob.glob(path): #assuming gif

        # Read image data
        img_array = plt.imread(filename)

        # Compress and flatten
        compressed_img = cv2.resize(img_array, dsize=(128, 128))
        #compressed_img = compressed_img.flatten()

        # Assign class identifier as the first digit of each line
        training_array= [class_idenfier,compressed_img]
        dataset.append(training_array)

    return dataset

def import_all_training():
    training_dataset = []
    training_dataset = import_data(training_dataset,"Moon",0)
    training_dataset = import_data(training_dataset,"V_Cloudy",1)
    training_dataset = import_data(training_dataset,"Cloudy",1)
    training_dataset = import_data(training_dataset,"Almost_Clear",1)
    training_dataset = import_data(training_dataset,"Clear",1)
    training_dataset = import_data(training_dataset,"Speckle",2)
    
    random.shuffle(training_dataset)
    return training_dataset

def check_dataset_entry(dataset, entry):
    # Print Lable
    print(dataset[entry][0])

    # Show image
    img_array = dataset[entry][1]
    img = Image.fromarray(img_array, 'L')
    img.save('test.png')
    img.show()
    return

def run_CNN(num_of_outputs, train_test_split, dropout_rate=0.5, num_of_filters=[64,128], num_of_dense_units=128, act_func='relu'):
    DR = dropout_rate
    NF = num_of_filters
    ND = num_of_dense_units
    AF = act_func
    NO = num_of_outputs

    # Import all training data and complete a sanity check on the split value.
    training_dataset = import_all_training()
    if train_test_split > len(training_dataset):
        raise Exception("Split must be smaller than dataset size!")
    
    newCNN = CNN(DR,NF,ND,AF,NO)
    newCNN.load_evaluation_data(training_dataset, train_test_split)
    score = newCNN.CNN_2D_evaluate()
    accuracy = score[1] * 100.0
    test_loss = score[0]
    return accuracy,test_loss


train_test_split = 180
number_outputs = 3

acc, loss = run_CNN(number_outputs, train_test_split)



