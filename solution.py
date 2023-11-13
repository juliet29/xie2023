from setup import *
from actions import * 

class Solution(SetUp):
    def __init__(self):
        SetUp.__init__(self)
        self.visited_nodes = []
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
            curr_face.state_update()
        a.set_face_rel(n0) 

        a.final_check(n0)
        
        return n0.faces.get_node_sols()
    

    
    def solve_2D_problem(self):
        
        tree = self.spanning_tree
        self.track = {}
        for ix, edge in enumerate(tree):
            a = Actions()
            if ix in [0,1, 2]:
                
                # self.track[ix] = []
                
                ni = self.graph.nodes[edge[0]]["props"]
                nj = self.graph.nodes[edge[1]]["props"] # new node to set 
                orient = self.graph.edges[edge]["orient"] 
                rel = self.graph.edges[edge]["space_rel"] 
                # self.track[ix].append([edge, orient, rel])
                ic(edge, orient)

                # relationships 
                self.visited_nodes.append(nj.index)


                # spatial relate
                a.spatial_relate_ij(ni, nj, orient, rel)
                # self.track[ix].append(nj.faces.get_node_sols())



                # complete rel 
                nj.correct_nb.append(ni)
                ni.correct_nb.append(nj)


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
    
    def get_node(self, ix):
        return self.graph.nodes[ix]["props"]
    
    def get_node_history(self, ix):
        hist = {}
        for f in self.get_node(ix).faces.face_list:
            hist[f.name] = f.state
        return hist


        
            








    def solve_TB_problem(self):
        pass
