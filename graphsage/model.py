from cProfile import label
import torch
import torch.nn as nn
import torch.nn.functional as F
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
from graphsage.GNN import GNN

from test_hw import filter_size_type_elec_rule, pair_bipartite_match
import matplotlib.pyplot as plt
"""
Simple supervised GraphSAGE model for directed graph as well as examples running the model
on the EDA datasets.
"""

class SupervisedGraphSage(nn.Module):

    def __init__(self, enc):
        super(SupervisedGraphSage, self).__init__()
        self.enc = enc
        self.xent = nn.BCEWithLogitsLoss()

        # self.weight = nn.Parameter(torch.FloatTensor(enc.embed_dim, enc.embed_dim))
        # init.xavier_uniform_(self.weight)
    def reset_parameters(self):
        self.enc.reset_parameters()
        init.xavier_uniform_(self.weight)
    def forward(self, features, adj_lists, pair1, pair2):
        embed=self.enc(features,adj_lists)
        embed=embed.to('cpu')
        embed1=embed[pair1]
        # embed2=embed[pair2].t()
        embed2=embed[pair2]
        # embed1 = (self.enc(pair1)).t()
        # embed2 = (self.enc(pair2))
        #print(embed1.data, embed2.data)

        # scores = torch.diag(torch.mm(embed1, self.weight.mm(embed2)))
        # scores = torch.sigmoid(scores)
        scores = F.cosine_similarity(embed1,embed2)
        return scores

    def loss(self, features, adj_lists,  pair1, pair2, labels):
        scores = self.forward(features, adj_lists, pair1, pair2)
        return self.xent(scores, labels)

def load_cora(feats, G, all_pairs):
    feat_data = feats
    num_nodes = feat_data.shape[0]
    train = []
    test = []
    valid = []
    train_label = []
    test_label = []
    valid_label = []
    for pair in all_pairs:
        if pair[3] == 1:
            train.append([pair[0], pair[1]])
            train_label.append(pair[2])
        elif pair[3] == 0:
            test.append([pair[0], pair[1]])
            test_label.append(pair[2])
        else:
            valid.append([pair[0], pair[1]])
            valid_label.append(pair[2])

    adj_lists=[]
    for edge in G.edges():
        adj_lists.append(edge)
        adj_lists.append([edge[1],edge[0]])
    adj_lists=torch.LongTensor(adj_lists).T
    # adj_lists = defaultdict(lambda: defaultdict(set))
    # for pair in list(G.edges()):
    #     adj_lists[pair[0]]["out"].add(pair[1])
    #     adj_lists[pair[1]]["in"].add(pair[0])

    return feat_data, train_label, test_label, valid_label, adj_lists, train, test, valid

def shuffle_list(*ls):
    l =list(zip(*ls))
    random.seed(1234)
    random.shuffle(l)
    return zip(*l)

