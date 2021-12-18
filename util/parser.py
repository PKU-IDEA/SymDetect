#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import glob
import pdb

import numpy as np
import networkx as nx

from util.netlist import *

def read_netlist(filename):
    subckts = []
    subckt_flag = False

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            if line.startswith("*"):
                continue
            elif line.startswith(".subckt") or line.startswith(".SUBCKT"):
                tmpckt = SpiceSubckt()
                tmpckt.name = tokens[1]
                tmpckt.pins = tokens[2:]
                subckts.append(tmpckt)
                subckt_flag = True
            elif line.startswith(".ends") or line.startswith(".ENDS"):
                subckt_flag = False
            else:
                if subckt_flag:
                    entry = SpiceEntry()
                    entry.name = tokens[0]
                    for i in range(len(tokens)-1, 0, -1):
                        token = tokens[i]
                        if '=' in token:
                            a_eq_b = token.split('=')
                            assert len(a_eq_b) == 2
                            entry.attributes[a_eq_b[0]] = a_eq_b[1]
                        else:
                            entry.cell = tokens[i] # type: nmos, pmos, ...
                            entry.pins = tokens[1:i]
                            break
                    subckts[-1].entries.append(entry)
                else:
                    assert 0, "not in a subckt: %s" % line

    return subckts

def read_symfile(filename):
    subckt = ""
    symmetry_map = {}
    
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            # ???
            if len(tokens) == 1 and not tokens[0].startswith("x"):
                subckt = tokens[0]
                symmetry_map[subckt] = []
            else:
                symmetry_map[subckt].append(tokens)

    return symmetry_map

def read_symattr(subckts):
    # parse symmetry group
    symmetry_map = {}

    for subckt in subckts:
        symmetry_map[subckt.name] = []
        for i in range(len(subckt.entries)):
            if "sg" in subckt.entries[i].attributes.keys():
                for j in range(i+1, len(subckt.entries)):
                    if "sg" not in subckt.entries[j].attributes.keys():
                        continue
                    if subckt.entries[i].attributes["sg"] == subckt.entries[j].attributes["sg"]:
                        symmetry_map[subckt.name].append([subckt.entries[i].name, subckt.entries[j].name])

    # parse matching group
    # not implemented yet
    
    return symmetry_map

def print_graph_subckt(subckt, graph):
    content = ".subckt " + subckt.name
    for pin in subckt.pins:
        content += " " + pin
    content += "\n"
    for tmpnode in graph.nodes:
        if tmpnode.attributes["cell"] != "IO":
            content += tmpnode.attributes["name"]
            for pin in tmpnode.pins:
                assert graph.pins[pin].node_id == tmpnode.id
                content += " " + graph.nets[graph.pins[pin].net_id].attributes["name"]
            content += " " + tmpnode.attributes["cell"]
            for key, value in tmpnode.attributes.items():
                if key not in ["name", "cell"]:
                    content += " %s=%s" % (key, value)
            content += "\n"
    content += ".ends " + subckt.name
    print(content)

