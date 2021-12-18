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
        nflist, llist, caplist, reslist, bjtlist, xilist, trainset=[]):
    G = nx.Graph() # the graph of all circuits
    num_nodes = 0 # used to merge subgraphs by changing node indices
    all_pairs = [] # store all pos and neg node pairs
    
    node_attr = {} # ?
    node_types = [] # store types of all nodes
    node_is_pin = [] # ? judge pin
    node_potential = [] # store symbolic electricity potential of all pins
    ratio_sample = 0.7 # #training_samples/#total_samples
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
            node_is_pin.append(np.array([1, 0]))
            
            # add node
            G.add_node(g.id+num_nodes)
            sub_G.add_node(g.id+num_nodes)
            G.nodes[g.id+num_nodes]["name"] = g.attributes["name"]
            G.nodes[g.id+num_nodes]["graph"] = i # which subgraph the node belongs to

            if g.attributes["cell"] == "IO":
                G.nodes[g.id+num_nodes]["type"] = "IO"
                sub_G.nodes[g.id+num_nodes]["type"] = "IO"
            else:
                G.nodes[g.id+num_nodes]["type"] = "device"
                sub_G.nodes[g.id+num_nodes]["type"] = "device"
            #if g.attributes["cell"] in ["pmos", "pfet", "pfet_lvt", "PMOS", "nmos", "nfet", "nfet_lvt", "NMOS"] or "xm" in g.attributes["cell"]:
            if g.attributes["cell"] in moslist:
                w, nf = -1, 1
                #if 'w' in g.attributes:
                #    w = convert_length(g.attributes['w'])
                #elif 'fw' in g.attributes:
                #    w = convert_length(g.attributes['fw'])
                for wname in wlist:
                    if wname in g.attributes:
                        w = convert_length(g.attributes[wname])
                        break
                #if 'nf' in g.attributes:
                #    nf = int(g.attributes['nf'])
                #elif 'fn' in g.attributes:
                #    nf = int(g.attributes['fn'])
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
                G.nodes[g.id+num_nodes]["device"] = g.attributes["cell"]
            else:
                G.nodes[g.id+num_nodes]['w'] = -1
                G.nodes[g.id+num_nodes]['l'] = -1
                G.nodes[g.id+num_nodes]["device"] = "-1"

        # determine pairs for training
        node_pairs = list(combinations(list(sub_G.nodes()), 2)) # all possible node pairs
        #random.seed(1)
        #random.shuffle(node_pairs)
        neg_pairs = []
        neg_size = 2 # the ratio of #neg_pairs/#pos_pairs
        for pair in node_pairs:
            # skip pos pairs 
            if [pair[0]-num_nodes, pair[1]-num_nodes] in label or [pair[1]-num_nodes, pair[0]-num_nodes] in label:
                continue
            type1, type2 = graph.nodes[pair[0]-num_nodes].attributes["cell"], graph.nodes[pair[1]-num_nodes].attributes["cell"]
            # ignore devices not mos 
            #if not type_filter_pnmos(type1, type2):
            #    continue
            valid_pair_num += 1
            neg_pair_num += 1
            
            # neg_pairs: first 2 cols - node idx, 3rd col - label, 4th col - is_train
            if is_train:
                if len(neg_pairs) > neg_size * len(label):
                    break
                else:
                    neg_pairs.append([pair[0], pair[1], 0, 1])
            else:
                neg_pairs.append([pair[0], pair[1], 0, 0])

        pos_pairs = []
        for l in label:
            # ignore self symmetry
            if len(l) == 1:
                continue
            valid_pair_num += 1
            type1, type2 = graph.nodes[l[0]].attributes["cell"], graph.nodes[l[1]].attributes["cell"]
            if not type_filter_pnmos(type1, type2):
                continue
            # ??? wl
            w1, l1, w2, l2 = -1, -1, -1, -1
            if 'w' in graph.nodes[l[0]].attributes:
                w1 = float(graph.nodes[l[0]].attributes['w']) / int(graph.nodes[l[0]].attributes['nf']) 
                w2 = float(graph.nodes[l[1]].attributes['w']) / int(graph.nodes[l[1]].attributes['nf'])
            elif 'fw' in g.attributes:
                w1 = convert_length(graph.nodes[l[0]].attributes['fw']) / int(graph.nodes[l[0]].attributes['fn'])
                w2 = convert_length(graph.nodes[l[1]].attributes['fw']) / int(graph.nodes[l[1]].attributes['fn'])
            l1 = convert_length(graph.nodes[l[0]].attributes['l'])
            l2 = convert_length(graph.nodes[l[1]].attributes['l'])
            # ignore matching
            if w1 != w2 or l1 != l2:
                continue
            if is_train:
                pos_pairs.append([l[0]+num_nodes, l[1]+num_nodes, 1, 1])
            else:
                pos_pairs.append([l[0]+num_nodes, l[1]+num_nodes, 1, 0])

        all_pairs += pos_pairs + neg_pairs
        num_nodes += len(graph.nodes)

        # construct graph edges 
        # hyperedge: clique model
        for p in graph.pins:
            node_attr[p.id+num_nodes] = p.attributes["type"]
            node_types.append(p.attributes["type"]) 
            node_is_pin.append(np.array([0, 1])) # [0, 1] for pin, [1, 0] for device

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
    all_type = {}
    for x in node_types:
        if x not in all_type:
            all_type[x] = len(all_type)
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

