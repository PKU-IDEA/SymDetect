#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob

import numpy as np
import networkx as nx

class SpiceEntry(object):
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

class SpiceSubckt(object):
    def __init__(self):
        self.name = ""
        self.pins = []
        self.entries = []

    def __str__(self):
        content = "subckt: " + self.name + "\n"
        content += "pins: " + " ".join(self.pins) + "\n"
        content += "entries: \n"
        for entry in self.entries:
            content += str(entry) + "\n"
        return content

    def __repr__(self):
        return self.__str__()

class SpiceNode(object):
    def __init__(self):
        self.id = None
        self.attributes = {}
        self.pins = []

    def __str__(self):
        content = "Node: " + str(self.id) + ", " + str(self.attributes) + ", " + str(self.pins)
        return content

    def __repr__(self):
        return self.__str__()

class SpiceNet(object):
    def __init__(self):
        self.id = None
        self.attributes = {}
        self.pins = []

    def __str__(self):
        content = "Net: " + str(self.id) + ", " + str(self.attributes) + ", " + str(self.pins)
        return content

    def __repr__(self):
        return self.__str__()

class SpicePin(object):
    def __init__(self):
        self.id = None
        self.node_id = None
        self.net_id = None
        self.attributes = {}
    
    def __str__(self):
        content = "SpicePin( " + str(self.id) + ", node: " + str(self.node_id) + ", net: " + str(self.net_id) + " attributes: " + str(self.attributes) + " )" 
        return content 

    def __repr__(self):
        return self.__str__()

class SpiceGraph(object):
    def __init__(self):
        self.nodes = []
        self.pins = []
        self.nets = []

    def __str__(self):
        content = "Graph\n"
        for node in self.nodes:
            content += str(node) + "\n"
        for pin in self.pins:
            content += str(pin) + "\n"
        for net in self.nets:
            content += str(net) + "\n"
        return content

    def __repr__(self):
        return self.__str__()
