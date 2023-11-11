from helpers import *

class Actions():
    # SET MATCHING FACES ----------
    def __set_matching_face(self, f1: Face, f2:Face, prop):
        poss_sols = [[*sol.values()][0] + prop for sol in f2.getSolutionIter()]
        return f1.addConstraint(cn.InSetConstraint(poss_sols))

    def set_face_relation(self, n: NodeProperties, ax: Axes):
        # TODO  pass in an axis here, and Orient should have axis property 
        d = {
            Axes.Y: ("faceN", "faceS", n.width),
            Axes.X: ("faceE", "faceW", n.length),
            Axes.Z: ("faceT", "faceB", n.height)
        }

        f1, f2, prop = [*d[ax]]
        return self.__set_matching_face(n.faces.__getattribute__(f1), n.faces.__getattribute__(f2), prop)








    # SET ORIENTATION RELATIONSHIPS --------------
    def __add_orientation_constraint(self, f1: Face, f2_val: int):
        return f1.addConstraint(lambda x: x > f2_val) # TODO FIX, should be like a set?


    def orient_ij(self, ni: NodeProperties, nj: NodeProperties, orient: Orient):
        ni = ni.faces
        nj = nj.faces
        d = {
            Orient.SOUTH : (nj.faceN, ni.faceS.get_face_sol()),
            Orient.WEST : (nj.faceE, ni.faceW.get_face_sol()),  
            Orient.BOTTOM : (nj.faceT, ni.faceB.get_face_sol())
        }

        self.__add_orientation_constraint(*d[orient])
        return                 