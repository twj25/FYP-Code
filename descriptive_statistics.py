from import_training_data import import_all_training
from plot_scatter import scatter_2D
import numpy as np

def calc_statistics(data):
    statistic_list = []
    labels = []
    for entry in data:
        mean = entry[1].mean()
        median = np.median(entry[1])
        
        statistic_list.append([mean,median])
        labels.append(entry[0])

    return statistic_list,labels

training_dataset = import_all_training()
stat_list,labels = calc_statistics(training_dataset)
stat_array = np.array(stat_list)
label_array = np.array(labels)


scatter_2D(stat_array,label_array, "Mean", "Median")
x = 1