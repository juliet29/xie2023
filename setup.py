import matplotlib.pyplot as plt
import numpy as np

import networkx as nx

from operator import itemgetter

from helpers import *
from graph_data import *

class SetUp():
    def __init__(self):
        self.graph = self.initialize_graph()
        self.create_spanning_tree()
        pass


    def initialize_graph(self):
        # nodes
        n_nodes = 4 # TODO make flexible, assert that data matches up 
        CG = nx.complete_graph(n_nodes)  

        for ix, node in enumerate(CG.nodes):
            d = [list_of_values[ix] for list_of_values in NODE_DATA.values()]
            CG.nodes[ix]["props"] = NodeProperties(*d, ix) 
            #TODO can extend the node object from networkx module so dont have props dict 

        # orientations may not be fixed coming 
        ut = self.set_orientations()

        # set graph edges info
        # graph needs to be a directed graph 
        DG = nx.DiGraph(CG)
        for iy, ix in np.ndindex(ut.shape):
            if (iy, ix) in DG.edges():
                DG.edges[iy, ix]["orient"] = ut[iy, ix]
                DG.edges[iy, ix]["space_rel"] = SPACE_REL[iy, ix]


        return DG
    
    
    def set_orientations(self):
        ut = np.triu(ORIENTATIONS)

        # randomly set values in upper triangle that are not set 
        rng = np.random.default_rng(seed=42)
        for iy, ix in np.ndindex(ut.shape):
            if ut[iy, ix] == Orient.NONE:
                r = rng.integers(Orient.NORTH.value, Orient.WEST.value, size=1)[0]
                ut[iy, ix] = Orient(r)

        # match with partner
        for iy, ix in np.ndindex(ut.shape):
            if ut[iy, ix] == 0:
                ut[iy, ix] = ut[ix, iy].partner

        # zero out diagonal 
        for iy, ix in np.ndindex(ut.shape):
            if iy == ix:
                ut[iy, ix] = Orient(0) 

        return ut 



    def create_spanning_tree(self):
        self.tree = list(nx.edge_dfs(self.graph, source=0))

        spanning = []
        backing = []
        for e in self.tree:
            if abs(e[1] - e[0]) == 1:
                if e[1] - e[0] < 0:
                    spanning.append((e[1], e[0]))
                else:
                    spanning.append(e)
            else:
                if e[1] - e[0] > 0:
                    backing.append((e[1], e[0]))
                else:
                    backing.append(e)

        self.forward_edges, self.back_edges  = list(set(spanning)), sorted(list(set(backing)), reverse=True)
        self.spanning_tree = self.forward_edges + self.back_edges
        return self.spanning_tree
        