def train(feats, G, all_pairs, tflag, pmos_types, nmos_types):
    np.random.seed(1)
    random.seed(1)
    feat_data, train_label, test_label, valid_label, adj_lists, train, test, valid = load_cora(feats, G, all_pairs)
    num_nodes = feat_data.shape[0]
    feat_dim = feat_data.shape[1]
    hidden_dim = 8
    features=torch.Tensor(feat_data)
    train_label=torch.Tensor(train_label)

    # device = 'cuda' if torch.cuda.is_available() else 'cpu'
    # features = features.to(device)
    # adj_lists = adj_lists.to(device)
    # train_label = train_label.to(device)
    
    epoch = 500
    if tflag:
        epoch = 0
    batch_size = 256
    num_batch = math.ceil(len(train)/batch_size)
    # best = 0
    best_train_loss = 1e9
    cnt_wait = 0
    patience = 100
    best_epoch = 0
    best_batch = 0

    train_loss_record=[]
    train_acc_record=[]
    val_loss_record=[]
    val_acc_record=[]

    train_pair1 = []
    train_pair2 = []
    test_pair1 = []
    test_pair2 = []
    valid_pair1 = []
    valid_pair2 = []
    for x in train:
        train_pair1.append(x[0])
        train_pair2.append(x[1])
    for x in test:
        test_pair1.append(x[0])
        test_pair2.append(x[1])
    for x in valid:
        valid_pair1.append(x[0])
        valid_pair2.append(x[1])
    # shuffle training set
    # fused_train = [list(x) for x in shuffle_list(train_pair1,train_pair2,train_label)]
    # train_pair1 = fused_train[0]
    # train_pair2 = fused_train[1]
    # train_label = fused_train[2]

    enc=GNN(feat_dim,hidden_dim,hidden_dim,3,0.2)
    graphsage = SupervisedGraphSage(enc)
    # graphsage.reset_parameters()
    criterion=nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(filter(lambda p : p.requires_grad, graphsage.parameters()), lr=0.001, weight_decay=1e-5)
    

    for e in range(epoch):
        graphsage.train()
        train_acc = 0.0
        train_loss = 0.0
        val_acc = 0.0
        val_loss = 0.0
        for i in range(num_batch):
            if i < num_batch - 1:
                pair1 = train_pair1[i*batch_size: i*batch_size + batch_size]
                pair2 = train_pair2[i*batch_size: i*batch_size + batch_size]
                sub_label = train_label[i*batch_size: i*batch_size + batch_size]
            else:
                pair1 = train_pair1[i*batch_size: len(train_pair1)]
                pair2 = train_pair2[i*batch_size: len(train_pair2)]
                sub_label = train_label[i*batch_size: len(train_pair1)]

            optimizer.zero_grad()
            output=graphsage(features, adj_lists, pair1, pair2)
            # loss=graphsage.loss(features, adj_lists, pair1, pair2,\
            #     Variable(torch.FloatTensor(np.asarray(sub_label))))
            loss=criterion(output,sub_label)
            loss.backward()
            optimizer.step()
            
            pred = output.data.numpy()
            filt = filter_size_type_elec_rule(G, pair1, pair2, pmos_types, nmos_types)
            pred = np.where(pred < filt, pred, filt)
            # pred = torch.where(output < 0.5, 0, 1)
            pred = pair_bipartite_match(G, pred, pair1, pair2)
            train_acc+=f1_score(sub_label, pred)
            train_loss+=loss.item()           

        # test loss
        train_loss/=num_batch
        train_acc/=num_batch
        train_loss_record+=[train_loss]
        train_acc_record+=[train_acc]
        
        graphsage.eval()
        output = graphsage(features, adj_lists, valid_pair1, valid_pair2)
        val_loss=criterion(output,Variable(torch.FloatTensor(np.asarray(valid_label))))
        pred = output.data.numpy()
        filt = filter_size_type_elec_rule(G, valid_pair1, valid_pair2, pmos_types, nmos_types)
        pred = np.where(pred < filt, pred, filt)
        # pred = np.where(pred < 0.5, 0, 1)
        pred = pair_bipartite_match(G, pred, valid_pair1, valid_pair2)
        val_acc=f1_score(np.asarray(valid_label), pred)
        val_loss_record+=[val_loss]
        val_acc_record+=[val_acc]

        print('[{:03d}/{:03d}] Train Acc: {:3.6f} Loss: {:3.6f} | Val Acc: {:3.6f} loss: {:3.6f}'.format(
                e, epoch, train_acc, train_loss, val_acc, val_loss ))

        # if val_acc > best:
        #     best = val_acc
        if train_loss < best_train_loss:
            best_epoch = e
            best_train_loss = train_loss
            best_train_acc = train_acc
            best_valid_loss = val_loss
            best_valid_acc = val_acc
            # best_batch = i
            cnt_wait = 0
            torch.save(graphsage.state_dict(), 'best_model.pkl')
        else:
            cnt_wait += 1
                     
        if cnt_wait == patience or val_acc==1:
            print('Early stoppping!')
            break

    print('Loading {}th epoch'.format(best_epoch))
    print('[{:03d}/{:03d}] Train Acc: {:3.6f} Loss: {:3.6f} | Val Acc: {:3.6f} loss: {:3.6f}'.format(
        best_epoch, epoch, best_train_acc, best_train_loss, best_valid_acc, best_valid_loss ))
    with open("log", "a") as f:       
        f.write('[{:03d}/{:03d}] Train Acc: {:3.6f} Loss: {:3.6f} | Val Acc: {:3.6f} loss: {:3.6f}'.format(
        best_epoch, epoch, best_train_acc, best_train_loss, best_valid_acc, best_valid_loss ))

    graphsage.load_state_dict(torch.load('best_model.pkl'))
    plt.subplot(2,1,1)
    plt.plot(train_loss_record, label='train')
    plt.plot(val_loss_record, label='val')
    plt.legend()
    plt.title("loss")

    plt.subplot(2,1,2)
    plt.plot(train_acc_record, label='train')
    plt.plot(val_acc_record, label='val')
    plt.title("score")
    plt.legend()
    plt.savefig("loss-score-pyg")
    return graphsage, test, test_pair1, test_pair2, test_label, features, adj_lists

