import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering

class Hierarchical:

    def __init__(self, num_classes):
        self.num_classes = num_classes

    def load_evaluation_data(self,dataset):
        # Hierarachical clustering is an unsupervised learning technique, therefore:

            # spliting into training and testing is unneccessary
            # spliting into x & y is uneccessary
        img_data = [data[1] for data in dataset]
        self.directories = [data[0] for data in dataset]
        self.preprocess_data(img_data)
        return

    def preprocess_data(self,data):
        # Must flatten data + normalise between 0 - 1
        data = np.array(data)
        data = data.reshape(len(data),-1)
        self.data = data.astype(float)/255
        return

    def draw_dendrogram(self):
        plt.figure(figsize=(10, 7))
        plt.title("Airglow")
        dend = shc.dendrogram(shc.linkage(self.data, method='ward'))
        plt.show()
        return

    def cluster(self):
        cluster = AgglomerativeClustering(n_clusters=self.num_classes)
        cluster.fit_predict(self.data)
        labels = cluster.labels_
        result = self.comb_label_and_dir(labels)

        return result

    def comb_label_and_dir(self, labels):
        result = []
        for i in range(len(labels)):
            result.append([labels[i],self.directories[i]])

        return result
