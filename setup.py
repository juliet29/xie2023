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
    
    def ser_orientations(self):
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

        # set graph edges

        return 

        
