from setup import *
from actions import * 

class Solution(SetUp):
    def __init__(self):
        SetUp.__init__(self)

    def set_start_node(self):
        n0 = self.graph.nodes[0]["props"]
        # default settings for the initial node 
        base_faces = ["faceB", "faceW", "faceS"]
        props = [n0.level_height, 0, 0 ]

        a = Actions()
        for face, prop in zip(base_faces, props):
            curr_face = n0.faces.__getattribute__(face)
            curr_face.addConstraint(cn.InSetConstraint([prop])) 
            a.set_face_relation(n0, curr_face.axis, "NET") 
        return n0.faces.see_curr_sols()
    
    def solve_TB_problem(self):
        pass

    def solve_2D_problem(self):
        for edge in self.tree:
            a = Actions()

            # get the nodes
            ni = self.graph.nodes[edge[0]]["props"]
            nj = self.graph.nodes[edge[1]]["props"]
            # get the orientation 
            orient = self.graph.edges[self.tree[0]]["orient"] 
            print(edge, orient)
  
            # constrain based on orientation 
            a.orient_ij(ni, nj, orient)

            # match face 
            a.set_face_relation(nj, orient.axis)

