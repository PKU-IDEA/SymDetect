##
# @file   readgraph.py
# @author Yibo Lin
# @date   Feb 2020
#

import os
import sys
import pdb
import numpy as np
import networkx as nx
import pickle
import networkx as nx
from itertools import combinations
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import OrderedDict
import random
from sklearn.model_selection import train_test_split

class SpiceEntry (object):
    def __init__(self):
        self.name = ""
        self.pins = []
        self.cell = None
        self.attributes = {}

    def __str__(self):
        content = "name: " + self.name
        content += "; pins: " + " ".join(self.pins)
        content += "; cell: " + self.cell
        content += "; attr: " + str(self.attributes)
        return content

    def __repr__(self):
        return self.__str__()

class SpiceSubckt (object):
    def __init__(self):
        self.name = ""
        self.pins = []
        self.entries = []

    def __str__(self):
        content = "subckt: " + self.name + "\n"
        content += "pins: " + " ".join(self.pins) + "\n"
        content += "entries: \n";
        for entry in self.entries:
            content += str(entry) + "\n"
        return content

class SpiceNode (object):
    def __init__(self):
        self.id = None
        self.attributes = {} # include name (named in hierarchy), cell
        self.pins = []
    def __str__(self):
        content = "SpiceNode( " + str(self.id) + ", " + str(self.attributes) + ", " + str(self.pins) + " )"
        return content
    def __repr__(self):
        return self.__str__()

class SpiceNet (object):
    def __init__(self):
        self.id = None
        self.attributes = {} # include name
        self.pins = []
    def __str__(self):
        content = "SpiceNet( " + str(self.id) + ", " + str(self.attributes) + ", " + str(self.pins) + " )"
        return content
    def __repr__(self):
        return self.__str__()

class SpicePin (object):
    def __init__(self):
        self.id = None
        self.node_id = None
        self.net_id = None
        self.attributes = {} # include type
    def __str__(self):
        content = "SpicePin( " + str(self.id) + ", node: " + str(self.node_id) + ", net: " + str(self.net_id) + " attributes: " + str(self.attributes) + " )"
        return content
    def __repr__(self):
        return self.__str__()

class SpiceGraph (object):
    def __init__(self):
        self.nodes = []
        self.pins = []
        self.nets = []
    def __str__(self):
        content = "SpiceGraph\n"
        for node in self.nodes:
            content += str(node) + "\n"
        for pin in self.pins:
            content += str(pin) + "\n"
        for net in self.nets:
            content += str(net) + "\n"
        return content

def draw_graph(G, labels, color):
    color_map = []
    for node in G:
        flag = 0
        for i in range(len(color)):
            if node in color[i]:
                color_map.append(10*i+10)
                flag = 1
        if flag == 0:
            color_map.append(10*len(color)+10)
    #for node in G:
        #if node in color:
            #color_map.append('skyblue')
        #else:
            #color_map.append('green')
    pos = nx.nx_pydot.graphviz_layout(G, prog='dot')
    options = {'arrowstyle': '-|>', 'arrowsize': 12}
    nx.draw(G, font_weight='bold', pos=pos, node_color=color_map, **options, cmap=plt.cm.Blues)
    nx.draw_networkx_labels(G,pos,labels,font_size=16)
    plt.savefig('graph.pdf', dpi=120)

def convert(integer, length):
    bool_list = [0] * length
    bool_list[integer] = 1
    return bool_list

def type_rule(type1, type2):
    types1 = ['diode', 'res', 'cap']
    types2 = ['pfet', 'nfet', 'pfet_lvt', 'nfet_lvt']
    if type1 in types1:
        return (type1 == type2)
    if type1 in types2:
        return (type2 in types2)
    return 0

def type_rule2(type1, type2):
    types1 = ['pfet', 'pfet_lvt', 'pmos']
    types2 = ['nfet', 'nfet_lvt', 'nmos']
    if type1 in types1:
        return type2 in types1
    if type1 in types2:
        return type2 in types2
    return 0

def type_filter(type1):
    types1 = ['pfet', 'pfet_lvt', 'pmos']
    types2 = ['nfet', 'nfet_lvt', 'nmos']
    if type1 in types1:
        return 'pmos'
    elif type1 in types2:
        return 'nmos'
    else:
        return type1

def power_name_filter(pname):
    if 'gnd' in pname.lower():
        return 2
    if 'vss' in pname.lower():
        return 1
    return 0

