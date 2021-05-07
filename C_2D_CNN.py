# cnn model
import numpy
from numpy import newaxis, mean, std
from csv import reader
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Flatten, Dropout
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.utils import to_categorical
from keras import backend as K
import keras

class CNN:
	def __init__(self, dropout_rate, num_filters, num_units_dense, act_func, num_outputs):
		# Constructor: Initilise the CNN with hyperparameters specified

			# INPUTS:
			# dropout rate - 

		self.d_rate = dropout_rate
		self.filters = num_filters
		self.units_dense = num_units_dense
		self.act_func = act_func
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

	def load_submission_data(self, trainingData, submissionData):
		# This function is used when the CNN is required to predict data
		# TrainX and trainy are set up like before but using the whole training dataset this time
		trainX, trainy = self.assign_data(trainingData,len(trainingData))
		# trainy is converted from a 1D list to a 2D list
		trainy = self.set_up_output(trainy)
		# trainX and trainy are converted to numpy arrays and saved
		self.trainX = self.convert_to_array(trainX, 'in')
		self.trainy = self.convert_to_array(trainy, 'out')
		# the submission data is converted to a numpy array ready to be classified
		self.predictX = self.convert_to_array(submissionData, 'in')
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
			numpArray=numpy.array(pyList)
			numpArray = numpArray.astype('float32')
			numpArray /= 255
			numpArray = numpArray[:,:,:,newaxis]
		else:
			numpArray=numpy.array([numpy.array(xi) for xi in pyList])
		# Array is returned
		return numpArray

	def updateParameters(self, dropout_rate, num_filters, num_units_dense, act_func):
		# CNN parameters are updated as specified
		self.d_rate = dropout_rate
		self.filters = num_filters
		self.units_dense = num_units_dense
		self.act_func = act_func

	def CNN_2D_evaluate(self, img_size):
		##model building
		model = Sequential()

		#convolutional layer with rectified linear unit activation
		model.add(Conv2D(32, kernel_size=(3, 3),
						activation='relu',
						input_shape=(img_size,img_size,1)))
		#32 convolution filters used each of size 3x3
		#again
		model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
		#64 convolution filters used each of size 3x3
		#choose the best features via pooling
		model.add(MaxPooling2D(pool_size=(2, 2)))
		#randomly turn neurons on and off to improve convergence
		model.add(Dropout(0.25))
		#flatten since too many dimensions, we only want a classification output
		model.add(Flatten())
		#fully connected to get all relevant data
		model.add(Dense(128, activation='relu'))
		#one more dropout for convergence' sake :) 
		model.add(Dropout(0.5))
		#output a softmax to squash the matrix into output probabilities
		model.add(Dense(self.num_outputs, activation='softmax'))

		#Adaptive learning rate (adaDelta) is a popular form of gradient descent rivaled only by adam and adagrad
		#categorical ce since we have multiple classes (10) 
		model.compile(loss=keras.losses.categorical_crossentropy,
					optimizer=keras.optimizers.Adadelta(),
					metrics=['accuracy'])

		batch_size = 128
		num_epoch = 7
		#model training
		model_log = model.fit(self.trainX, self.trainy,
				batch_size=batch_size,
				epochs=num_epoch,
				verbose=1,
				validation_data=(self.testX, self.testy))

		score = model.evaluate(self.testX, self.testy, verbose=0)
		print('Test loss:', score[0])
		print('Test accuracy:', score[1])
		return score

	# def CNN_evaluate(self, verbose = 0, epochs = 10, batch_size = 32, kernel_size = 3):
	# 	# This function is used to just test the CNN
	# 	# Define the network size, timesteps = 90, features = 1, outputs = 4
	# 	num_timesteps, num_features, num_outputs = len(self.trainX[0]), 1, len(self.trainy[0])

	# 	# Use a sequential Keras CNN model as it is easy to chop and change layers
	# 	model = Sequential()

	# 	# Build the CNN architecture by adding layers in order then compile
	# 	# Add a convolutional layer followed by ReLU layer, define the input size
	# 	model.add(Conv1D(filters=self.filters[0], kernel_size=kernel_size, activation='relu', input_shape=(num_timesteps,num_features)))
	# 	# Add another conv layer + ReLU layer
	# 	model.add(Conv1D(filters=self.filters[1], kernel_size=kernel_size, activation='relu'))
	# 	# Add a dropout layer to drop random weights
	# 	model.add(Dropout(self.d_rate))
	# 	# Max pooling layer reduces the size of the data down so less weights are required
	# 	model.add(MaxPooling1D(pool_size=2))
	# 	# Flatten converts the data to 1D in preperation for the fully connected layers
	# 	model.add(Flatten())
	# 	# The fully connected (dense) layers contain the weights to be trained
	# 	model.add(Dense(self.units_dense, activation=self.act_func))
	# 	# A softmax activation function is used at the output to normalise the outputs
	# 	model.add(Dense(num_outputs, activation='softmax'))
	# 	# The CNN is compiled with a cateorical crossentropy loss and adam optimiser, these are discussed in the report
	# 	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc',self.f1_m,self.precision_m, self.recall_m])
		
	# 	# Train the CNN
	# 	model.fit(self.trainX, self.trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)
		
	# 	# Test the CNN, return the f1 score
	# 	loss, accuracy, f1_score, precision, recall = model.evaluate(self.testX, self.testy, batch_size=batch_size, verbose=verbose)
	# 	# Return the f1 score
	# 	return f1_score

	# def CNN_predict(self, verbose = 0, epochs = 10, batch_size = 32, kernel_size = 3):
	# 	# This function is used to predict submission classes
	# 	trainX = self.trainX
	# 	trainy = self.trainy
	# 	predictX = self.predictX
	# 	n_timesteps, n_features, n_outputs = len(trainX[0]), 1, len(trainy[0])
	# 	# Use a sequential Keras CNN model as it is easy to chop and change layers
	# 	model = Sequential()

	# 	# Build the CNN architecture by adding layers in order then compile
	# 	# Add a convolutional layer followed by ReLU layer, define the input size
	# 	model.add(Conv1D(filters=self.filters[0], kernel_size=kernel_size, activation='relu', input_shape=(num_timesteps,num_features)))
	# 	# Add another conv layer + ReLU layer
	# 	model.add(Conv1D(filters=self.filters[1], kernel_size=kernel_size, activation='relu'))
	# 	# Add a dropout layer to drop random weights
	# 	model.add(Dropout(self.d_rate))
	# 	# Max pooling layer reduces the size of the data down so less weights are required
	# 	model.add(MaxPooling1D(pool_size=2))
	# 	# Flatten converts the data to 1D in preperation for the fully connected layers
	# 	model.add(Flatten())
	# 	# The fully connected (dense) layers contain the weights to be trained
	# 	model.add(Dense(self.units_dense, activation=self.act_func))
	# 	# A softmax activation function is used at the output to normalise the outputs
	# 	model.add(Dense(num_outputs, activation='softmax'))
	# 	# The CNN is compiled with a cateorical crossentropy loss and adam optimiser, these are discussed in the report
	# 	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc',self.f1_m,self.precision_m, self.recall_m])

	# 	# Model is trained using the training data
	# 	model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)

	# 	# The CNN then predicts the submission classes
	# 	predicty = model.predict(predictX, verbose=verbose)
	# 	# Return the predicted classes
	# 	return predicty

	# def recall_m(self, y_true, y_pred):
	# 	# Tensorflow no longer supports the f1 score so these functions are required to calculate it
	# 	# The true positives and possible positives are calculated and then used to work out the recall
	# 	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	# 	possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
	# 	recall = true_positives / (possible_positives + K.epsilon())
	# 	# Return recall
	# 	return recall

	# def precision_m(self, y_true, y_pred):
	# 	# Tensorflow no longer supports the f1 score so these functions are required to calculate it
	# 	# The true positive and predicted positives are calculated and then used to work out the precision
	# 	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	# 	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	# 	precision = true_positives / (predicted_positives + K.epsilon())
	# 	# Return precision
	# 	return precision

	# def f1_m(self, y_true, y_pred):
	# 	# Tensorflow no longer supports the f1 score so these functions are required to calculate it
	# 	precision = self.precision_m(y_true, y_pred)
	# 	recall = self.recall_m(y_true, y_pred)
	# 	# Return the harmonic mean of the precision and recall scores
	# 	return 2*((precision*recall)/(precision+recall+K.epsilon()))

		
	
