import numpy as np
from sklearn.cluster import MiniBatchKMeans

class Kmeans:

    def __init__(self, num_classes):
        self.num_classes = num_classes

    def load_evaluation_data(self,dataset):
        # K-means is an unsupervised learning technique, therefore:

            # spliting into training and testing is unneccessary
            # spliting into x & y is uneccessary

        self.preprocess_data(dataset)
        return

    def preprocess_data(self,data):
        # Must flatten data + normalise between 0 - 1
        data = np.array(data)
        data = data.reshape(len(data),-1)
        self.data = data.astype(float)/255
        return

    def cluster(self):
        kmeans = MiniBatchKMeans(n_clusters= self.num_classes)

        kmeans.fit(self.data)

        kmeans.labels_

        return