def subckts2graph(subckts, root_hint, moslist, caplist, reslist, bjtlist, xilist):
    hierarchy_graph = nx.DiGraph()
    subckts_map = {}
    subckts2nodes_map = {}

    for subckt in subckts:
        subckts_map[subckt.name] = subckt
        hierarchy_graph.add_node(subckt.name)
        subckts2nodes_map[subckt.name] = []

    for subckt in subckts:
        for entry in subckt.entries:
            if entry.cell in subckts_map:
                hierarchy_graph.add_edge(subckt.name, entry.cell)

    roots = []
    for n, d in hierarchy_graph.in_degree():
        if d == 0:
            roots.append(n)
    print("roots", roots)

    graph = SpiceGraph()

    def build_flat(subckt, context, context_nets):
        local_nets = {}
        for entry in subckt.entries:
            for pin in entry.pins:
                if pin not in subckt.pins:
                    assert pin not in context_nets, "%s not in %s failed" % (pin, str(context_nets.keys()))
                    if pin not in local_nets:
                        tmpnet = SpiceNet()
                        tmpnet.id = len(graph.nets)
                        tmpnet.attributes["name"] = context + pin
                        graph.nets.append(tmpnet)
                        local_nets[pin] = tmpnet
        print("local nets", local_nets.keys())

        def entry_pins(entry, pin):
            #if len(entry.pins) == 4 and ("fet" in entry.cell or "mos" in entry.cell or "xm" in entry.cell):
            if len(entry.pins) == 4 and entry.cell in moslist:
                if i == 0:
                    pin.attributes["type"] = "gate"
                elif i == 1 or i == 2:
                    pin.attributes["type"] = "source/drain"
                elif i == 3:
                    pin.attributes["type"] = "substrate"
                else:
                    assert 0, "Unknown %d" % i
            #elif "res" in entry.cell or "cap" in entry.cell or "xr" in entry.cell or "xc" in entry.cell:
            elif entry.cell in reslist or entry.cell in caplist:
                pin.attributes["type"] = "passive"
            elif "diode" in entry.cell:
                if i == 0:
                    pin.attributes["type"] = "N+"
                elif i == 1:
                    pin.attributes["type"] = "N-"
                else:
                    assert 0, "Unknown %d" %i
            # bipolar junction transistor
            #elif "pnp" in entry.cell or "npn" in entry.cell:
            elif entry.cell in bjtlist:
                if i == 0:
                    pin.attributes["type"] = "c"
                elif i == 1:
                    pin.attributes["type"] = "b"
                elif i == 2:
                    pin.attributes["type"] = "e"
                else:
                    assert 0, "Unknown %d" % i
            # customized instance
            #elif "xi" in entry.cell:
            elif entry.cell in xilist:
                pin.attributes["type"] = "customized"
            else:
                assert 0, "Unknown device: %s" % entry.cell
        
        for entry in subckt.entries:
            # leaf device, mosfet, cap, res, bjt, etc
            if entry.cell not in subckts_map:
                tmpnode = SpiceNode()
                tmpnode.id = len(graph.nodes)
                tmpnode.attributes["name"] = context + entry.name
                tmpnode.attributes["cell"] = entry.cell
                tmpnode.attributes.update(entry.attributes)
                graph.nodes.append(tmpnode)
                for i, pin in enumerate(entry.pins):
                    if pin in subckt.pins:
                        assert pin in context_nets, "%s in %s failed" % (pin, str(context_nets.keys()))
                        tmppin = SpicePin()
                        tmppin.id = len(graph.pins)
                        tmppin.node_id = tmpnode.id
                        tmppin.net_id = context_nets[pin].id
                        entry_pins(entry, tmppin)
                        tmpnode.pins.append(tmppin.id)
                        context_nets[pin].pins.append(tmppin.id)
                        graph.pins.append(tmppin)
                    # local nets
                    else:
                        assert pin not in context_nets, "%s not in %s failed" % (pin, str(context_nets.keys()))
                        tmppin = SpicePin()
                        tmppin.id = len(graph.pins)
                        tmppin.node_id = tmpnode.id
                        tmppin.net_id = local_nets[pin].id
                        entry_pins(entry, tmppin)
                        tmpnode.pins.append(tmppin.id)
                        local_nets[pin].pins.append(tmppin.id)
                        graph.pins.append(tmppin)
            # another subckt
            else:
                subckt_sub = subckts_map[entry.cell]
                context_sub = context + entry.name + "/"
                context_nets_sub = {}
                for i in range(len(entry.pins)):
                    pin = entry.pins[i]
                    if pin in subckt.pins:
                        assert pin in context_nets, "%s in %s failed" % (pin, str(context_nets.keys()))
                        context_nets_sub[subckt_sub.pins[i]] = context_nets[pin]
                    else:
                        assert pin not in context_nets, "%s not in %s failed" % (pin, str(context_nets.keys()))
                        context_nets_sub[subckt_sub.pins[i]] = local_nets[pin]
                build_flat(subckt_sub, context_sub, context_nets_sub)

    if root_hint in roots:
        roots = [root_hint]
    assert len(roots) == 1
    for root in roots:
        subckt = subckts_map[root]
        context_nets = {}
        for pin in subckt.pins:
            tmpnode = SpiceNode()
            tmppin = SpicePin()
            tmpnet = SpiceNet()
            tmpnode.id = len(graph.nodes)
            tmpnet.id = len(graph.nets)
            tmppin.id = len(graph.pins)

            tmpnode.attributes["cell"] = "IO"
            tmpnode.attributes["name"] = pin
            tmpnode.pins.append(tmppin.id)

            tmpnet.attributes["name"] = pin
            tmpnet.pins.append(tmppin.id)

            tmppin.node_id = tmpnode.id
            tmppin.net_id = tmpnet.id
            tmppin.attributes["type"] = "IO"

            graph.nodes.append(tmpnode)
            graph.nets.append(tmpnet)
            graph.pins.append(tmppin)
            context_nets[pin] = tmpnet
        
        build_flat(subckt, subckt.name + "/", context_nets)

        print("recovered")
        print_graph_subckt(subckt, graph)

    return graph, roots

