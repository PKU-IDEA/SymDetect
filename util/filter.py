#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx

def convert_one_hot(index, length):
    one_hot = [0] * length
    one_hot[index] = 1
    return one_hot

def convert_length(length):
    # um / nm / scientific notation
    if 'u' not in length and 'n' not in length:
        return float(length)
    else:
        if 'u' in length:
            return float(length.split('u')[0]) * 1e-6
        elif 'n' in length:
            return float(length.split('n')[0]) * 1e-9

def type_filter_rule(type1, type2):
    types1 = ["diode", "res", "cap", "resistor", "capacitor"]
    types2 = ["pfet", "nfet", "pfet_lvt", "nfet_lvt", "NMOS", "PMOS"]
    if type1 in types1:
        return (type1 == type2)
    if "xm" in type1:
        return ("xm" in type2)
    if type1 in types2:
        return (type2 in types2)

def type_filter_pnmos(type1, type2):
    types1 = ["pfet", "pfet_lvt", "pmos", "PMOS"]
    types2 = ["nfet", "nfet_lvt", "nmos", "NMOS"]
    if type1 in types1:
        return type2 in types1
    if type1 in types2:
        return type2 in types2
    if "xm" in type1 and "p" in type1:
        return "p" in type2
    if "xm" in type2 and "n" in type2:
        return "n" in type2

'''def type_filter_mos(type1):
    types1 = ["pfet", "pfet_lvt", "pmos", "PMOS"]
    types2 = ["nfet", "nfet_lvt", "nmos", "NMOS"]

    if type1 in types1:
        return "pmos"
    elif type1 in types2:
        return "nmos"
    elif "xm" in type1 and "p" in type1:
        return "pmos"
    elif "xm" in type1 and "n" in type1:
        return "nmos"
    else:
        return type1'''

def type_filter_mos(type1, pmoslist, nmoslist, caplist, reslist, bjtlist, xilist):
    if type1 in pmoslist:
        return "pmos"
    elif type1 in nmoslist:
        return "nmos"
    elif type1 in caplist:
        return "cap"
    elif type1 in reslist:
        return "res"
    elif type1 in bjtlist:
        return "bjt"
    elif type1 in xilist:
        return "xi"
    else:
        return type1

def power_name_filter(pname):
    if "gnd" in pname.lower():
        return 2
    if "vss" in pname.lower():
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
    elif t1 in ['gate', 'substrate'] and t2 in ['gate','substrate']:
        return 4
    elif t1 in ['source', 'substrate'] and t2 in ['source', 'substrate']:
        return 5
    else:
        return 6

def symbolic_electricity_potential(g, snode, left, right):
    pin_elec = []
    for pin in range(left, right):
        path_len = nx.shortest_path_length(g, source=snode, target=pin, weight='weight')
        pin_elec.append(path_len)
    return pin_elec

