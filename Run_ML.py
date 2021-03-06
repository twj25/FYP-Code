from f_import_data import import_all_training, import_all
from C_Hierarachical import Hierarchical
from C_MLP import MLP
from C_2D_CNN import CNN
from C_KNN import KNN
from C_kmeans import Kmeans
import numpy
import csv
import time
import matplotlib.pyplot as plt
from sklearn.metrics import f1_score

def run_MLP(data, output_nodes, datasplit = 300, input_nodes = 1024, hidden_nodes = 200,  learning_rate = 0.1):
    

    # The dataset generated by pre-processing is split into training and testing data
    training = training_data[:datasplit]
    testing = training_data[datasplit + 1:]
    # THE FOLLOWING CODE IS USED TO KEEP TRACK OF THE BALANCE BETWEEN CLASSES
    # train_classes = numpy.array(training)[:,0]
    # test_classes = numpy.array(testing)[:,0]
    # print("0s in training:", train_classes.tolist().count(0), "1s in training:", train_classes.tolist().count(1), "2s in training:", train_classes.tolist().count(2))
    # print("0s in testing:", test_classes.tolist().count(0), "1s in testing:", test_classes.tolist().count(1), "2s in testing:", test_classes.tolist().count(2))


    # An instance of the mlp class is initialised  
    n = MLP(input_nodes,hidden_nodes,output_nodes,learning_rate)

    print("Training...")
    for sample in training:
        # For each sample in the training dataset the inputs become a normalised array of the original data
        inputs = sample[1]
        inputs = (inputs/ 255 * 0.99) + 0.01
        inputs = inputs.flatten()
        #inputs = (numpy.asfarray(sample[1:])/ 255 * 0.99) + 0.01

        # An array of target values is set up based on the neuron sample type specified at the start of each line
        targets = numpy.zeros(output_nodes) + 0.01
        targets[int(sample[0])] = 0.99

        # Weights in the network are trained
        n.train(inputs, targets)
        pass

    # Once the network has been trained the testing begins
    print("Testing...")
    # Lists are set up to hold the correct and predicted labels for calculation of the f1 score
    score = []
    correctLabels = []
    predictedLabels = []
    for sample in testing:
        # The correct label is the number specified at the start of the line
        correct_label = int(sample[0])
        # Inputs to the network are setup again like before
        inputs = sample[1]
        inputs = (inputs/ 255 * 0.99) + 0.01
        inputs = inputs.flatten() 
        #inputs = (numpy.asfarray(sample[1:])/ 255 * 0.99) + 0.01
        # But this time the network is queried rather than trained 
        outputs = n.query(inputs)
        # The prediction is the neuron with the largest output plus 1 to account for numbers starting at 0
        label = numpy.argmax(outputs)
        label = int(label)

        # Correct and predicted label lists are updated each iteration
        correctLabels.append(correct_label)
        predictedLabels.append(label)
        pass

    # The f1_score function from sklearn is used to calculate the f1 score using the lists, average method weighted is used
    f1Score = round(f1_score(y_true = correctLabels, y_pred = predictedLabels,average = 'weighted'),4)
    return f1Score

def run_CNN(num_of_outputs, train_test_split, dropout_rate=0.5, num_of_filters=[64,128], num_of_dense_units=128, act_func='relu'):
    DR = dropout_rate
    NF = num_of_filters
    ND = num_of_dense_units
    AF = act_func
    NO = num_of_outputs
    img_sze = 64

    # Import all training data and complete a sanity check on the split value.
    training_dataset = import_all_training("True", img_size= img_sze)
    if train_test_split > len(training_dataset):
        raise Exception("Split must be smaller than dataset size!")
    
    newCNN = CNN(DR,NF,ND,AF,NO)
    newCNN.load_evaluation_data(training_dataset, train_test_split)
    score = newCNN.CNN_2D_evaluate(img_sze)
    accuracy = score[1] * 100.0
    test_loss = score[0]
    return accuracy,test_loss

