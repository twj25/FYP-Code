from f_import_data import import_all_training
from f_plot_scatter import scatter_2D, scatter_3D
from matplotlib import pyplot as plt
import time
import pandas as pd
import numpy as np
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import seaborn as sns

def convert_data_format(dataset):
    # Input: List of list, each entry contains two elements: class & compressed image
    # Output: Two numpy arrays: compressed images (X_train) & classes (y_train)

    num_samples = len(dataset)
    X_train = []
    y_train = []
    for i in range(num_samples):
        X_train.append(dataset[i][1])
        y_train.append(dataset[i][0])

    y_train = np.array(y_train)
    X_train = np.array(X_train).reshape(len(X_train), -1)

    return X_train, y_train

def _tSNE(x_data,y_data):
    RS= 123
    time_start = time.time()
    fashion_tsne = TSNE(random_state=RS).fit_transform(x_data)
    print('t-SNE done! Time elapsed: {} seconds'.format(time.time()-time_start))
    scatter_2D(fashion_tsne, y_data)

    return

def _PCA(x_data, y_data):

    time_start = time.time()
    pca = PCA(n_components=4)
    pca_result = pca.fit_transform(x_subset)
    print('PCA done! Time elapsed: {} seconds'.format(time.time()-time_start))

    pca_df = pd.DataFrame(columns = ['pca1','pca2','pca3','pca4'])
    pca_df['pca1'] = pca_result[:,0]
    pca_df['pca2'] = pca_result[:,1]
    pca_df['pca3'] = pca_result[:,2]
    pca_df['pca4'] = pca_result[:,3]
    print('Variance explained per principal component: {}'.format(pca.explained_variance_ratio_))

    top_two_comp = pca_df[['pca1','pca2']] # taking first and second principal component
    scatter_2D(top_two_comp.values,y_data) # Visualizing the PCA output

    return

def _PCA_3D(x_data, y_data):

    time_start = time.time()
    pca = PCA(n_components=3)
    pca_result = pca.fit_transform(x_subset)
    print('PCA done! Time elapsed: {} seconds'.format(time.time()-time_start))

    pca_df = pd.DataFrame(columns = ['pca1','pca2','pca3'])
    pca_df['pca1'] = pca_result[:,0]
    pca_df['pca2'] = pca_result[:,1]
    pca_df['pca3'] = pca_result[:,2]

    top_three_comp = pca_df[['pca1','pca2','pca3']]
    scatter_3D(top_three_comp.values,y_data) # Visualizing the PCA output

    return

data_source = ["mcdonald","5577","2018","Jul"]
training_dataset = import_all_training(data_source)
x_subset, y_subset = convert_data_format(training_dataset)

#_tSNE(x_subset, y_subset)
_PCA(x_subset, y_subset)
#_PCA_3D(x_subset, y_subset)
