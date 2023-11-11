from helpers import *

class Actions():
    # SET MATCHING FACES ----------
    def __set_matching_face(self, f1: Face, f2:Face, prop):
        poss_sols = [[*sol.values()][0] + prop for sol in f2.getSolutionIter()]
        return f1.addConstraint(cn.InSetConstraint(poss_sols))

    def set_face_relation(self, n: NodeProperties, ax: Axes, rel_type="SWB"):
        d = {
            "NET": {
            Axes.Y: ("faceN", "faceS", n.width),
            Axes.X: ("faceE", "faceW", n.length),
            Axes.Z: ("faceT", "faceB", n.height)
        },
            "SWB":             
            {Axes.Y: ("faceS", "faceN", n.width),
            Axes.X: ("faceW", "faceE", n.length),
            Axes.Z: ("faceB", "faceT", n.height)
            }
        } # TODO might remove this from dict for speed purposes later

        f1, f2, prop = [*d[rel_type][ax]]
        return self.__set_matching_face(n.faces.__getattribute__(f1), n.faces.__getattribute__(f2), prop)





    # def __set_matching_face(self, f1: Face, f2:Face, prop):
    #     poss_sols = [[*sol.values()][0] + prop for sol in f2.getSolutionIter()]
    #     return f1.addConstraint(cn.InSetConstraint(poss_sols))


    # SET ORIENTATION RELATIONSHIPS --------------
    def __add_orientation_constraint(self, f1: Face, f2: Face):
        min_f2 = min([abs(list(s.values())[0]) for s in f2.getSolutions()])
        return f1.addConstraint(lambda x: x < min_f2) # TODO FIX, should be like a set?


    def orient_ij(self, ni: NodeProperties, nj: NodeProperties, orient: Orient):
        ni = ni.faces
        nj = nj.faces
        d = {
            Orient.SOUTH : (nj.faceN, ni.faceS),
            Orient.WEST : (nj.faceE, ni.faceW),  
            Orient.BOTTOM : (nj.faceT, ni.faceB),

        }

        self.__add_orientation_constraint(*d[orient])
        return                 