def count_pin_num(t1, t2):
    if t1 in ['drain', 'gate'] and t2 in ['drain', 'gate']:
        return 0
    elif t1 in ['drain', 'source'] and t2 in ['drain', 'source']:
        return 1
    elif t1 in ['drain', 'substrate'] and t2 in ['drain', 'substrate']:
        return 2
    elif t1 in ['gate', 'source'] and t2 in ['gate', 'source']:
        return 3
    elif t1 in ['gate', 'substrate'] and t2 in ['gate', 'substrate']:
        return 4
    elif t1 in ['source', 'substrate'] and t2 in ['source', 'substrate']:
        return 5
    else:
        return 6

def symbolic_electricity_potential(g, snode, left, right):
    '''extract electricity potential feature from gnd
    save into files, add attribute to graph node
    '''
    pin_elec = []
    for pin in range(left, right):
        path_len = nx.shortest_path_length(g, source=snode, target=pin, weight='weight')
        pin_elec.append(path_len)
    return pin_elec

if __name__ == '__main__':
    # pickle file
    filename = sys.argv[1]
    #test_subckt = int(sys.argv[2])

    with open(filename, "rb") as f:
        dataX, dataY = pickle.load(f)

    save_dir = "../data/"
    G = nx.Graph()
    node_att = {}
    num_nodes = 0   # used to merge subgraphs by changing node indices
    all_pairs = []  # store all pos and neg node pairs
    node_type = []  # store types of all nodes
    node_is_pin = []
    node_potential = [] # store symbolic electricity potential of all pins
    ratio = 0.7     # #training_samples/#total_samples
    trainset = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(trainset)
    valid_pair_num = 0
    neg_pair_num = 0
    for i in range(len(dataX)):
        sub_G = nx.Graph()
        train = i in trainset
        subckts = dataX[i]["subckts"] # raw subcircuits read from spice netlist
        graph = dataX[i]["graph"] # hypergraph
        label = dataY[i] # symmetry pairs of node indices, self-symmetry if a pair only has one element
        pin_map = {}    # map pins to node id
        for g in graph.nodes:
            node_att[g.id+num_nodes] = type_filter(g.attributes['cell'])
            node_type.append(type_filter(g.attributes['cell']))
            node_is_pin.append(np.array([1, 0]))
            G.add_node(g.id+num_nodes)
            sub_G.add_node(g.id+num_nodes)
            G.nodes[g.id+num_nodes]['name'] = g.attributes['name']
            G.nodes[g.id+num_nodes]['graph'] = i
            if g.attributes['cell'] == 'IO':
                G.nodes[g.id+num_nodes]['type'] = 'IO'
                sub_G.nodes[g.id+num_nodes]['type'] = 'IO'
            else:
                G.nodes[g.id+num_nodes]['type'] = 'device'
                sub_G.nodes[g.id+num_nodes]['type'] = 'device'
            if g.attributes['cell'] in ['pmos', 'pfet', 'pfet_lvt', 'nmos', 'nfet', 'nfet_lvt']:
                G.nodes[g.id+num_nodes]['w'] = float(g.attributes['w']) / int(g.attributes['nf'])
                G.nodes[g.id+num_nodes]['l'] = float(g.attributes['l'])
                G.nodes[g.id+num_nodes]['device'] = g.attributes['cell']
            else:
                G.nodes[g.id+num_nodes]['w'] = -1
                G.nodes[g.id+num_nodes]['l'] = -1
                G.nodes[g.id+num_nodes]['device'] = '-1'
            # comment lines below and uncomment line above if using pin info
            '''for p in g.pins:
                pin_map[p] = g.id
        for n in graph.nets:
            node_list = []
            for pin in n.pins:
                if pin_map[pin] not in node_list:
                    node_list.append(pin_map[pin])
            edges = combinations(node_list, 2)
            for edge in edges:
                G.add_edge(edge[0]+num_nodes, edge[1]+num_nodes)
                sub_G.add_edge(edge[0]+num_nodes, edge[1]+num_nodes)'''

        node_pairs = list(combinations(list(sub_G.nodes()), 2)) # all possible node pairs
        #random.seed(1)
        #random.shuffle(node_pairs)
        neg_pairs = []
        #neg_size = 300000000
        neg_size = 2
        for pair in node_pairs:
            if [pair[0]-num_nodes, pair[1]-num_nodes] in label or [pair[1]-num_nodes, pair[0]-num_nodes] in label:
                continue
            type1, type2 = graph.nodes[pair[0]-num_nodes].attributes['cell'], graph.nodes[pair[1]-num_nodes].attributes['cell']
            if not type_rule2(type1, type2):
                continue
            valid_pair_num += 1
            neg_pair_num += 1
            '''w1, l1 = float(graph.nodes[pair[0]-num_nodes].attributes['w']) / int(graph.nodes[pair[0]-num_nodes].attributes['nf']), float(graph.nodes[pair[0]-num_nodes].attributes['l'])
            w2, l2 = float(graph.nodes[pair[1]-num_nodes].attributes['w']) / int(graph.nodes[pair[1]-num_nodes].attributes['nf']), float(graph.nodes[pair[1]-num_nodes].attributes['l'])
            if w1 != w2 or l1 != l2:
                continue'''
            if train:
                if len(neg_pairs) > neg_size*len(label):
                    break
                else:
                    neg_pairs.append([pair[0], pair[1], 0, 1])
                # first two cols are node ids, the third col is the label, the last col is train or test
            else:
                neg_pairs.append([pair[0], pair[1], 0, 0])

        pos_pairs = []
        for l in label:
            if len(l) == 1:
                continue
            valid_pair_num += 1
            type1, type2 = graph.nodes[l[0]].attributes['cell'], graph.nodes[l[1]].attributes['cell']
            if not type_rule2(type1, type2):
                continue
            w1, l1 = float(graph.nodes[l[0]].attributes['w']) / int(graph.nodes[l[0]].attributes['nf']), float(graph.nodes[l[1]].attributes['l'])
            w2, l2 = float(graph.nodes[l[1]].attributes['w']) / int(graph.nodes[l[1]].attributes['nf']), float(graph.nodes[l[1]].attributes['l'])
            if w1 != w2 or l1 != l2:
                continue
            if train:
                pos_pairs.append([l[0]+num_nodes, l[1]+num_nodes, 1, 1])
            else:
                pos_pairs.append([l[0]+num_nodes, l[1]+num_nodes, 1, 0])

        all_pairs += pos_pairs + neg_pairs
        num_nodes += len(graph.nodes)

        # uncomment lines below if using pin info
        for p in graph.pins:
            node_att[p.id+num_nodes] = p.attributes['type']
            node_type.append(p.attributes['type'])
            node_is_pin.append(np.array([0, 1]))
            G.add_node(p.id+num_nodes)
            G.nodes[p.id+num_nodes]['type'] = p.attributes['type']
            if graph.nodes[p.node_id].attributes['cell'] == 'IO':
                G.add_edge(p.node_id+num_nodes-len(graph.nodes), p.id+num_nodes, weight=0)
            else:
                G.add_edge(p.node_id+num_nodes-len(graph.nodes), p.id+num_nodes, weight=0.5)
        for n in graph.nets:
            edges = combinations(n.pins, 2)
            for edge in edges:
                G.add_edge(edge[0]+num_nodes, edge[1]+num_nodes, weight=0)

        sflag, snode = 0, -1
        for g in graph.nodes:
            if power_name_filter(g.attributes['name']) > sflag:
                sflag = power_name_filter(g.attributes['name'])
                snode = g.id+num_nodes-len(graph.nodes)
        pin_potential = symbolic_electricity_potential(G, snode, num_nodes, num_nodes+len(graph.pins))
        node_potential.extend([0 for _ in range(len(graph.nodes))] + pin_potential)
        
        for g in graph.nodes:
            node_pin_elec = []
            for p in g.pins:
                node_pin_elec.append(pin_potential[p])
            G.nodes[g.id+num_nodes-len(graph.nodes)]['elec'] = node_pin_elec

        num_nodes += len(graph.pins)

        #draw_graph(G, node_att, label)

    # convert node types into one-hot vector
    all_type = {}
    for x in node_type:
        if x not in all_type:
            all_type[x] = len(all_type)
    print(all_type)
    num_types = len(all_type)
    feat = []
    for x in node_type:
        feat.append(convert(all_type[x], num_types))
    feats = np.array([np.hstack((node_is_pin[t], np.array(feat[t]), np.array(node_potential[t]))) for t in range(len(feat))])
    print(feats.shape)
    # comment line below and uncommnet line above if using elec potential
    #feats = np.array([np.hstack((node_is_pin[t], np.array(feat[t]))) for t in range(len(feat))])
    # comment line below and uncomment line above if using pin info
    #feats = np.array([np.array(x) for x in feat])
    '''all_size = {}
    for x in node_size:
        if x not in all_size:
            all_size[x] = len(all_size)
    num_sizes = len(all_size)
    featsize = []
    for x in node_size:
        featsize.append(convert(all_size[x], num_sizes))
    feats = np.array([np.hstack((np.array(feat[t]), np.array(featsize[t]))) for t in range(len(feat))])'''
    print(len(G.nodes), len(G.edges), valid_pair_num, neg_pair_num)

    # save all files
    np.save(save_dir+"feats.npy", feats)
    nx.write_edgelist(G, save_dir+"all.edgelist")
    nx.write_gpickle(G, save_dir+'graph.pkl')
    with open(save_dir+"labels.txt", "w") as ff:
        for pair in all_pairs:
            ff.write((str(pair[0])+" "+str(pair[1])+" "+str(pair[2])+" "+str(pair[3])+"\n"))


