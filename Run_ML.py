from import_training_data import import_all_training, import_all
from C_2D_CNN import CNN
from C_kmeans import Kmeans

def run_CNN(num_of_outputs, train_test_split, dropout_rate=0.5, num_of_filters=[64,128], num_of_dense_units=128, act_func='relu'):
    DR = dropout_rate
    NF = num_of_filters
    ND = num_of_dense_units
    AF = act_func
    NO = num_of_outputs

    # Import all training data and complete a sanity check on the split value.
    training_dataset = import_all_training("True")
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

    kmeans_ob = Kmeans(outputs)
    kmeans_ob.load_evaluation_data(data)
    labels = kmeans_ob.cluster()

    kmeans_ob.move_to_new_dir(labels)
    return

train_test_split = 180
cnn_outputs = 7
k_means_outputs = 5
samples = 1000

#acc, loss = run_CNN(cnn_outputs, train_test_split)
run_kmeans(k_means_outputs, samples)
x = 1

