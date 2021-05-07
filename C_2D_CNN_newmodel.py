# baseline cnn model for mnist
from f_import_data import import_all_training, import_all, import_prediction
from numpy import mean, std, newaxis
import numpy
import shutil
import os
import csv
import time
from matplotlib import pyplot
from sklearn.model_selection import KFold
from keras.datasets import mnist
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.optimizers import SGD

# load train and test dataset
def load_evaluation_data(data, split, num_outputs):
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
	trainX, trainy, testX, testy = assign_data(data,split)

	# The outputs need to be converted from 1D lists to 2D list where each row has 3 zeros and a 1
	trainy = set_up_output(trainy, num_outputs)
	testy = set_up_output(testy, num_outputs)

	# Every list need to be converted to a numpy array and saved to the CNN
	trainX = convert_to_array(trainX, 'in')
	trainy = convert_to_array(trainy, 'out')
	testX = convert_to_array(testX, 'in')
	testy = convert_to_array(testy, 'out')
	return trainX,trainy, testX, testy

def load_unlabelled_data(data):
	img_arrays = []
	for img in data:
		img_arrays.append(img[1])
	predictX = convert_to_array(img_arrays, 'in')
	return predictX

def assign_data(data, split):
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

def set_up_output(y1Dlist, num_outputs):
	# A new list is created for the output
	y2Dlist = []
	# For each number in the 1D list the relevant output is detected and set up as a row with 3 zeros and a one
	for num in y1Dlist:
		line = [0]*num_outputs
		line[int(num)] = 1
		y2Dlist.append(line)
	# The 2D list is returned
	return y2Dlist

def convert_to_array(pyList, type):
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

# define cnn model
def define_model(img_sz, num_outputs):
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(img_sz, img_sz, 1)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(num_outputs, activation='softmax'))
	# compile model
	opt = SGD(lr=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model

# define cnn model
def define_model1(img_sz, num_outputs):
	model = Sequential()
	model.add(Conv2D(128, (5, 5), activation='relu', kernel_initializer='he_uniform', input_shape=(img_sz, img_sz, 1)))
	model.add(Conv2D(64, (5, 5), activation='relu', kernel_initializer='he_uniform'))
	model.add(Dropout(0.4))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(num_outputs, activation='softmax'))
	# compile model
	opt = SGD(lr=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model

# define cnn model
def define_model2(img_sz, num_outputs):
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(img_sz, img_sz, 1)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	model.add(MaxPooling2D((2, 2)))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(num_outputs, activation='softmax'))
	# compile model
	opt = SGD(lr=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model

def define_model3(img_sz, num_outputs):
	model = Sequential()
	model.add(Conv2D(32, (3, 3), activation='relu', kernel_initializer='he_uniform', input_shape=(img_sz, img_sz, 1)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	model.add(Conv2D(64, (3, 3), activation='relu', kernel_initializer='he_uniform'))
	model.add(MaxPooling2D((2, 2)))
	model.add(Dropout(0.2))
	model.add(Flatten())
	model.add(Dense(100, activation='relu', kernel_initializer='he_uniform'))
	model.add(Dense(num_outputs, activation='softmax'))
	# compile model
	opt = SGD(lr=0.01, momentum=0.9)
	model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
	return model

# evaluate a model using k-fold cross-validation
def kfold_evaluate_model(dataX, dataY, img_sz, num_outputs, n_folds=5):
	scores, histories, times = list(), list(), list()
	# prepare cross validation
	kfold = KFold(n_folds, shuffle=True, random_state=1)
	# enumerate splits
	for train_ix, test_ix in kfold.split(dataX):
		# define model
		time_start = time.time()
		model = define_model3(img_sz, num_outputs)
		# select rows for train and test
		trainX, trainY, testX, testY = dataX[train_ix], dataY[train_ix], dataX[test_ix], dataY[test_ix]
		# fit model
		history = model.fit(trainX, trainY, epochs=20, batch_size=32, validation_data=(testX, testY), verbose=1)
		# evaluate model
		_, acc = model.evaluate(testX, testY, verbose=1)
		times.append(time.time()-time_start)
		print('> %.3f' % (acc * 100.0))
		# stores scores
		scores.append(acc)
		histories.append(history)
		
	return scores, histories, times

# evaluate a model using k-fold cross-validation
def evaluate_model(trainX, trainY, testX, testY, img_sz, num_outputs):
	# define model
	model = define_model2(img_sz, num_outputs)
	# fit model
	history = model.fit(trainX, trainY, epochs=20, batch_size=32, validation_data=(testX, testY), verbose=1)
	# evaluate model
	_, acc = model.evaluate(testX, testY, verbose=1)
	print('> %.3f' % (acc * 100.0))
	scores, histories = list(), list()
	histories.append(history)
	scores.append(acc)	
	return scores, histories

def prediction_model(trainX, trainY, predictX, img_sz, num_outputs):
	# define model
	model = define_model2(img_sz, num_outputs)
	# fit model
	history = model.fit(trainX, trainY, epochs=20, batch_size=32, verbose=1)
	# evaluate model
	predicty = model.predict(predictX, verbose = 1)
	return predicty


# plot diagnostic learning curves
def summarize_diagnostics(histories):
	
	for i in range(len(histories)):
		# plot loss
		pyplot.rcParams.update({'font.size': 18})
		pyplot.subplot(1, 2, 1)
		if i == 1:
			pyplot.plot(histories[i].history['loss'], color='blue', label='train')
			pyplot.plot(histories[i].history['val_loss'], color='orange', label='test')
		else:
			pyplot.plot(histories[i].history['loss'], color='blue', label='_Hidden')
			pyplot.plot(histories[i].history['val_loss'], color='orange', label='_Hidden')
		
		# plot accuracy
		pyplot.subplot(1, 2, 2)
		if i == 1:
			pyplot.plot(histories[i].history['accuracy'], color='blue', label='train')
			pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='test')
		else:
			pyplot.plot(histories[i].history['accuracy'], color='blue', label='_Hidden')
			pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='_Hidden')
	
	
	pyplot.title('Classification Accuracy', loc="center",fontweight="bold")
	pyplot.xlabel("Epoch")
	pyplot.ylabel("Accuracy")
	pyplot.legend(loc= "lower right")
	pyplot.ylim(top=1)

	pyplot.subplot(1, 2, 1)
	pyplot.title('Cross Entropy Loss', loc="center",fontweight="bold")
	pyplot.xlabel("Epoch")
	pyplot.ylabel("Loss")
	pyplot.ylim(bottom=0)
	#pyplot.tight_layout()
	pyplot.show()

def summarize_accuracy(histories):
	for i in range(len(histories)):
		pyplot.rcParams.update({'font.size': 18})
				
		# plot accuracy
		if i == 0:
			pyplot.plot(histories[i].history['accuracy'], color='blue', label='train')
			pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='test')
		else:
			pyplot.plot(histories[i].history['accuracy'], color='blue', label='_Hidden')
			pyplot.plot(histories[i].history['val_accuracy'], color='orange', label='_Hidden')
	
	
	pyplot.title('Classification Accuracy', loc="center",fontweight="bold")
	pyplot.xlabel("Epoch")
	pyplot.ylabel("Accuracy")
	pyplot.legend(loc= "lower right")
	pyplot.ylim(top=1)
	pyplot.show()
	