def parse_all(filedir, moslist, caplist, reslist, bjtlist, xilist):
    dataX = []
    dataY = []

    netlists = glob.glob(os.path.join(filedir, "*.sp"))
    symfiles = glob.glob(os.path.join(filedir, "*.sym"))
    for netlist in netlists:
        # parse netlist
        print("read netlist file: %s" % netlist)
        root_hint = netlist.split('/')[-1].split('.')[0]

        subckts = read_netlist(netlist)
        
        # parse symfile
        symfile = netlist.replace(".sp", ".sym") if netlist.replace(".sp", ".sym") in symfiles else None 

        if symfile:
            print("read symmetry file: %s" % symfile)
            symmetry_map = read_symfile(symfile)
        else:
            print("parse symmetry info from attributes")
            symmetry_map = read_symattr(subckts)
            pass

        # spice graph
        graph, roots = subckts2graph(subckts, root_hint, moslist, caplist, reslist, bjtlist, xilist)

        symmetry_id_array = []

        def add_symmetry_pairs(subckt_inst, pairs):
            for pair in pairs:
                skip_flag = False
                if len(pair) == 1:
                    for subckt in subckts:
                        for entry in subckt.entries:
                            if entry.name == pair[0] and entry.cell in symmetry_map:
                                skip_flag = True
                                break
                        if skip_flag:
                            break
                if skip_flag:
                    continue

                names = pair
                node_id_pair = []
                groups = {}
                for name in names:
                    groups[name] = []
                for tmpnode in graph.nodes:
                    for name in names:
                        if root_hint + "/" + name == tmpnode.attributes["name"]:
                            groups[name].append(tmpnode.id)
                for key, value in groups.items():
                    assert len(value) == 1
                    node_id_pair.append(value[0])
                symmetry_id_array.append(node_id_pair)

        for subckt_sym, pairs in symmetry_map.items():
            if subckt_sym in roots:
                add_symmetry_pairs(subckt_sym, pairs)
            else:
                for subckt in subckts:
                    for entry in subckt.entries:
                        if entry.cell == subckt_sym:
                            add_symmetry_pairs(entry.name, pairs)

        print("symmetry_map")
        print(symmetry_map)
        print("symmetry_id_array")
        print(symmetry_id_array)
        
        content = ""
        for pair in symmetry_id_array:
            content += "("
            for node_id in pair:
                if isinstance(node_id, tuple):
                    content += " { "
                    for nid in node_id:
                        content += " " + graph.nodes[nid].attributes["name"]
                    content += " } "
                else:
                    content += " " + graph.nodes[node_id].attributes["name"]
            content += " ) "
        print(content)

        dataX.append({"subckts" : subckts, "graph" : graph})
        dataY.append(symmetry_id_array)

    return dataX, dataY, netlists
