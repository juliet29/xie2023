from setup import *
from actions import * 

class Solution(SetUp):
    def __init__(self):
        SetUp.__init__(self)

    def set_start_node(self):
        n0 = self.graph.nodes[0]["props"]
        # default settings for the initial node 
        base_faces = ["faceB", "faceW", "faceS"]
        props = [n0.level_height, 10, 10]

        a = Actions()
        for face, prop in zip(base_faces, props):
            curr_face = n0.faces.__getattribute__(face)
            curr_face.addConstraint(cn.InSetConstraint([prop])) 
            a.set_face_relation(n0, curr_face.axis, "NET") 
        n0.constrained = True
        return n0.faces.get_node_sols()
    
    def solve_TB_problem(self):
        pass

    def solve_2D_problem(self):
        a = Actions()
        # span_tree, back_tree = a.reorganize_tree(self.tree)
        # print(span_tree, back_tree)
        self.visited_nodes = []
        for edge in self.tree:
            # get the nodes
            
            self.new_node = self.graph.nodes[edge[1]]
            ni = self.graph.nodes[edge[0]]["props"]
            nj = self.new_node["props"]
            orient = self.graph.edges[edge]["orient"] 

            # if the new node is constrained, then flip ni and nj and flip the direction 
            if self.new_node["props"].constrained == True:
                ni = self.graph.nodes[edge[1]]["props"]
                self.new_node = self.graph.nodes[edge[0]]
                nj = self.new_node["props"]
                orient = orient.partner
                
            
            print(edge, orient) 
            # constrain based on orientation
            try:
                if orient.basis:
                    a.orient_ij(ni, nj, orient)
                else:
                    a.orient_ij(nj, ni, orient.partner)
                    print("switched")
                

                # match face 
                a.set_face_relation(nj, orient.axis)
            except:
                return "Issue :("
            print((f"node_num is {edge[1]}", nj.faces.get_node_sols()))