# summarize model performance
def summarize_performance(scores):
	# print summary
	print('Accuracy: mean=%.3f std=%.3f, n=%d' % (mean(scores)*100, std(scores)*100, len(scores)))
	# box and whisker plots of results
	pyplot.boxplot(scores)
	pyplot.show()

def simplify_predictions(dec_predictions, unlabelled_data):
	int_predictions = []
	for i in range(len(dec_predictions)):
		# Label is set to the maximum argument of the 4 output neurons from the classifier
		label = numpy.argmax(dec_predictions[i])
		# 1 is added to account for positions starting at 0
		label = int(label) + 1
		# The data is converted to a float
		label = float(label)
		# The label is added to the list
		int_predictions.append([label,unlabelled_data[i][0]])
	return int_predictions

# ~~~ Function to move classified images to individual folders ~~~
def organise_data(dec_predictions, source):
	# unpack the data source information, this is used to find the correct file path
	Location = source[0]
	Frequency = source[1]
	Year = source[2]
	Month = source[3]

	base_path = r"C:\Users\tomjo\OneDrive\Documents\50 University\Year 5\Individual Proj\Data\Final System Data\{}\{}\{}\{}".format(Location,Frequency,Year,Month)
	
	# If the paths are not yet established, make them
	classes = ['Moon', 'Moon_Exposure', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear','Speckle']
	for clas in classes:
		dir = base_path + "/Sorted By CNN/" + clas
		if not os.path.isdir(dir):
			os.makedirs(dir)
	
	# Loop through images and put in the correct folder
	for image in dec_predictions:
		file_name = image[1]
		label = int(image[0]) - 1
		old_dir = base_path + "/Unsorted/" + file_name
		
		
		new_dir = base_path + "/Sorted By CNN/" + classes[label] + "/" + file_name
		
		shutil.copy(old_dir, new_dir)

	return

# run the test harness for evaluating a model
def run_test_harness():
	# load dataset
	source = ["mcdonald","5577","2018","Jul"]
	train_test_split = 1000
	img_sz = 128
	trainingdata = import_all_training(source, shuffle=True, img_size= img_sz)
	if train_test_split > len(trainingdata):
		train_test_split = len(trainingdata) -2
	classifier_outputs = len(numpy.unique(numpy.array(trainingdata, dtype=object)[:,0]))
	trainX, trainY, testX, testY = load_evaluation_data(trainingdata, train_test_split, classifier_outputs)

	#### Test Model
	scores, histories, times = kfold_evaluate_model(trainX, trainY, img_sz, classifier_outputs, n_folds=5)
	#scores, histories = evaluate_model(trainX, trainY, testX, testY, img_sz, num_outputs)
	# learning curves
	summarize_accuracy(histories)
	# summarize estimated performance
	#summarize_performance(scores)
	with open("CNN_time_log.csv", "w", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(times)

	with open("CNN_acc_log.csv", "w", newline="") as f:
		writer = csv.writer(f)
		writer.writerow(scores)
	return

def run_prediction_model(source):
	# Import the training data for the CNN to learn from
	num_outputs = 7
	train_test_split = 500
	img_sz = 32
	trainingdata = import_all_training(source, shuffle=True, img_size= img_sz)
	if train_test_split > len(trainingdata):
		train_test_split = len(trainingdata) -2
	trainX, trainY, testX, testY = load_evaluation_data(trainingdata, train_test_split, num_outputs)

	# ~~~ Make Classification Predictions ~~~
	unlabelled_data = import_prediction(source)
	predictX = load_unlabelled_data(unlabelled_data)
	predictions = prediction_model(trainX,trainY, predictX,img_sz,num_outputs)
	labels = simplify_predictions(predictions, unlabelled_data)
	organise_data(labels,source)

	return
	

# entry point, run the test harness
#run_test_harness()
