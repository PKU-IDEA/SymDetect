# -*- coding: utf-8 -*-

import os 
import sys
import pdb
import random

from itertools import combinations
from collections import OrderedDict

import numpy as np
import networkx as nx

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
#from sklearn.model_selection import train_test_split

from util.netlist import *
from util.filter import *

def draw_graph(graph, labels, colours):
    colours_map = []
    for node in graph:
        flag = False
        for i in range(len(colours)):
            if node in colours[i]:
                colours_map.append(10*i+10)
                flag = True
        if flag == False:
            colours_map.append(10*len(colours)+10)

    pos = nx.nx_pydot.graphviz_layout(graph, prog="dot")
    options = {'arrowstyle' : '-|>', 'arrowsize' : 12}
    nx.draw(graph, font_weight='bold', pos=pos, node_color=colours_map, **options, cmap=plt.cm.Blues)
    nx.draw_networkx_labels(graph, pos, labels, font_size=16)
    plt.savefig("graph.pdf", dpi=120)
    return

def prepare_data(dataX, dataY, moslist, pmoslist, nmoslist, wlist, 
        nflist, llist, caplist, reslist, bjtlist, xilist, multilist, trainset=[], testset=[]):
    G = nx.Graph() # the graph of all circuits
    num_nodes = 0 # used to merge subgraphs by changing node indices
    all_pairs = [] # store all pos and neg node pairs
    
    node_attr = {} # ?
    node_types = [] # store types of all nodes
    node_is_pin = [] # ? judge pin
    node_potential = [] # store symbolic electricity potential of all pins
    # ratio_sample = 0.7 # #training_samples/#total_samples
    #trainset = [0, 7, 3, 1, 2]
    print("trainset", trainset)

    valid_pair_num = 0
    neg_pair_num = 0
    for i in range(len(dataX)):
        sub_G = nx.Graph() # graph of one single circuit
        is_train = i in trainset
        subckts = dataX[i]["subckts"] # raw subcircuits read from spice netlist
        graph = dataX[i]["graph"] # raw hypergraph
        label = dataY[i] # symmetry pairs of node indices, self-symmetry if a pair only has one element
        pin_map = {} # map pins to node id
        print("process circuit:", i, subckts[0].name)

        # graph -> G
        for g in graph.nodes:
            # node type
            node_attr[g.id+num_nodes] = type_filter_mos(g.attributes["cell"], pmoslist, nmoslist, caplist, reslist, bjtlist, xilist)
            node_types.append(type_filter_mos(g.attributes["cell"], pmoslist, nmoslist, caplist, reslist, bjtlist, xilist))
            node_is_pin.append(np.array([0]))
            
            # add node
            G.add_node(g.id+num_nodes)
            sub_G.add_node(g.id+num_nodes)
            G.nodes[g.id+num_nodes]["name"] = g.attributes["name"]
            G.nodes[g.id+num_nodes]["graph"] = i # which subgraph the node belongs to
            G.nodes[g.id+num_nodes]["device"] = node_attr[g.id+num_nodes]
            
            if g.attributes["cell"] == "IO":
                G.nodes[g.id+num_nodes]["type"] = "IO"
                # sub_G.nodes[g.id+num_nodes]["type"] = "IO"
            else:
                G.nodes[g.id+num_nodes]["type"] = "device"
                # sub_G.nodes[g.id+num_nodes]["type"] = "device"
            #if g.attributes["cell"] in ["pmos", "pfet", "pfet_lvt", "PMOS", "nmos", "nfet", "nfet_lvt", "NMOS"] or "xm" in g.attributes["cell"]:
            if g.attributes["cell"] in moslist:
                w, nf = -1, 1
                for wname in wlist:
                    if wname in g.attributes:
                        w = convert_length(g.attributes[wname])
                        break
                for nfname in nflist:
                    if nfname in g.attributes:
                        nf = int(g.attributes[nfname])
                        break
                #G.nodes[g.id+num_nodes]['w'] = w / nf 
                G.nodes[g.id+num_nodes]['w'] = w * nf
                #G.nodes[g.id+num_nodes]['l'] = convert_length(g.attributes['l'])
                l = -1
                for lname in llist:
                    if lname in g.attributes:
                        l = convert_length(g.attributes[lname])
                        break
                G.nodes[g.id+num_nodes]['l'] = l
                # G.nodes[g.id+num_nodes]["device"] = g.attributes["cell"]
            else:
                G.nodes[g.id+num_nodes]['w'] = -1
                G.nodes[g.id+num_nodes]['l'] = -1
                # G.nodes[g.id+num_nodes]["device"] = "-1"
            
            # attribute: multi
            for multiname in multilist:
                if multiname in g.attributes.keys():
                    G.nodes[g.id+num_nodes]['multi'] = g.attributes[multiname]

        # determine pairs for training
        node_pairs = list(combinations(list(sub_G.nodes()), 2)) # all possible node pairs
        random.seed(1)
        random.shuffle(node_pairs)
        neg_pairs = []
        neg_size = 2 # the ratio of #neg_pairs/#pos_pairs
        for pair in node_pairs:
            # skip pos pairs 
            if [pair[0]-num_nodes, pair[1]-num_nodes] in label or [pair[1]-num_nodes, pair[0]-num_nodes] in label:
                continue
            # ignore devices not mos 
            #if not type_filter_pnmos(type1, type2):
            #    continue
            type1, type2 = G.nodes[pair[0]]["device"], G.nodes[pair[1]]["device"]
            if type1!=type2:
                continue
            if type1=='IO':
                continue
            if type_filter_pnmos(type1, type2):
                w1 = G.nodes[pair[0]]['w']
                w2 = G.nodes[pair[1]]['w']
                l1 = G.nodes[pair[0]]['l']
                l2 = G.nodes[pair[1]]['l']          
                # ignore matching
                if w1 != w2 or l1 != l2:
                    continue

            valid_pair_num += 1
            neg_pair_num += 1
            
            # neg_pairs: first 2 cols - node idx, 3rd col - label, 4th col - is_train
            if is_train:
                if len(neg_pairs) > neg_size * len(label):
                    break
                else:
                    neg_pairs.append([pair[0], pair[1], 0, 1])
            elif i in testset:
                neg_pairs.append([pair[0], pair[1], 0, 0])
            else:
                neg_pairs.append([pair[0], pair[1], 0, 2])

        pos_pairs = []
        for l in label:
            # ignore self symmetry
            if len(l) == 1:
                continue
            type1, type2 = G.nodes[pair[0]]["device"], G.nodes[pair[1]]["device"]
            if not type_filter_pnmos(type1, type2):
                continue
            w1 = G.nodes[pair[0]]['w']
            w2 = G.nodes[pair[1]]['w']
            l1 = G.nodes[pair[0]]['l']
            l2 = G.nodes[pair[1]]['l']          
            # ignore matching
            if w1 != w2 or l1 != l2:
                continue

            if is_train:
                pos_pairs.append([l[0]+num_nodes, l[1]+num_nodes, 1, 1])
            elif i in testset:
                pos_pairs.append([l[0]+num_nodes, l[1]+num_nodes, 1, 0])
            else:
                pos_pairs.append([l[0]+num_nodes, l[1]+num_nodes, 1, 2])

            valid_pair_num += 1

        sub_pairs=pos_pairs + neg_pairs
        random.seed(1)
        random.shuffle(sub_pairs)

        all_pairs += sub_pairs
        num_nodes += len(graph.nodes)

        # construct graph edges 
        # hyperedge: clique model
        for p in graph.pins:
            node_attr[p.id+num_nodes] = p.attributes["type"]
            node_types.append(p.attributes["type"]) 
            node_is_pin.append(np.array([1])) # [1] for pin, [0] for device

            G.add_node(p.id+num_nodes)
            G.nodes[p.id+num_nodes]["type"] = p.attributes["type"]
            # connect device with its corresponding pins
            if graph.nodes[p.node_id].attributes["cell"] == "IO":
                G.add_edge(p.node_id+num_nodes-len(graph.nodes), p.id+num_nodes, weight=0)
            else:
                G.add_edge(p.node_id+num_nodes-len(graph.nodes), p.id+num_nodes, weight=0.5)
        # connect pins in the same hyperedge
        for n in graph.nets:
            edges = combinations(n.pins, 2)
            for edge in edges:
                G.add_edge(edge[0]+num_nodes, edge[1]+num_nodes, weight=0)

        # compute potential
        sflag, snode = 0, -1
        for g in graph.nodes:
            if power_name_filter(g.attributes["name"]) > sflag:
                sflag = power_name_filter(g.attributes["name"])
                snode = g.id+num_nodes-len(graph.nodes)
        pin_potential = symbolic_electricity_potential(G, snode, num_nodes, num_nodes+len(graph.pins))
        node_potential.extend([0 for _ in range(len(graph.nodes))] + pin_potential)

        for g in graph.nodes:
            node_pin_elec = []
            for p in g.pins:
                node_pin_elec.append(pin_potential[p])
            G.nodes[g.id+num_nodes-len(graph.nodes)]["elec"] = node_pin_elec

        num_nodes += len(graph.pins)
        #draw_graph(G, node_attr, label)

    # convert node types into one-hot vector
    all_type = {'IO': 0, 'nmos': 1, 'pmos': 2, 'res': 3, 'gate': 4, \
        'source/drain': 5, 'substrate': 6, 'passive': 7, 'cap': 8, 'bjt' : 9, "c" : 10, "b" : 11, "e" : 12}
    # for x in node_types:
    #     if x not in all_type:
    #         all_type[x] = len(all_type)
    print(all_type)
    num_types = len(all_type)
    feat = []
    for x in node_types:
        feat.append(convert_one_hot(all_type[x], num_types))
    # features consist of 3 parts: device/pin, type one hot, symbolic potential
    feats = np.array([np.hstack((node_is_pin[t], np.array(feat[t]), np.array(node_potential[t]))) for t in range(len(feat))])
    #print(feats.shape)
    print("dataset statistics:", "#nodes", len(G.nodes), "#edges", len(G.edges), "#pairs", valid_pair_num, "#negpairs", neg_pair_num)

    return feats, G, all_pairs

