from sklearn.neural_network import MLPClassifier
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import numpy
from f_import_data import import_all_training
import csv
import time

def unpack_data():
    source = ['mercedes', '5577', '2020', 'Aug']
    training_data = import_all_training(source,shuffle=True)
    print("Quantity of training data:", len(training_data))

    classifier_outputs = len(numpy.unique(numpy.array(training_data, dtype=object)[:,0]))

    X = []
    y = []
    for sample in training_data:
        # For each sample in the training dataset the inputs become a normalised array of the original data
        inputs = sample[1]
        inputs = (inputs/ 255 * 0.99) + 0.01
        inputs = inputs.flatten()
        #inputs = (numpy.asfarray(sample[1:])/ 255 * 0.99) + 0.01
        X.append(inputs)

        # An array of target values is set up based on the neuron sample type specified at the start of each line
        targets = numpy.zeros(classifier_outputs) + 0.01
        targets[int(sample[0])] = 0.99    
        y.append(int(sample[0]))
        pass
    X = numpy.array(X)
    y = numpy.array(y)
    return X,y



final_acc_list,acc_list,MLPtimes = list(),list(),list()
nodes = [20,20,20,20,20,20]
#nodes = [5,10,20,30,40,50,[2,2],[5,10],[10,10],[10,15],[15,15],[20,10],[30,30],[40,20],[5,5,5],[5,10,15],[15,10,15]]
#nodes = [[500,500,500,500,500,500]]
num_tests = 1

#nodes = [[2,2],[5,10],[10,10],[10,15],[15,15],[20,10],[30,30],[40,20]]
#X, y = make_classification(n_samples=100, random_state=1)
for i in range(num_tests):
    X1, y1 = unpack_data()#
    for i in range(len(nodes)):
        X_train, X_test, y_train, y_test = train_test_split(X1, y1, stratify=y1, random_state=1)
        # clf = MLPClassifier(hidden_layer_sizes=(nodes[i]),random_state=1, max_iter=200).fit(X_train, y_train)
        # clf.predict_proba(X_test[:1])
        # #array([[0.038..., 0.961...]])
        # clf.predict(X_test[:5, :])
        # #array([1, 0, 1, 0, 1])
        # print(clf.score(X_test, y_test))
        time_start = time.time()
        # create mutli-layer perceptron classifier
        clf = MLPClassifier(hidden_layer_sizes=(nodes[i]),random_state=1,max_iter=200).fit(X_train, y_train)

        # train
        clf.fit(X_train, y_train)
        timetest = time.time()-time_start
        #print(clf.predict(X_test[:, :]))
        print(nodes[i],' = ',clf.score(X_test, y_test))
        acc_list.append(clf.score(X_test, y_test))
        MLPtimes.append(timetest)
    final_acc_list.append(acc_list)
    i = 0
    acc_list = []

# with open("MLP_acc_log.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(final_acc_list)

with open("MLP_time_log.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(MLPtimes)