def run_KNN(training_dataset, outputs, train_test_split):
    if train_test_split > len(training_dataset):
        train_test_split = round(len(training_dataset)*0.8)

    time_start = time.time()
    newKNN = KNN(outputs)
    newKNN.load_evaluation_data(training_dataset,train_test_split)
    #newKNN.evaluate()
    acc_list = newKNN.test_k_value()
    timetest = time.time()-time_start
    num_k = numpy.arange(1, 21)

    with open("KNN_acc_log.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(acc_list)
    # plt.figure(dpi=100)
    # plt.style.use('ggplot')
    # plt.plot(num_k, acc_list)
    # plt.xlabel('Number of Neighbors')
    # plt.ylabel('Accuracy %')
    # plt.show()
    # plt.savefig('acc_plot.png')
    return timetest

def run_kmeans(outputs,samples,testmode):
    if testmode == True:
        data_source = ["mcdonald","5577","2018","Jul"]
        data = import_all_training(data_source)
    else:
        data = import_all(samples)
    time_start = time.time()
    kmeans_ob = Kmeans(outputs)
    kmeans_ob.load_evaluation_data(data)
    labels = kmeans_ob.cluster()
    timetest = time.time()-time_start
    #kmeans_ob.elbow_method(10)

    if testmode == True:
        with open("k-means_labels.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(labels)
    else:
        kmeans_ob.move_to_new_dir(labels)
    return timetest

def run_hierarch(num_clusters,samples,testmode):
    if testmode == True:
        data_source = ["mcdonald","5577","2018","Jul"]
        data = import_all_training(data_source)
    else:
        data = import_all(samples)

    time_start = time.time()
    hierarach_obj = Hierarchical(num_clusters)
    hierarach_obj.load_evaluation_data(data)
    labels = hierarach_obj.cluster()
    timetest = time.time()-time_start
    if testmode == True:
        with open("hierarchical_labels.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(labels)
    else:
        #hierarach_obj.move_to_new_dir(labels)
        pass
    return timetest

    

data_source = ["mcdonald","5577","2018","Jul"]
training_data = import_all_training(data_source, shuffle=True)
print("Quantity of training data:", len(training_data))
train_test_split = 350

classifier_outputs = len(numpy.unique(numpy.array(training_data, dtype=object)[:,0]))

# -------------- MLP TEST AREA  ---------------------------

# mlp_outputs = classifier_outputs
# hidden_nodes = [20,40,60,80,100,120,140]

# acc_list = []
# for i in range(3*len(hidden_nodes)-1):
#     hid_node = hidden_nodes[round(i/3)]
#     f1score = run_MLP(training_data, mlp_outputs, hidden_nodes=hid_node)
#     print("Hidden Nodes:", hid_node)
#     print("Accuracy:", f1score)
#     print("------------")
#     acc_list.append([hid_node,f1score])

# with open("MLP_acc_log.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(acc_list)

# ------------- CNN TEST AREA -----------------------------
# cnn_outputs = classifier_outputs
# acc, loss = run_CNN(cnn_outputs, train_test_split)


# ------------- KNN TEST AREA ------------------------------

knn_outputs = classifier_outputs
KNNtimes = []
for i in range(5):
    KNNtimes.append(run_KNN(training_data,knn_outputs,train_test_split))
with open("KNN_time_log.csv", "w", newline="") as f:
	writer = csv.writer(f)
	writer.writerow(KNNtimes)

# ------------- K-MEANS TEST AREA -------------------------
# k_means_outputs = 6
# samples = 2000
# Kmeanstimes = []
# for i in range(5):
#     Kmeanstimes.append(run_kmeans(k_means_outputs, samples, testmode=True))
# with open("Kmeans_time_log.csv", "w", newline="") as f:
# 	writer = csv.writer(f)
# 	writer.writerow(Kmeanstimes)
# run_kmeans(k_means_outputs, samples, testmode=True)


# ---------- HIERARACHICAL TEST AREA ------------------
# hierarchical_outputs = 6
# samples = 1000
# Htimes = []
# for i in range(5):
#     Htimes.append(run_hierarch(hierarchical_outputs, samples, testmode=True))
# with open("HC_time_log.csv", "w", newline="") as f:
# 	writer = csv.writer(f)
# 	writer.writerow(Htimes)
# run_hierarch(hierarchical_outputs, samples, testmode=True)

