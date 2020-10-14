##
# @file   netlist2graph.py
# @author Yibo Lin
# @date   Jan 2020
#

"""
import argparse
import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Spice.Parser import SpiceParser

import pdb 

parser = argparse.ArgumentParser(description='Convert a circuit file to PySpice')

parser.add_argument('circuit_file', # metavar='circuit_file',
                    help='.cir file')

parser.add_argument('-o', '--output',
                    default=None,
                    help='Output file')

parser.add_argument('--ground',
                    type=int,
                    default=0,
                    help='Ground node')

parser.add_argument('--build',
                    default=False, action='store_true',
                    help='Build circuit')

args = parser.parse_args()

parser = SpiceParser(path=args.circuit_file)

if args.build:
    parser.build_circuit()

circuit = parser.to_python_code(ground=args.ground)
if args.output is not None:
    with open(args.output, 'w') as f:
        f.write(circuit)
else:
    print(circuit)
"""

import os 
import sys 
import pdb 
import numpy as np 
import networkx as nx 
import pickle 

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

def subckts2graph(subckts, root_hint):
    # build hierachy_graph to find the roots 
    hierachy_graph = nx.DiGraph()
    subckts_map = {}
    subckts2nodes_map = {}
    for subckt in subckts:
        subckts_map[subckt.name] = subckt 
        hierachy_graph.add_node(subckt.name)
        subckts2nodes_map[subckt.name] = []

    for subckt in subckts:
        for entry in subckt.entries:
            if entry.cell in subckts_map: # refer another subckt 
                hierachy_graph.add_edge(subckt.name, entry.cell)

    roots = []
    for n, d in hierachy_graph.in_degree():
        if d == 0:
            roots.append(n)
    print("roots")
    print(roots)

    # build a flat graph 
    graph = SpiceGraph()

    def build_flat(subckt, context, context_nets):
        local_nets = {}
        for entry in subckt.entries:
            for pin in entry.pins:
                if pin not in subckt.pins:
                    assert pin not in context_nets, "%s not in %s failed" % (pin, str(context_nets.keys()))
                    if pin not in local_nets:
                        snet = SpiceNet()
                        snet.id = len(graph.nets)
                        snet.attributes["name"] = context + pin 
                        graph.nets.append(snet)
                        local_nets[pin] = snet
        print("local_nets")
        print(local_nets.keys())
        for entry in subckt.entries:
            if entry.cell not in subckts_map: # leaf device, mosfet, cap, res, etc. 
                snode = SpiceNode()
                snode.id = len(graph.nodes)
                snode.attributes["name"] = context + entry.name
                snode.attributes["cell"] = entry.cell 
                snode.attributes.update(entry.attributes)
                graph.nodes.append(snode)
                for i, pin in enumerate(entry.pins):
                    if pin in subckt.pins: # connect to external pin 
                        assert pin in context_nets, "%s in %s failed" % (pin, str(context_nets.keys())) 
                        spin = SpicePin() 
                        spin.id = len(graph.pins)
                        spin.node_id = snode.id
                        spin.net_id = context_nets[pin].id
                        if len(entry.pins) == 4 and ("fet" in entry.cell or "mos" in entry.cell):
                            if i == 0:
                                spin.attributes["type"] = "gate"
                            elif i == 1 or i == 2:
                                spin.attributes["type"] = "source/drain"
                            elif i == 3:
                                spin.attributes["type"] = "substrate"
                            else:
                                assert 0, "unknown %d" % (i)
                        elif "res" == entry.cell or "cap" == entry.cell:
                            spin.attributes["type"] = "passive"
                        elif "diode" in entry.cell:
                            if i == 0:
                                spin.attributes["type"] = "N+"
                            elif i == 1:
                                spin.attributes["type"] = "N-"
                            else:
                                assert 0, "unknown %d" % (i)
                        else:
                            pdb.set_trace()
                            assert 0, "unknown device"
                        snode.pins.append(spin.id)
                        context_nets[pin].pins.append(spin.id)
                        graph.pins.append(spin)
                    else: # local nets 
                        assert pin not in context_nets, "%s not in %s failed" % (pin, str(context_nets.keys())) 
                        spin = SpicePin() 
                        spin.id = len(graph.pins)
                        spin.node_id = snode.id
                        spin.net_id = local_nets[pin].id
                        if len(entry.pins) == 4 and ("fet" in entry.cell or "mos" in entry.cell):
                            if i == 0:
                                spin.attributes["type"] = "gate"
                            elif i == 1 or i == 2:
                                spin.attributes["type"] = "source/drain"
                            elif i == 3:
                                spin.attributes["type"] = "substrate"
                            else:
                                assert 0, "unknown %d" % (i)
                        elif "res" == entry.cell or "cap" == entry.cell:
                            spin.attributes["type"] = "passive"
                        elif "diode" in entry.cell:
                            if i == 0:
                                spin.attributes["type"] = "N+"
                            elif i == 1:
                                spin.attributes["type"] = "N-"
                            else:
                                assert 0, "unknown %d" % (i)
                        else:
                            pdb.set_trace()
                            assert 0, "unknown device"
                        snode.pins.append(spin.id)
                        local_nets[pin].pins.append(spin.id)
                        graph.pins.append(spin)
            else: # another subckt 
                another_subckt = subckts_map[entry.cell]
                another_context = context + entry.name + "/"
                another_context_nets = {}
                for i in range(len(entry.pins)):
                    pin = entry.pins[i]
                    if pin in subckt.pins: # connect to external pin 
                        assert pin in context_nets, "%s in %s failed" % (pin, str(context_nets.keys()))
                        another_context_nets[another_subckt.pins[i]] = context_nets[pin]
                    else: # local nets  
                        assert pin not in context_nets, "%s not in %s failed" % (pin, str(context_nets.keys()))
                        another_context_nets[another_subckt.pins[i]] = local_nets[pin]
                build_flat(another_subckt, another_context, another_context_nets)

    if root_hint in roots:
        roots = [root_hint]
    assert(len(roots) == 1)
    for root in roots:
        subckt = subckts_map[root]
        context_nets = {}
        for pin in subckt.pins:
            snode = SpiceNode()
            spin = SpicePin()
            snet = SpiceNet()
            snode.id = len(graph.nodes)
            snet.id = len(graph.nets)
            spin.id = len(graph.pins)

            snode.attributes["cell"] = "IO"
            snode.attributes["name"] = pin 
            snode.pins.append(spin.id)
            snet.attributes["name"] = pin 
            snet.pins.append(spin.id)
            spin.node_id = snode.id
            spin.net_id = snet.id
            spin.attributes["type"] = "IO"
            graph.nodes.append(snode)
            graph.nets.append(snet)
            graph.pins.append(spin)
            context_nets[pin] = snet
        build_flat(subckt, subckt.name + "/", context_nets)

        print("recovered")
        print_graph_subckt(subckt, graph)

    return graph, roots 

