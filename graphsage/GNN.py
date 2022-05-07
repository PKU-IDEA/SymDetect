import torch
import torch.nn.functional as F

# The PyG built-in GATConv
from torch_geometric.nn import GATConv, SAGEConv

import torch_geometric.transforms as T
from ogb.nodeproppred import PygNodePropPredDataset, Evaluator

class GNN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers,
                 dropout, return_embeds=True):
        # TODO: Implement a function that initializes self.convs, 
        # self.bns, and self.softmax.

        super(GNN, self).__init__()
        self.convs = torch.nn.ModuleList()
        self.convs.append(GATConv(input_dim,hidden_dim))
        for l in range(num_layers-2):
            self.convs.append(GATConv(hidden_dim,hidden_dim))
        self.convs.append(GATConv(hidden_dim,output_dim))

        self.bns = torch.nn.ModuleList()
        for l in range(num_layers-1):
            self.bns.append(torch.nn.BatchNorm1d(hidden_dim))
        
        self.softmax = torch.nn.LogSoftmax(dim=1)

        #########################################

        # Probability of an element getting zeroed
        self.dropout = dropout

        # Skip classification layer and return node embeddings
        self.return_embeds = return_embeds
        self.embed_dim=output_dim

    def reset_parameters(self):
        for conv in self.convs:
            conv.reset_parameters()
        for bn in self.bns:
            bn.reset_parameters()

    def forward(self, x, adj_t):
        for l in range(len(self.convs)-1):
            x = self.convs[l](x,adj_t)
            x = self.bns[l](x)
            x = F.relu(x)
            # x = F.dropout(x,self.dropout,self.training)
        x = self.convs[-1](x,adj_t)
        if self.return_embeds:
            out = x
        else:
            out = self.softmax(x)
        #########################################

        return out