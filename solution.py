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
            a.set_face_relation(n0, curr_face.axis, "NET") 
        n0.constrained = True
        
        return n0.faces.get_node_sols()
    

    
    def solve_2D_problem(self):
        a = Actions()
        tree = self.spanning_tree
        for ix, edge in enumerate(tree):
            self.process_track[ix] = ProcessTracking()
            self.process_track[ix].edge = edge

            ni = self.graph.nodes[edge[0]]["props"]
            nj = self.graph.nodes[edge[1]]["props"] # new node to set 
            orient = self.graph.edges[edge]["orient"] 

            # relationships 
            self.visited_nodes.append(nj.index)
            self.nb_track[nj.index].current_nb = ni.index

            # orient # TODO fix basis in orient function 
            a.orient_ij(ni, nj, orient)
            em_check, fig = a.check(ni, nj, viz=True)
            self.process_track[ix].figs["orient"] = fig
            self.process_track[ix].empty_checks["orient"] = em_check
            if em_check:
                return 

            # # spatial relate
            # a.spatial_relate_ij()
            # a.check()

            # # match faces 
            # a.set_face_relation(nj, orient.axis)
            # a.check()

            # update relationships 
            self.nb_track[nj.index].current_nb = None
            self.nb_track[nj.index].correct_nb.append(ni.index)

    
    def see_updates(self):
        for k, v in self.process_track.items():
            c = v.empty_checks["orient"]
            v.figs["orient"].add_annotation(x=60, y=60, text=f"empty:{c}", showarrow=False)
            orientation = self.graph.edges[v.edge]["orient"] 
            v.figs["orient"].update_layout(title_text=f"{v.edge} - {orientation}")

            v.figs["orient"].show()
            








    def solve_TB_problem(self):
        pass
