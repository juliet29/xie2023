from helpers import *


# SET MATCHING FACES ----------
def set_matching_face(f1: Face, f2:Face, prop):
    # TODO s is a member of SpatialUnitProperties
    poss_sols = [[*sol.values()][0] + prop for sol in f2.getSolutionIter()]
    return f1.addConstraint(cn.InSetConstraint(poss_sols))

def set_face_relation(n: NodeFaces, f: Face, s: NodeProperties):
    d = {
        "y": ("faceS", "faceN", s.width),
        "x": ("faceW", "faceE", s.length),
        "z": ("faceB", "faceT", s.height)
    }

    f1, f2, s = [*d[f.axis]]
    return set_matching_face(n.__getattribute__(f1), n.__getattribute__(f2), s)



# SET ORIENTATION RELATIONSHIPS --------------
def add_orientation_constraint(face1, face2_val):
    print(face1, face2_val)
    return face1.addConstraint(lambda x: x > face2_val)


def orient_ij(ni, nj, orient: Orient):
    d = {
        Orient.SOUTH : (nj.faceN, ni.faceS.get_face_sol()),
        Orient.WEST : (nj.faceE, ni.faceW.get_face_sol()),  
        Orient.BOTTOM : (nj.faceT, ni.faceB.get_face_sol())
    }

    add_orientation_constraint(*d[orient])
    return                 