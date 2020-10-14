import numpy as  np
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from scipy.stats import ks_2samp
import math

from s3det.readckts import *
from s3det.plot_confusion_matrix import *

def subgraph_extract(g, v1, v2):
    """ extract subgraph for device pair
    """
    thres_min = 4
    thres_max = 8
    rad = math.ceil(nx.shortest_path_length(g, source=v1, target=v2) / 2)
    rad = max(rad, thres_min)
    rad = min(rad, thres_max)
    
    nodes1 = list(nx.single_source_shortest_path_length(g, v1, cutoff=rad).keys())
    nodes2 = list(nx.single_source_shortest_path_length(g, v2, cutoff=rad).keys())
    
    g1 = g.subgraph(nodes1)
    g2 = g.subgraph(nodes2)
    return g1, g2

def graph_sim(g1, g2, tol):
    """ determine subgraph similarity
    """
    spec1 = nx.laplacian_spectrum(g1)
    spec2 = nx.laplacian_spectrum(g2)
    D, p_val = ks_2samp(spec1, spec2)
    return p_val >= tol

def s3det(tol):
    filename = '../data/data.pkl'
    G, all_pairs, labels = readckts(filename)

    y_trues = []
    y_preds = []
    for i in range(len(G)):
        g = G[i]
        node_pair = all_pairs[i]
        label = labels[i]
        y_true = []
        y_pred = []

        for pair in node_pair:
            g1, g2 = subgraph_extract(g, pair[0], pair[1])
            if [pair[0], pair[1]] in label or [pair[1], pair[0]] in label:
                y_true.append(1)
            else:
                y_true.append(0)
            if graph_sim(g1, g2, tol):
                y_pred.append(1)
            else:
                y_pred.append(0)

        cm = confusion_matrix(np.array(y_true), np.array(y_pred))
        print('subckt', i)
        print(cm)
        if len(cm)>1:
            print('fpr:', cm[0][1]/(cm[0][0]+cm[0][1]), 'tpr:', cm[1][1]/(cm[1][0]+cm[1][1]))
        y_trues.extend(y_true)
        y_preds.extend(y_pred)

    plot_confusion_matrix(np.array(y_trues), np.array(y_preds), np.array([0, 1]), title='S3DET confusion matrix')

if __name__ == '__main__':
    s3det()
