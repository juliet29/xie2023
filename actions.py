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

        return f2, domain_range(f1.sols)
    
            
    def secondary_relate(self, face_j, face_i1, face_i2):
        params = [face_i1, face_i2, self.nj.length]
        face_j.addConstraint(lambda x: variable_constraint(x,*params ))

        # get best case domain 
        p = cn.Problem()
        p.addVariable("x", face_j.nrange)
        p.addConstraint(lambda x: variable_constraint(x, *params))
        best_domain = domain_range(get_problems_sols(p))
        return face_j, best_domain


    def relate_process(self, face_j, face_i1, face_i2):
        try:
            face, domain = self.primary_relate()
            face.state_update()
        except NoSolError:
                self.assess_failure(face, domain)
                raise RuntimeError("Primary relate failed")

        try:
            face, domain = self.secondary_relate(face_j, face_i1, face_i2)
            face.state_update()
        except NoSolError:
                self.assess_failure(face, domain)
                raise RuntimeError("Secondary relate failed")

        self.set_face_rel()
        self.final_check()
                
        return True
    

    def spatial_relate_ij(self, ni, nj, orient, rel):
        self.ni = ni
        self.nj = nj
        self.orient = orient
        self.rel = rel

        if self.rel == SpatialRel.ADJACENT or self.rel == SpatialRel.INTERSECTING: 
            ch = True
            if self.orient == Orient.NORTH or self.orient == Orient.SOUTH:
                self.relate_process(self.nj.faces.faceW, self.ni.faces.faceW, self.ni.faces.faceE)

            if self.orient == Orient.EAST or self.orient == Orient.WEST:
                self.relate_process(self.nj.faces.faceS, self.ni.faces.faceS, self.ni.faces.faceN) 
          
        else:
            ic(f"Action for {orient} not defined")
            pass



    def set_face_rel(self, nj:NodeProperties=None):
        node = nj if not self.nj else self.nj
        # if face vals are not the default, set the match face 
        d = {Axes.Y: node.width, Axes.X: node.length, Axes.Z: node.height}
        
        for face in node.faces.face_list:
            prop = d[face.axis]
            if not face.sols:
                face.get_face_sols()
            if not face.orig_sols:
                if not face.normal.basis:
                    prop*=-1
                poss_sols = [[*sol.values()][0] + prop for sol in face.getSolutionIter()]
                face.partner.addConstraint(cn.InSetConstraint(poss_sols))
                try: 
                    face.partner.state_update()
                except:
                    ic("Match faces failed")
                    self.assess_failure(face.partner, domain_range(poss_sols))
        return 

    
    def final_check(self, nj:NodeProperties=None):
        node = nj if not self.nj else self.nj
        for face in [node.faces.faceW, node.faces.faceS, node.faces.faceB]:
            face.get_face_sols()
            face.partner.get_face_sols()
            try:
                assert(min(face.sols) <= min(face.partner.sols))
            except AssertionError:
                ic("face order check failed")
                ic(node.index, face.name, face.partner.name)
                pass



    def assess_failure(self, face, domain):
        if self.nj and self.ni: # TODO doesnt work for first node ...
            ic("\n")
            ic(f"Face tried to move: {self.nj.index}.{face.name}")
            ic(f"Previous states: {face.state} ")
            ic(f"Constraining domain: {domain}")
            ic(f"Node relation: {self.ni.index}-{self.nj.index} {self.orient}")


