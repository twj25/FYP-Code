# cnn model
import numpy
from numpy import newaxis
from numpy import mean
from numpy import std
from csv import reader
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.utils import to_categorical
from keras import backend as K

class CNN:
	def __init__(self, dropout_rate, num_filters, num_units_dense, act_func):
		self.d_rate = dropout_rate
		self.filters = num_filters
		self.units_dense = num_units_dense
		self.act_func = act_func

	def load_evaluation_data(self, data):
		trainX, trainy, testX, testy = self.assign_data(data,50)
		trainy = self.set_up_output(trainy)
		testy = self.set_up_output(testy)
		self.trainX = self.convert_to_array(trainX, 'in')
		self.trainy = self.convert_to_array(trainy, 'out')
		self.testX = self.convert_to_array(testX, 'in')
		self.testy = self.convert_to_array(testy, 'out')
		return

	def load_prediction_data(self, trainingData, submissionData):
		trainX, trainy = self.assign_data(trainingData,len(trainingData))
		trainy = self.set_up_output(trainy)
		self.trainX = self.convert_to_array(trainX, 'in')
		self.trainy = self.convert_to_array(trainy, 'out')
		self.predictX = self.convert_to_array(submissionData, 'in')
		return

	def assign_data(self, data, split):
		trainX, V_trainy, testX, V_testy = [], [], [], []
		if split == len(data):
			train = data
			for result in train:
				trainX.append(result[1:])
				V_trainy.append(result[0])
			return trainX, V_trainy
		else:
			train, test = data[:split], data[(split+1):]
			for result in train:
				trainX.append(result[1:])
				V_trainy.append(result[0])
			for result in test:
				testX.append(result[1:])
				V_testy.append(result[0])
			return trainX, V_trainy, testX, V_testy

	def set_up_output(self, y1Dlist, numOutputs = 4):
		y2Dlist = []
		for num in y1Dlist:
			line = [0]*numOutputs
			line[int(num)-1] = 1
			y2Dlist.append(line)
		return y2Dlist

	def convert_to_array(self, pyList, type):
		numpArray=numpy.array([numpy.array(xi) for xi in pyList])
		if type == 'in':
			numpArray = numpArray.astype('float32')
			numpArray = numpArray[:,:,newaxis]
		return numpArray

	def updateParameters(self, dropout_rate, num_filters, num_units_dense, act_func):
		self.d_rate = dropout_rate
		self.filters = num_filters
		self.units_dense = num_units_dense
		self.act_func = act_func

	# fit and evaluate a model
	def evaluate_model(self, verbose = 0, epochs = 10, batch_size = 32, kernel_size = 3):
		trainX = self.trainX
		trainy = self.trainy
		testX = self.testX
		testy = self.testy
		n_timesteps, n_features, n_outputs = len(trainX[0]), 1, len(trainy[0])
		model = Sequential()
		model.add(Conv1D(filters=self.filters[0], kernel_size=kernel_size, activation='relu', input_shape=(n_timesteps,n_features)))
		model.add(Conv1D(filters=self.filters[1], kernel_size=kernel_size, activation='relu'))
		model.add(Dropout(self.d_rate))
		model.add(MaxPooling1D(pool_size=2))
		model.add(Flatten())
		model.add(Dense(self.units_dense, activation=self.act_func))
		model.add(Dense(n_outputs, activation='softmax'))
		model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc',self.f1_m,self.precision_m, self.recall_m])
		# fit network
		model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)
		# evaluate model
		#_, accuracy = model.evaluate(testX, testy, batch_size=batch_size, verbose=0)
		loss, accuracy, f1_score, precision, recall = model.evaluate(testX, testy, batch_size=batch_size, verbose=verbose)
		return f1_score

	def CNN_prediction(self, verbose = 0, epochs = 10, batch_size = 32, kernel_size = 3):
		trainX = self.trainX
		trainy = self.trainy
		predictX = self.predictX
		n_timesteps, n_features, n_outputs = len(trainX[0]), 1, len(trainy[0])
		model = Sequential()
		model.add(Conv1D(filters=self.filters[0], kernel_size=kernel_size, activation='relu', input_shape=(n_timesteps,n_features)))
		model.add(Conv1D(filters=self.filters[1], kernel_size=kernel_size, activation='relu'))
		model.add(Dropout(self.d_rate))
		model.add(MaxPooling1D(pool_size=2))
		model.add(Flatten())
		model.add(Dense(self.units_dense, activation=self.act_func))
		model.add(Dense(n_outputs, activation='softmax'))
		model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc',self.f1_m,self.precision_m, self.recall_m])
		model.fit(trainX, trainy, epochs=epochs, batch_size=batch_size, verbose=verbose)
		predicty = model.predict(predictX, verbose=verbose)
		return predicty

	def recall_m(self, y_true, y_pred):
		true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
		possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
		recall = true_positives / (possible_positives + K.epsilon())
		return recall

	def precision_m(self, y_true, y_pred):
		true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
		predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
		precision = true_positives / (predicted_positives + K.epsilon())
		return precision

	def f1_m(self, y_true, y_pred):
		precision = self.precision_m(y_true, y_pred)
		recall = self.recall_m(y_true, y_pred)
		return 2*((precision*recall)/(precision+recall+K.epsilon()))

	# summarize scores
	def summarize_results(self, scores):
		m, s = mean(scores), std(scores)
		return m, s
		
	
