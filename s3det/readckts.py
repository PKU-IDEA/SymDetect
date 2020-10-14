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
    types1 = ['pfet', 'pfet_lvt']
    types2 = ['nfet', 'nfet_lvt']
    if type1 in types1:
        return type2 in types1
    if type1 in types2:
        return type2 in types2
    return 0

def readckts(filename):
    """parse: graph, pairs, label
    """
    with open(filename, "rb") as f:
        dataX, dataY = pickle.load(f)

    G = []  # list of graphs for subckts
    all_pairs = [] # list of proper pairs for subckts
    for i in range(len(dataX)):
        sub_G = nx.Graph()
        node_pair = []
        num_nodes = 0
        
        subckts = dataX[i]["subckts"]
        graph = dataX[i]["graph"]

        for g in graph.nodes:
            sub_G.add_node(g.id)

        pairs = list(combinations(list(sub_G.nodes()), 2)) # all possible node pairs
        for pair in pairs:
            type1, type2 = graph.nodes[pair[0]].attributes['cell'], graph.nodes[pair[1]].attributes['cell']
            if not type_rule2(type1, type2):
                continue
            w1, l1 = graph.nodes[pair[0]].attributes['w'], graph.nodes[pair[0]].attributes['l']
            w2, l2 = graph.nodes[pair[1]].attributes['w'], graph.nodes[pair[1]].attributes['l']
            if w1 != w2 or l1 != l2:
                continue
            node_pair.append([pair[0], pair[1]])

        num_nodes += len(graph.nodes)

        for p in graph.pins:
            sub_G.add_node(p.id+num_nodes)
            sub_G.add_edge(p.node_id, p.id+num_nodes)
        for n in graph.nets:
            edges = combinations(n.pins, 2)
            for edge in edges:
                sub_G.add_edge(edge[0]+num_nodes, edge[1]+num_nodes)

        all_pairs.append(node_pair)
        G.append(sub_G)

    return G, all_pairs, dataY
