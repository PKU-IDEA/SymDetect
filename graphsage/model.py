import torch
import torch.nn as nn
from torch.nn import init
from torch.autograd import Variable
import os

import numpy as np
import time
import random
import math
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from collections import defaultdict

from graphsage.encoders import Encoder
from graphsage.aggregators import MeanAggregator
from graphsage.plot_confusion_matrix import plot_confusion_matrix

"""
Simple supervised GraphSAGE model for directed graph as well as examples running the model
on the EDA datasets.
"""

class SupervisedGraphSage(nn.Module):

    def __init__(self, num_classes, enc):
        super(SupervisedGraphSage, self).__init__()
        self.enc = enc
        #self.xent = nn.BCEWithLogitsLoss(pos_weight=torch.tensor([0.1]))
        self.xent = nn.BCEWithLogitsLoss()
      # pos_weight controls weight of "1" label in loss function

        self.weight = nn.Parameter(torch.FloatTensor(enc.embed_dim, enc.embed_dim))
        init.xavier_uniform_(self.weight)

    def forward(self, pair1, pair2):
        embed1 = (self.enc(pair1)).t()
        embed2 = (self.enc(pair2))
        #print(embed1.data, embed2.data)

        scores = torch.diag(torch.mm(embed1, self.weight.mm(embed2)))
        return scores

    def loss(self, pair1, pair2, labels):
        scores = self.forward(pair1, pair2)
        return self.xent(scores, labels)

'''def load_cora(feats, G, all_pairs):
    data_dir = "data"
    feat_data = np.load("{}/feats.npy".format(data_dir))
    feat_data = feats
    num_nodes = feat_data.shape[0]
    #labels = np.empty((num_nodes,1), dtype=np.int64)
    train = []
    test  = []
    train_label = []
    test_label = []
    with open("{}/labels.txt".format(data_dir)) as fp:
        for i,line in enumerate(fp):
            info = line.strip().split()
            #labels.append(int(info[2]))
            if int(info[3]) == 1:
                train.append([int(info[0]), int(info[1])])
                train_label.append(int(info[2]))
            else:
                test.append([int(info[0]), int(info[1])])
                test_label.append(int(info[2]))

    adj_lists = defaultdict(lambda: defaultdict(set))
    with open("{}/all.edgelist".format(data_dir)) as fp:
        for i,line in enumerate(fp):
            info = line.strip().split()
            paper1 = int(info[0])
            paper2 = int(info[1])
            adj_lists[paper1]["out"].add(paper2)
            adj_lists[paper2]["in"].add(paper1)
    return feat_data, train_label, test_label, adj_lists, train, test'''

def load_cora(feats, G, all_pairs):
    feat_data = feats
    num_nodes = feat_data.shape[0]
    train = []
    test = []
    train_label = []
    test_label = []
    for pair in all_pairs:
        if pair[3] == 1:
            train.append([pair[0], pair[1]])
            train_label.append(pair[2])
        else:
            test.append([pair[0], pair[1]])
            test_label.append(pair[2])

    adj_lists = defaultdict(lambda: defaultdict(set))
    for pair in list(G.edges()):
        adj_lists[pair[0]]["out"].add(pair[1])
        adj_lists[pair[1]]["in"].add(pair[0])

    return feat_data, train_label, test_label, adj_lists, train, test

def shuffle_list(*ls):
    l =list(zip(*ls))
    random.seed(1234)
    random.shuffle(l)
    return zip(*l)

def train(feats, G, all_pairs):
    np.random.seed(1)
    random.seed(1)
    feat_data, train_label, test_label, adj_lists, train, test = load_cora(feats, G, all_pairs)
    num_nodes = feat_data.shape[0]
    feat_dim = feat_data.shape[1]
    hidden_dim = 15
    features = nn.Embedding(num_nodes, feat_dim)
    features.weight = nn.Parameter(torch.FloatTensor(feat_data), requires_grad=False)
    #features.cuda()

    agg1 = MeanAggregator(features, cuda=False)
    enc1 = Encoder(features, feat_dim, hidden_dim, adj_lists, agg1, gcn=False, cuda=False)
    agg2 = MeanAggregator(lambda nodes : enc1(nodes).t(), cuda=False)
    enc2 = Encoder(lambda nodes : enc1(nodes).t(), enc1.embed_dim, hidden_dim, adj_lists, agg2,
            base_model=enc1, gcn=False, cuda=False)
    agg3 = MeanAggregator(lambda nodes : enc2(nodes).t(), cuda=False)
    enc3 = Encoder(lambda nodes : enc2(nodes).t(), enc2.embed_dim, hidden_dim, adj_lists, agg3,
            base_model=enc2, gcn=False, cuda=False)
    agg4 = MeanAggregator(lambda nodes : enc3(nodes).t(), cuda=False)
    enc4 = Encoder(lambda nodes : enc3(nodes).t(), enc3.embed_dim, hidden_dim, adj_lists, agg4,
            base_model=enc3, gcn=False, cuda=False)
    enc1.num_samples = 15
    enc2.num_samples = 15
    enc3.num_samples = 15
    enc4.num_samples = 15

    graphsage = SupervisedGraphSage(hidden_dim, enc3)
    #graphsage.cuda()

    optimizer = torch.optim.Adam(filter(lambda p : p.requires_grad, graphsage.parameters()), lr=0.001, weight_decay=1e-5)
    times = []
    epoch = 500
    batch_size = 256
    num_batch = math.ceil(len(train)/batch_size)
    best = 1e9
    cnt_wait = 0
    patience = 100
    best_epoch = 0
    best_batch = 0

    train_pair1 = []
    train_pair2 = []
    test_pair1 = []
    test_pair2 = []
    for x in train:
        train_pair1.append(x[0])
        train_pair2.append(x[1])
    for x in test:
        test_pair1.append(x[0])
        test_pair2.append(x[1])
    # shuffle training set
    fused_train = [list(x) for x in shuffle_list(train_pair1,train_pair2,train_label)]
    train_pair1 = fused_train[0]
    train_pair2 = fused_train[1]
    train_label = fused_train[2]
    for e in range(epoch):
        for i in range(num_batch):
            if i < num_batch - 1:
                pair1 = train_pair1[i*batch_size: i*batch_size + batch_size]
                pair2 = train_pair2[i*batch_size: i*batch_size + batch_size]
                sub_label = train_label[i*batch_size: i*batch_size + batch_size]
            else:
                pair1 = train_pair1[i*batch_size: len(train_pair1)]
                pair2 = train_pair2[i*batch_size: len(train_pair2)]
                sub_label = train_label[i*batch_size: len(train_pair1)]
            start_time = time.time()
            optimizer.zero_grad()
            loss = graphsage.loss(pair1, pair2,\
                Variable(torch.FloatTensor(np.asarray(sub_label))))

            
            if loss < best:
                best = loss
                best_epoch = e
                best_batch = i
                cnt_wait = 0
                torch.save(graphsage.state_dict(), 'best_model.pkl')
            else:
                cnt_wait += 1
            

            loss.backward()
            optimizer.step()
            end_time = time.time()
            times.append(end_time-start_time)
            print("The {}-th epoch, The {}-th batch, ".format(e, i), "Loss: ", loss.item())
        if cnt_wait == patience:
            print('Early stoppping!')
            break

    print('Loading {}th epoch {}th batch'.format(best_epoch, best_batch))
    graphsage.load_state_dict(torch.load('best_model.pkl'))

    return graphsage, test, test_pair1, test_pair2, test_label

