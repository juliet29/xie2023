from helpers import *
from visuals import * 


class Actions:
    # SET MATCHING FACES ----------
    def __set_matching_face(self, f1: Face, f2: Face, prop):
        poss_sols = [[*sol.values()][0] + prop for sol in f2.getSolutionIter()]
        return f1.addConstraint(cn.InSetConstraint(poss_sols))

    def set_face_relation(self, n: NodeProperties, ax: Axes, rel_type="SWB"):
        d = {
            "NET": {
                Axes.Y: ("faceN", "faceS", n.width),
                Axes.X: ("faceE", "faceW", n.length),
                Axes.Z: ("faceT", "faceB", n.height),
            },
            "SWB": {
                Axes.Y: ("faceS", "faceN", n.width),
                Axes.X: ("faceW", "faceE", n.length),
                Axes.Z: ("faceB", "faceT", n.height),
            },
        }  # TODO might remove this from dict for speed purposes later

        f1, f2, prop = [*d[rel_type][ax]]
        return self.__set_matching_face(
            n.faces.__getattribute__(f1), n.faces.__getattribute__(f2), prop
        )

    # def __set_matching_face(self, f1: Face, f2:Face, prop):
    #     poss_sols = [[*sol.values()][0] + prop for sol in f2.getSolutionIter()]
    #     return f1.addConstraint(cn.InSetConstraint(poss_sols))
    

    def orient_ij(self, ni: NodeProperties, nj: NodeProperties, orient: Orient):
        ni = ni.faces
        nj = nj.faces
        d = {
            Orient.NORTH: (nj.faceN, ni.faceS),
            Orient.SOUTH: (nj.faceN, ni.faceS),
            Orient.EAST: (nj.faceE, ni.faceW),
            Orient.WEST: (nj.faceE, ni.faceW),
            Orient.TOP: (nj.faceT, ni.faceB),
            Orient.BOTTOM: (nj.faceT, ni.faceB),
        }

        f1, f2 = d[orient]
        min_f2 = min([abs(list(s.values())[0]) for s in f2.getSolutions()])

        if orient.basis:
            return f1.addConstraint(lambda x: x <= min_f2) 
        else:
            return f1.addConstraint(lambda x: x >= min_f2)  
        


    def spatial_relate_ij(self, ni: NodeProperties, nj: NodeProperties, orient: Orient, rel: SpatialRel):
        if rel == SpatialRel.ADJACENT:
            if orient == Orient.NORTH or orient == Orient.SOUTH:
                assert(len(ni.faces.faceW.get_face_sols()) == 1)
                assert(len(ni.faces.faceE .get_face_sols()) == 1)
                
                print(ni.faces.faceW.sols, ni.faces.faceE.sols)

                side1 = ni.faces.faceW.sols[0] - nj.length + THRESHOLD
                side2 = ni.faces.faceE.sols[0] - THRESHOLD

                print(side1, side2)

                nj.faces.faceW.addConstraint(lambda x: side1 < x < side2)

                if orient == Orient.NORTH:
                    # ni.faceN == nj.faceS
                    f1 = nj.faces.faceS
                    f2 = ni.faces.faceN
                else:
                    f1 = nj.faces.faceN
                    f2 = ni.faces.faceS
    
                assert(len(f2.get_face_sols()) == 1)
                f2.addConstraint(cn.InSetConstraint(f1.sols))
        else:
            pass


    def set_face_rel(self, node: NodeProperties):
        # if face vals are not the default, set the match face 
        d = {
            Axes.Y: node.width,
            Axes.X: node.length,
            Axes.Z: node.height,
            }
        
        for face in node.faces.face_list:
            prop = d[face.axis]
            if not face.sols:
                face.get_face_sols()
            if not face.orig_sols:
                poss_sols = [[*sol.values()][0] + prop for sol in face.getSolutionIter()]
                print("original", poss_sols)
                face.partner.addConstraint(cn.InSetConstraint(poss_sols))



        


    def check(self, ni:NodeProperties, nj:NodeProperties, viz:bool=False):
        

        # check that solitoons exists for both nodes
        empty_sol_tracker = []
        for node in [ni, nj]:
            for face in node.faces.face_list:
                # print(node.index, face.name, face.getSolutions())
                sols = face.get_face_sols()
                if not sols:
                    empty_sol_tracker.append({"node": node.index, "face": face.name})

        fig = None 
        if viz:
            fig=go.Figure()
            p = PlotSols()
            for node in [ni, nj]:
                fig = p.plot_node_sols(node, fig)
            # TODO some tracker that stores all figs? 

        # TODO -> raise error if empty sol tracker != empty 
        
        return empty_sol_tracker, fig






