import os
import sys

import json
import time

import numpy as np
import networkx as nx
import torch

from sklearn.metrics import f1_score, recall_score, precision_score

from util.message import info
from util.parser import *
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

def test_sage(G, model, testset, test_pair1, test_pair2, test_label, resultfile, lflag):
    #G = nx.read_gpickle('data/graph.pkl')
    
    if len(testset) < 100000:
        test_output = torch.sigmoid(model.forward(test_pair1, test_pair2))
        #pred = np.where(test_output.data.numpy() < 0.5, 0, 1)
        pred = test_output.data.numpy()
        filt = filter_size_type_elec_rule(G, test_pair1, test_pair2)
        pred = np.where(pred < filt, pred, filt)
        pred = pair_bipartite_match(G, pred, test_pair1, test_pair2)
        '''for j in range(pred.size):
            if pred[j] == 1 and test_label[j] == 0:
                #print(G.nodes[test_pair1[j]]['name'], G.nodes[test_pair2[j]]['name'])
                f = open('falsealarm.txt', 'a')
                f.write(G.nodes[test_pair1[j]]['name']+' '+G.nodes[test_pair2[j]]['name']+'\n')
                f.close()'''
        with open(resultfile, "w") as f:
            for j in range(pred.size):
                if pred[j] == 1:
                    f.write(G.nodes[test_pair1[j]]['name']+' '+G.nodes[test_pair2[j]]['name']+'\n')

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

    if lflag:
        return

    print("True Positive Rate:", recall_score(np.asarray(test_label), pred, average="micro", labels=[1]))
    print("False Positive Rate:", 1-recall_score(np.asarray(test_label), pred, average="micro", labels=[0]))
    plot_confusion_matrix(np.asarray(test_label), pred, np.array([0, 1]), title='Confusion Matrix, without normalization')

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

class Model():
    def __init__(self, config):
        self.config = config
        self.datadir = config["dataset"]
        self.resultfile = config["result"]

        self.trainlist = config["trainset"]
        self.testlist = config["testset"]
        
        self.istrain = "train" in config["mode"]
        self.istest = "test" in config["mode"]
        self.labelflag = "nolabel" in config["mode"]
        self.savemodel = config["savemodel"]

        self.nmoslist = config["nmos"]
        self.pmoslist = config["pmos"]
        self.moslist = self.nmoslist + self.pmoslist
        self.wlist = config["w"]
        self.nflist = config["nf"]
        self.llist = config["l"]

        self.caplist = config["cap"]
        self.reslist = config["res"]
        self.bjtlist = config["bjt"]
        self.xilist = config["xi"]
        pass

    def preprocess(self):
        info('i', "Start Parsing Dataset...")

        dataX, dataY, netlists = parse_all(self.datadir, self.moslist, 
                self.caplist, self.reslist, self.bjtlist, self.xilist) 
        
        netlists = [os.path.basename(netlist) for netlist in netlists]
        self.trainset = []
        self.testset = []
        for i in range(len(dataX)):
            data = dataX[i]
            if data["subckts"][0].name in self.trainlist:
                self.trainset.append(i)
            elif data["subckts"][0].name in self.testlist:
                self.testset.append(i)

        feats, G, all_pairs  = prepare_data(dataX, dataY, 
                self.moslist, self.pmoslist, self.nmoslist,
                self.wlist, self.nflist, self.llist, 
                self.caplist, self.reslist, self.bjtlist, self.xilist, self.trainset)
        
        self.dataX = dataX
        self.dataY = dataY
        self.feats = feats
        self.G = G
        self.all_pairs = all_pairs
        pass

    def trainntest(self):
        self.tflag = False
        if self.istrain and self.istest:
            self.tflag = False
        elif self.istrain:
            self.tflag = False
        elif self.istest:
            self.tflag = True
        else:
            info('e', "Mode NOT Supported")

        self.train()
        if self.istest:
            self.test()

    def train(self):
        start_time = time.time()
        graphsage, testset, test_pair1, test_pair2, test_label = sage.train(self.feats, self.G, self.all_pairs, self.tflag)
        end_time = time.time()
        info('i', "Training time %f s" % (end_time - start_time))
        self.graphsage = graphsage
        self.testset = testset
        self.test_pair1 = test_pair1
        self.test_pair2 = test_pair2
        self.test_label = test_label
        pass

    def test(self):
        start_time = time.time()
        test_sage(self.G, self.graphsage, self.testset, self.test_pair1, self.test_pair2, self.test_label, self.resultfile, self.labelflag)
        end_time = time.time()
        info('i', "Inference time %f s" % (end_time - start_time))
        pass


if __name__=="__main__":
    config = None
    with open("config.json", "r") as f:
        config = json.load(f)
    info('i', "Load Config from %s" % "config.json")
    info('i', "Use Verbose %d Mode" % config["verbose"])
    info('i', "Use Dataset %s" % config["dataset"])

    model = Model(config)
    model.preprocess()
    model.trainntest()
