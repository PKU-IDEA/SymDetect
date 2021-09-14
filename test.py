import time
import numpy as np
import networkx as nx
import torch

from sklearn.metrics import f1_score, recall_score, precision_score

from util.dataloader import *

import graphsage.model as sage
import s3det.s3det as s3det
from graphsage.plot_confusion_matrix import plot_confusion_matrix

def filter_exact_the_same(G, p0, p1):
    tol = 1.0
    pred = np.zeros(len(p0))
    for i in range(len(p0)):
        g1, g2 = s3det.subgraph_extract(G, str(p0[i]), str(p1[i]))
        if s3det.graph_sim(g1, g2, tol):
            pred[i] = 1 
        else:
            pred[i] = 0
    return pred

def type_rule2(type1, type2):
    types1 = ['pfet', 'pfet_lvt', 'pmos', 'PMOS']
    types2 = ['nfet', 'nfet_lvt', 'nmos', 'NMOS']
    if type1 in types1:
        return type2 in types1
    if type1 in types2:
        return type2 in types2
    return 0

def filter_size_type_elec_rule(G, p0, p1):
    pred = np.zeros(len(p0))
    for i in range(len(p0)):
        type1, type2 = G.nodes[p0[i]]['device'], G.nodes[p1[i]]['device']
        w1, l1 = G.nodes[p0[i]]['w'], G.nodes[p0[i]]['l']
        w2, l2 = G.nodes[p1[i]]['w'], G.nodes[p1[i]]['l']
        elec1, elec2 = G.nodes[p0[i]]['elec'], G.nodes[p1[i]]['elec']
        if type_rule2(type1, type2) and float(w1) == float(w2) and float(l1) == float(l2) and elec1 == elec2:
            pred[i] = 1
        else:
            pred[i] = 0
    return pred

def pair_bipartite_match(G, prob, test_pair1, test_pair2):
    pair_gid = []
    testset = []
    pred = np.zeros(len(prob))

    for i in range(len(test_pair1)):
        p_gid = G.nodes[test_pair1[i]]['graph']
        pair_gid.append(p_gid)
        if p_gid not in testset:
            testset.append(p_gid)
    
    for gid in testset:
        pair_prob = []
        node_set = []
        for i in range(len(pair_gid)):
            if pair_gid[i] == gid:
                pair_prob.append((test_pair1[i], test_pair2[i], prob[i], i))
        pair_prob = sorted(pair_prob, key=lambda x:x[2], reverse=True)
        for i in range(len(pair_prob)):
            if pair_prob[i][0] not in node_set and pair_prob[i][1] not in node_set:
                if pair_prob[i][2] >= 0.5:
                    node_set.append(pair_prob[i][0])
                    node_set.append(pair_prob[i][1])
                    pred[pair_prob[i][3]] = 1
    return pred

def test_sage(G, model, testset, test_pair1, test_pair2, test_label):
    #G = nx.read_gpickle('data/graph.pkl')
    
    if len(testset) < 100000:
        test_output = torch.sigmoid(model.forward(test_pair1, test_pair2))
        #pred = np.where(test_output.data.numpy() < 0.5, 0, 1)
        filt = filter_size_type_elec_rule(G, test_pair1, test_pair2)
        pred = np.where(pred < filt, pred, filt)
        pred = pair_bipartite_match(G, pred, test_pair1, test_pair2)
        '''for j in range(pred.size):
            if pred[j] == 1 and test_label[j] == 0:
                #print(G.nodes[test_pair1[j]]['name'], G.nodes[test_pair2[j]]['name'])
                f = open('falsealarm.txt', 'a')
                f.write(G.nodes[test_pair1[j]]['name']+' '+G.nodes[test_pair2[j]]['name']+'\n')
                f.close()'''

    else:
        chunk_size = 5120
        pred = []
        for j in range(len(testset)//chunk_size):
            if j < (len(test)//chunk_size-1):
                pair1 = test_pair1[j*chunk_size:(j+1)*chunk_size]
                pair2 = test_pair2[j*chunk_size:(j+1)*chunk_size]
            else:
                pair1 = test_pair1[j*chunk_size:len(test_pair1)]
                pair2 = test_pair2[j*chunk_size:len(test_pair2)]
            test_output = torch.sigmoid(model.forward(pair1, pair2))
            pred_chunk = np.where(test_output.data.numpy() < 0.5, 0, 1)
            filt_chunk = filter_size_type_elec_rule(G, pair1, pair2)
            pred_chunk = np.where(pred_chunk < filt_chunk, pred_chunk, filt_chunk)
            pred = np.concatenate((pred, pred_chunk), axis=None)
            print("Inference on the {}-th chunk".format(j))

    print("True Positive Rate:", recall_score(np.asarray(test_label), pred, average="micro", labels=[1]))
    print("False Positive Rate:", 1-recall_score(np.asarray(test_label), pred, average="micro", labels=[0]))
    plot_confusion_matrix(np.asarray(test_label), pred, np.array([0, 1]), title='Confusion Matrix, without normalization')

if __name__ == '__main__':
    assert len(sys.argv) >= 2, "expected input data directory" 

    print("read data dir:", sys.argv[1])
    dataX, dataY = parse_all(sys.argv[1]) 
    feats, G, all_pairs  = prepare_data(dataX, dataY)

    start_time = time.time()
    #graphsage, testset, test_pair1, test_pair2, test_label = sage.train()
    graphsage, testset, test_pair1, test_pair2, test_label = sage.train(feats, G, all_pairs)
    end_time = time.time()
    print(end_time-start_time)
    start_time1 = time.time()
    test_sage(G, graphsage, testset, test_pair1, test_pair2, test_label)
    end_time1 = time.time()
    print(end_time1-start_time1)
