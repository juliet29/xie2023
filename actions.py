from helpers import *
from visuals import * 


class Actions:
    def __init__(self):
        self.ni:NodeProperties = None
        self.nj:NodeProperties = None
        self.orient:Orient = None
        self.rel: SpatialRel

            
    def primary_relate(self):
        f1 = None
        f2 = None
        if self.orient == Orient.NORTH:
            f1 = self.ni.faces.faceN
            f2 = self.nj.faces.faceS
        elif self.orient == Orient.SOUTH:
            f1 = self.ni.faces.faceS
            f2 = self.nj.faces.faceN
        elif self.orient == Orient.EAST:
            f1 = self.ni.faces.faceE
            f2 = self.nj.faces.faceW
        elif self.orient == Orient.WEST:
            f1 = self.ni.faces.faceW
            f2 = self.nj.faces.faceE
        else:
            ic("wrong orient")
            return False

        f2.addConstraint(cn.InSetConstraint(f1.sols))

        return f2, f1
    
    
    def variable_constraint(self, x):
        set1 = [ix - self.nj.length + THRESHOLD for ix  in self.ni.faces.faceW.sols]
        set2 = [ix - THRESHOLD for ix in self.ni.faces.faceE.sols]

        valid_len = len(set1) if len(set1) < len(set2) else len(set2)
        for i in list(range(valid_len)):
            if set1[i] <= x <= set2[i]:
                return x
            
    def secondary_relate(self, face):
        face.addConstraint(lambda x: self.variable_constraint(x))



    def spatial_relate_ij(self, ni, nj, orient, rel):
        self.ni = ni
        self.nj = nj
        self.orient = orient
        self.rel = rel
        ic(self.orient, self.rel)
        if self.rel == SpatialRel.ADJACENT or self.rel == SpatialRel.INTERSECTING: 
            if self.orient == Orient.NORTH or self.orient == Orient.SOUTH:
                self.primary_relate()
                self.secondary_relate(self.nj.faces.faceW)
                

            if self.orient == Orient.EAST or self.orient == Orient.WEST:
                self.primary_relate()
                self.secondary_relate(self.nj.faces.faceS)
                
        else:
            pass


    def set_face_rel(self, nj:NodeProperties=None):
        if not self.nj:
            node = nj
        else:
            node = self.nj
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
            if not face.orig_sols: # TODO need stronger check here -> when all are adjusted might have issue 
                if face.normal.basis:
                    prop*=-1
                    print(prop, face.name)
                poss_sols = [[*sol.values()][0] + prop for sol in face.getSolutionIter()]
                face.partner.addConstraint(cn.InSetConstraint(poss_sols))

    
    def final_check(self, nj:NodeProperties=None):
        if not self.nj:
            node = nj
        else:
            node = self.nj
        for face in [node.faces.faceW, node.faces.faceS, node.faces.faceB]:
                print(node.index, face.name, face.partner.name)
                assert(min(face.sols) <= min(face.partner.sols))






