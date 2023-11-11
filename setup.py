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
        self.fix_orientations()
        pass


    def initialize_graph(self):
        # nodes
        n_nodes = 4 # TODO make flexible, assert that data matches up 
        CG = nx.complete_graph(n_nodes)  

        for ix, node in enumerate(CG.nodes):
            d = [list_of_values[ix] for list_of_values in NODE_DATA.values()]
            CG.nodes[ix]["props"] = NodeProperties(*d, ix) #TODO can extend the node object from networkx module so dont have props dict 

        # edges # TODO make EdgeProperties object 
        n = np.linspace(0,3,4) # TODO make flexible 
        X2D,Y2D = np.meshgrid(n,n)
        attrs = {(x,y): {"space_rel": sr, "orient": o} for x,y,sr,o in zip(Y2D.ravel(),X2D.ravel(), SPACE_REL.ravel(), ORIENTATIONS.ravel())}
        nx.set_edge_attributes(CG, attrs)

        return CG
    
    def create_spanning_tree(self):
        # TODO fix alignments 
        self.tree = list(nx.edge_dfs(self.graph, source=0))
        self.traversal_order = [item for sublist in self.tree for item in sublist]
    
    def fix_orientations(self):
        # TODO -> extend to include all unincluded information 
        rng = np.random.default_rng(seed=42) # rand num generator
        new_orients = rng.integers(Orient.NORTH.value, Orient.WEST.value, len(self.tree)) # can assign new orientations to be NSEW but not (bottom/top -> level height addresses this)

        for n, rel in zip(new_orients, self.tree):
            if self.graph.edges[rel]["orient"] == Orient.NONE:
                self.graph.edges[rel]["orient"] = Orient(n)

        # FOR testing purposes, match Fig 16a, 3-2 has East(*-1) relationship => West (but edges are unidirectional for now, so keep as East...) 
        self.graph.edges[2,3]["orient"] = Orient.EAST

        return 

        