def print_graph_subckt(subckt, graph):
    content = ".subckt " + subckt.name
    for pin in subckt.pins:
        content += " " + pin
    content += "\n"
    for snode in graph.nodes:
        if snode.attributes["cell"] != "IO": 
            content += snode.attributes["name"]
            for pin_id in snode.pins:
                assert graph.pins[pin_id].node_id == snode.id
                content += " " + graph.nets[graph.pins[pin_id].net_id].attributes["name"]
            content += " " + snode.attributes["cell"]
            for key, value in snode.attributes.items():
                if key not in ["name", "cell"]:
                    content += " %s=%s" % (key, value)
            content += "\n"
    content += ".ends " + subckt.name
    print(content)

def read_netlist(filename):
    subckts = []
    subckt_flag = False 
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line: # skip empty line 
                continue 
            tokens = line.split()
            if line.startswith(".subckt"):
                subckts.append(SpiceSubckt())
                subckts[-1].name = tokens[1]
                subckts[-1].pins = tokens[2:]
                subckt_flag = True
            elif line.startswith(".ends"):
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
                            entry.cell = tokens[i]
                            entry.pins = tokens[1:i]
                            break 
                    subckts[-1].entries.append(entry)
                else:
                    assert 0, "not in a subckt: %s" % (line)

    #for subckt in subckts:
    #    print(subckt)
    return subckts


def read_sym(filename):
    subckt = ""
    symmetry_map = {}
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line: # skip empty line
                continue 
            tokens = line.split()
            if len(tokens) == 1 and not tokens[0].startswith("x"):
                subckt = tokens[0]
                symmetry_map[subckt] = []
            else:
                symmetry_map[subckt].append(tokens)

    #print("symmetry_map")
    #print(symmetry_map)
    return symmetry_map

dataX = []
dataY = []
for i in range(1, len(sys.argv)):
    filename = sys.argv[i]
    print("read %s" % (filename))
    root_hint = os.path.basename(filename).replace(".sp", "")
    subckts = read_netlist(filename)
    symmetry_map = read_sym(filename.replace("netlist/", "sym2/").replace(".sp", ".sym"))

    graph, roots = subckts2graph(subckts, root_hint)

    symmetry_id_array = []

    def add_symmetry_pairs(subckt_inst, pairs): 
        for pair in pairs:
            # skip an instance whose cell type is already symmetric 
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
            #names = [subckt_inst + "/" + v for v in pair]
            names = pair 
            node_id_pair = []
            groups = {}
            for name in names:
                groups[name] = []
            for snode in graph.nodes:
                for name in names: 
                    #if name in snode.attributes["name"]:
                    if root_hint + "/" + name == snode.attributes["name"]:
                        groups[name].append(snode.id)
            for k, v in groups.items():
                if len(v) != 1:
                    pdb.set_trace()
                assert len(v) == 1
                node_id_pair.append(v[0])
            symmetry_id_array.append(node_id_pair)

    for sym_subckt, pairs in symmetry_map.items():
        if sym_subckt in roots:
            add_symmetry_pairs(sym_subckt, pairs)
        else:
            for subckt in subckts:
                for entry in subckt.entries: 
                    if entry.cell == sym_subckt: 
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

with open("data.pkl", "wb")  as f:
    pickle.dump((dataX, dataY), f)
