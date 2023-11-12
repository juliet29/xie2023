from setup import *
from actions import * 

class Solution(SetUp):
    def __init__(self):
        SetUp.__init__(self)
        self.visited_nodes = []
        self.process_track = {}
        self.nb_track = {}
        for node in self.graph.nodes:
            self.nb_track[node] = LocalTracking()
        self.set_start_node()



    def set_start_node(self):
        n0 = self.graph.nodes[0]["props"]
        self.visited_nodes.append(n0.index)

        # default settings for the initial node 
        base_faces = ["faceB", "faceW", "faceS"]
        props = [n0.level_height, 10, 10]

        a = Actions()
        for face, prop in zip(base_faces, props):
            curr_face = n0.faces.__getattribute__(face)
            curr_face.addConstraint(cn.InSetConstraint([prop]))
        a.set_face_rel(n0) 
        n0.constrained = True
        
        return n0.faces.get_node_sols()
    

    
    def solve_2D_problem(self):
        a = Actions()
        tree = self.spanning_tree
        self.track = {}
        for ix, edge in enumerate(tree):
            if ix in [0,1,2]:
                ic(edge)
                self.track[ix] = []
                

                ni = self.graph.nodes[edge[0]]["props"]
                nj = self.graph.nodes[edge[1]]["props"] # new node to set 
                orient = self.graph.edges[edge]["orient"] 
                rel = self.graph.edges[edge]["space_rel"] 
                self.track[ix].append([edge, orient, rel])

                # relationships 
                self.visited_nodes.append(nj.index)
                self.nb_track[nj.index].current_nb = ni.index


                # spatial relate
                a.spatial_relate_ij(ni, nj, orient, rel)
                self.track[ix].append(nj.faces.get_node_sols())


                # match faces 
                a.set_face_rel()
                self.track[ix].append(nj.faces.get_node_sols())

                self.nb_track[nj.index].current_nb = None
                self.nb_track[nj.index].correct_nb.append(ni.index)

    def mode_update(self, v, mode):
        c = v.empty_checks[mode] if v.empty_checks[mode] else "-"
        v.figs[mode].add_annotation(x=60, y=60, text=f"empty:{c}", showarrow=False)
        orientation = self.graph.edges[v.edge]["orient"] 
        v.figs[mode].update_layout(title_text=f"{mode}:{v.edge} - {orientation}")

        v.figs[mode].show()
    
    def see_updates(self):
        for k, v in self.process_track.items():
                if k in [0,1]:
                    self.mode_update(v, "orient")
                    self.mode_update(v, "adjacent")

    def get_sols(self, ix):
        return self.graph.nodes[ix]["props"].faces.get_node_sols()
        
            








    def solve_TB_problem(self):
        pass
