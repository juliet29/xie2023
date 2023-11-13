from helpers import *
from visuals import * 



class Actions:
    def __init__(self, ni, nj, orient, rel, debug=False):
        self.ni:NodeProperties = ni
        self.nj:NodeProperties = nj
        self.orient:Orient = orient
        self.rel: SpatialRel = rel
        self.debug = debug

            
    def primary_relate(self):
        fi = None
        fj = None
        if self.orient == Orient.NORTH:
            fi = self.ni.faces.faceN
            fj = self.nj.faces.faceS
        elif self.orient == Orient.SOUTH:
            fi = self.ni.faces.faceS
            fj = self.nj.faces.faceN
        elif self.orient == Orient.EAST:
            fi = self.ni.faces.faceE
            fj = self.nj.faces.faceW
        elif self.orient == Orient.WEST:
            fi = self.ni.faces.faceW
            fj = self.nj.faces.faceE
        else:
            ic("wrong orient")
            return False

        fj.addConstraint(cn.InSetConstraint(fi.sols))

        return fi, fj, domain_range(fi.sols)
    
            
    def secondary_relate(self, face_j, face_i1, face_i2):
        prop = self.nj.length if face_j.axis == Axes.X else self.nj.width
        params = [face_i1, face_i2, prop] # TODO fix , might be width..
        
        set1 = [ix - prop + THRESHOLD for ix  in face_i1.sols]
        set2 = [ix - THRESHOLD for ix in face_i2.sols]

        if self.debug:
            ic("yyy", face_i1.sols, face_i2.sols, set1, set2, face_j.getSolutions())


        face_j.addConstraint(lambda x: variable_constraint(x,*params, debug=self.debug))


        # get best case domain 
        p = cn.Problem()
        p.addVariable("x", face_j.nrange)
        p.addConstraint(lambda x: variable_constraint(x, *params))
        best_domain = domain_range(get_problems_sols(p))
        return (face_i1, face_i2), face_j, best_domain


    def relate_process(self, face_j, face_i1, face_i2):
        try:
            facei, facej, domain = self.primary_relate()
            facej.state_update()
        except NoSolError:
                res = self.assess_failure(facei, facej, domain)
                warnings.warn("Primary relate failed")
                raise ActionError("Primary relate failed")
        

        try:
            facei, facej, domain = self.secondary_relate(face_j, face_i1, face_i2)
            facej.state_update()
        except NoSolError:
                warnings.warn("Secondary relate failed")
                res = self.assess_failure(facei, facej, domain)
                # starting here bc source of 3-1 failure 
                
                return res
                # raise ActionError("Secondary relate failed")
        
        # ic("setting faces because 2nd rel no fail")
        self.set_face_rel()
        self.final_check()

      
        
    

    def spatial_relate_ij(self):
        if self.rel == SpatialRel.ADJACENT or self.rel == SpatialRel.INTERSECTING: 
            ch = True
            if self.orient == Orient.NORTH or self.orient == Orient.SOUTH:
                res = self.relate_process(self.nj.faces.faceW, self.ni.faces.faceW, self.ni.faces.faceE)

            if self.orient == Orient.EAST or self.orient == Orient.WEST:
                res = self.relate_process(self.nj.faces.faceS, self.ni.faces.faceS, self.ni.faces.faceN) 
          
        else:
            ic(f"Action for {self.orient} not defined")
            pass

        return res



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
                except NoSolError:
                    self.assess_failure(face.partner, face, domain_range(poss_sols))
                    raise ActionError("Match faces failed")
        return 

    
    def final_check(self, nj:NodeProperties=None):
        node = nj if not self.nj else self.nj
        for face in [node.faces.faceW, node.faces.faceS, node.faces.faceB]:
            face.get_face_sols()
            face.partner.get_face_sols()
            try:
                assert(min(face.sols) <= min(face.partner.sols))
            except AssertionError("Face order check failed"):
                ic(node.index, face.name, face.partner.name)
                pass



    def assess_failure(self, facei, facej, domain):
        if self.nj and self.ni: # TODO doesnt work for first node ...
            if self.debug:
                ic("\n")
                ic(f"Face tried to move: {facej.full_name}")
                ic(f"Previous states: {facej.state} ")
                ic(f"Constraining domain: {domain}")
                try:
                    ic(f"Constraining face: {facei.full_name}")
                    ic(f"Previous states of constraining face: {facei.state} ")
                except AttributeError:
                    ic(f"Constraining face: {facei[0].full_name}")
                    ic(f"Constraining face: {facei[1].full_name}")
                    ic(f"Previous states of constraining face: {facei[0].state} ")
                    ic(f"Previous states of constraining face: {facei[1].state} ")
                
                ic(f"Node relation: {self.ni.index}-{self.nj.index} {self.orient}")

            move_package = {
                "constraining_domain": domain, 
                "problem_face": facej,
                "constraining_face": facei
            }

            return move_package


