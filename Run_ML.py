from matplotlib import pyplot as plt
import cv2
import csv
import numpy as np
import random
import glob
from PIL import Image
from C_2D_CNN import CNN
from C_kmeans import Kmeans
import shutil
import os
import time
import math

def import_data(dataset, path, class_idenfier, max = -1):
    counter = 0

    for filename in glob.glob(path): #assuming gif

        # Read image data
        img_array = plt.imread(filename)

        # Compress and flatten
        compressed_img = cv2.resize(img_array, dsize=(128, 128))
        #compressed_img = compressed_img.flatten()

        # Assign class identifier as the first digit of each line
        # -1 = unsupervised learning, therefore don't add identifier
        if class_idenfier == -1:
            training_array = [filename.split("\\")[-1], compressed_img]
            dataset.append(training_array)
        # else = supervised learning, therefore add identifier
        else:
            training_array= [class_idenfier,compressed_img]
            dataset.append(training_array)

        # This break allows a maximum quantity of data to be set
        counter += 1
        print(counter)
        if counter == max:
            break

    return dataset

def import_all_training():
    training_dataset = []
    base_path = 'C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Sorted/'
    classes = ['Moon', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear', 'Speckle']
    #classes = ['Moon', 'Cloudy', 'Speckle'] # Test 1

    class_id = 0

    for CLASS in classes:
        path = base_path + CLASS + '/*.gif'
        training_dataset = import_data(training_dataset,path,class_id)
        #training_dataset = import_data(training_dataset,path,-1) # Test 1
        class_id += 1

    random.shuffle(training_dataset)
    return training_dataset

def import_all(max_quant):
    path = 'C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Unsorted/*.gif'
    training_dataset = []
    # Import all data, -1 tells function not to add a class identifier to each entry
    iterations = math.ceil(max_quant/500)
    for i in range(iterations):
        training_dataset = import_data(training_dataset,path,-1, max=500)
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

def run_kmeans(outputs,samples):
    data = import_all(samples)
    #data = import_all_training() # Test 1

    kmeans_O = Kmeans(outputs)
    kmeans_O.load_evaluation_data(data)
    labels = kmeans_O.cluster()

    move_to_new_dir(labels)
    return 

def move_to_new_dir(labels):
    counter = 0
    for data in labels:
        cluster_label = data[0]
        file = data[1]
        old_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Unsorted/" + file

        if cluster_label == 0:
            new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Clustered/0/" + file
        elif cluster_label == 1:
            new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Clustered/1/" + file
        elif cluster_label == 2:
            new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Clustered/2/" + file
        elif cluster_label == 3:
            new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Clustered/3/" + file
        else:
            new_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Clustered/4/" + file
        if counter == 199:
            z= 1
        time.sleep(0.05)
        shutil.copy(old_dir,new_dir)
        print(counter)
        counter +=1

    return
        


train_test_split = 180
num_outputs = 5
samples = 300

# acc, loss = run_CNN(num_outputs, train_test_split)
run_kmeans(num_outputs, samples)

# Test 1
# Lines 44,51,54,98
# Test to see if clustering would work correctly on unshuffled, sorted data

