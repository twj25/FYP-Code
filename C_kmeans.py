import numpy as np
from sklearn.cluster import MiniBatchKMeans
import shutil

class Kmeans:

    def __init__(self, num_classes):
        self.num_classes = num_classes

    def load_evaluation_data(self,dataset):
        # K-means is an unsupervised learning technique, therefore:

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

    def cluster(self):
        kmeans = MiniBatchKMeans(n_clusters= self.num_classes)

        kmeans.fit(self.data)

        labels = kmeans.labels_
        result = self.comb_label_and_dir(labels)

        return result

    def comb_label_and_dir(self, labels):
        result = []
        for i in range(len(labels)):
            result.append([labels[i],self.directories[i]])

        return result

    def move_to_new_dir(self, labels):
        counter = 0
        new_dir_base = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Clustered/"
        for data in labels:
            cluster_label = data[0]
            file = data[1]
            old_dir = "C:/Users/Tom/OneDrive/Documents/50 University/Year 5/Individual Proj/Data/Unsorted/" + file

            if cluster_label == 0:
                new_dir = new_dir_base + "0/" + file
            elif cluster_label == 1:
                new_dir = new_dir_base + "1/" + file
            elif cluster_label == 2:
                new_dir = new_dir_base + "2/" + file
            elif cluster_label == 3:
                new_dir = new_dir_base + "3/" + file
            else:
                new_dir = new_dir_base + "4/" + file

            shutil.copy(old_dir,new_dir)
            print(counter)
            counter +=1
        return