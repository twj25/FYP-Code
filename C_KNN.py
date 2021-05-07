import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

class KNN:

    def __init__(self,num_outputs):
        self.num_outputs = num_outputs


    def load_evaluation_data(self, data, split):
        # Function purpose: to load the training data in the correct format

            # INPUTS:
            # data(list of lists) - the training data, each entry contains a class and a 64x64 image array
            # split(integer) - to specify the split between train and test data

            # OUTPUTS:
            # trainX(float 32 array) - images for training
            # trainy(float 32 array) - classes corresponding to training images
            # testX(float 32 array) - images for testing
            # testy(float 32 array) - classes corresponding to testing images

        # Assign data divides the data into trainX, trainy, testX and testy,  split the data for training and testing
        trainX, trainy, testX, testy = self.assign_data(data,split)

        # The outputs need to be converted from 1D lists to 2D list where each row has 3 zeros and a 1
        trainy = self.set_up_output(trainy)
        testy = self.set_up_output(testy)

        # Every list need to be converted to a numpy array and saved to the CNN
        self.trainX = self.convert_to_array(trainX, 'in')
        self.trainy = self.convert_to_array(trainy, 'out')
        self.testX = self.convert_to_array(testX, 'in')
        self.testy = self.convert_to_array(testy, 'out')
        return
    
    def assign_data(self, data, split):
        # This function is used to split up the training data
        # Lists are created for the outputs
        trainX, V_trainy, testX, V_testy = [], [], [], []
        # For prediction the split value is equal to the lenght of the data so all training data is used for training
        if split == len(data):
            train = data
            # Each row is divided into the class and the remaining waveform values
            for result in train:
                trainX.append(result[1])
                V_trainy.append(result[0])
            # Lists are returned
            return trainX, V_trainy
        else:
            # This is if the split is not set to max
            train, test = data[:split], data[(split+1):]
            # The same process of dividng the data is completed for train and test
            for result in train:
                trainX.append(result[1])
                V_trainy.append(result[0])
            for result in test:
                testX.append(result[1])
                V_testy.append(result[0])
            # The final lists are returned
            return trainX, V_trainy, testX, V_testy

    def set_up_output(self, y1Dlist):
        # A new list is created for the output
        y2Dlist = []
        # For each number in the 1D list the relevant output is detected and set up as a row with 3 zeros and a one
        for num in y1Dlist:
            line = [0]*self.num_outputs
            line[int(num)-1] = 1
            y2Dlist.append(line)
        # The 2D list is returned
        return y2Dlist

    def convert_to_array(self, pyList, type):
        # Takes a list as an input, returns a numpy array
        
        # The output varies slightly for inputs and outputs to the CNN
        if type == 'in':
            # Inputs are converted to floats and given an extra dimension so they are compatable with the CNN
            numpArray=np.array(pyList)
            numpArray = numpArray.astype('float32')
            numpArray /= 255
            numpArray = numpArray.reshape(len(numpArray),-1)
            #numpArray = numpArray[:,:,:,np.newaxis]
        else:
            numpArray=np.array([np.array(xi) for xi in pyList])
        # Array is returned
        return numpArray

    def evaluate(self):
        knn_clf = KNeighborsClassifier()
        knn_clf.fit(self.trainX, self.trainy)

        preds = knn_clf.predict(self.testX)

        accuracy = accuracy_score(self.testy, preds)
        print(accuracy)
        return

    def test_k_value(self):
        acc_list = []
        # testing knn classifier with 20 k values
        for i in range(3, 3):
            knn_clf = KNeighborsClassifier(n_neighbors=i)
            
            knn_clf.fit(self.trainX, self.trainy)
            
            preds = knn_clf.predict(self.testX)
            
            accuracy = accuracy_score(self.testy, preds)*100
            
            acc_list.append(accuracy)

        return acc_list