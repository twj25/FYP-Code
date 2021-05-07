from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as PathEffects
import numpy as np
import seaborn as sns

sns.set_style('darkgrid')
sns.set_palette('muted')
sns.set_context("notebook", font_scale=1.5,
                rc={"lines.linewidth": 2.5})

def scatter_2D(x, colors, x_label = "N/A", y_label = "N/A"):
    # choose a color palette with seaborn.
    num_classes = len(np.unique(colors))
    palette = np.array(sns.color_palette("hls", num_classes))

    # create a scatter plot.
    f = plt.figure(figsize=(8, 8))
    ax = plt.subplot(aspect='equal')
    sc = ax.scatter(x[:,0], x[:,1], lw=0, s=40, c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    #ax.axis('off')
    ax.axis('tight')
    if x_label != "N/A":
        plt.xlabel(x_label)
        plt.ylabel(y_label)
    

    # add the labels for each digit corresponding to the label
    txts = []
    txt_labels = ['Moon', 'Moon_Exposure', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear', 'Speckle']

    for i in range(num_classes):

        # Position of each label at median of data points.

        xtext, ytext = np.median(x[colors == i, :], axis=0)
        txt = ax.text(xtext, ytext, txt_labels[i], fontsize=18)
        txt.set_path_effects([
            PathEffects.Stroke(linewidth=5, foreground="w"),
            PathEffects.Normal()])
        txts.append(txt)

    custom_legend = [ Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[0], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[1], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[2], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[3], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[4], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[5], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[6], markersize=15)]

    legend = ax.legend(custom_legend, txt_labels, loc="upper left", title="Classes")
    plt.show()
    return f, ax, sc, txts

def scatter_3D(x, colors):
    # choose a color palette with seaborn.
    num_classes = len(np.unique(colors))
    palette = np.array(sns.color_palette("hls", num_classes))

    # create a scatter plot.
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x[:,0], x[:,1], x[:,2], lw=0, s=40, c=palette[colors.astype(np.int)])
    plt.xlim(-25, 25)
    plt.ylim(-25, 25)
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.set_zlabel('PC3')
    ax.axis('tight')
    
    txt_labels = ['Moon', 'Moon_Exposure', 'V_Cloudy', 'Cloudy', 'Almost_Clear', 'Clear', 'Speckle']

    custom_legend = [ Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[0], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[1], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[2], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[3], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[4], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[5], markersize=15),
                      Line2D([0], [0], marker='o', color='w', label='Scatter', markerfacecolor=palette[6], markersize=15)]

    legend = ax.legend(custom_legend, txt_labels, loc="upper left", title="Classes")
    plt.show()
    return