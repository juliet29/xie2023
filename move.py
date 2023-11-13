from helpers import *
from actions import *


class Move:
    def __init__(self, ni:NodeProperties, nj:NodeProperties, data:dict, debug=False) -> None:
        self.mag = None
        self.ni = ni
        self.nj = nj
        self.constraining_domain = data["constraining_domain"]
        self.problem_face = data["problem_face"]
        self.constraining_face = data["constraining_face"]
        self.move_axis = self.problem_face.axis
        self.debug = debug
        pass


    
    def construct_move(self):
        # domain of i ... need to check this..
        if len(self.constraining_face) > 1:
            moving_domain = self.constraining_face[0].state[-1]
            moving_domain2 = self.constraining_face[1].state[-1]
        else:
            moving_domain = self.constraining_face.state[-1]

        constrain_domain = self.constraining_domain
        
        # last domain of j 
        prob_domain = self.problem_face.state[-1] 


        m1 = assess_move(constrain_domain, prob_domain)
        m2 = assess_move(moving_domain, constrain_domain)
        self.mag = m1*(-1) + m2
        
        if moving_domain2:
            m3 = assess_move(moving_domain2, constrain_domain)
            

        if self.debug:
            ic(constrain_domain, prob_domain, m1)
            ic(moving_domain, constrain_domain, m2)
            if moving_domain2:
                ic(moving_domain2, constrain_domain, m3)
                



    
    def apply_move(self):
        self.construct_move()
        for face in self.ni.faces.face_list:
            if face.axis == self.move_axis:
                # old domain is based on the last domain of this face 
                old_domain = face.state[-1]
                new_domain = [d + self.mag for d in list(range(*old_domain))]
                face.reset_face()
                face.addConstraint(cn.InSetConstraint(new_domain))
                try:
                    face.state_update() 
                except NoSolError:
                    # TODO assess failure..  or try a different process..
                    raise AdjustmentError("Moving i failed")   
                
                
    







def get_smallest_dif(a,b):
    res = np.array(a) - np.array(b)
    res_abs = [abs(i) for i in res]
    v = min(res_abs)
    mag = res[res_abs.index(v)]
    return mag

def assess_move(a,b):
    assert len(a) <= 2 and len(b) <= 2, "Arrays are the wrong size"
    # ic(a, b)
    # ic(len(a), len(b))

    if len(a) == 1 and len(b) == 1:
        mag= (a[0] - b[0])*-1
           
    elif len(b) == 2  and len(a) == 2:
        mag1 = get_smallest_dif(a,b[0])
        mag2 = get_smallest_dif(a, b[1])
        # ic(mag1, mag2)
        mag = mag1 if abs(mag1) > abs(mag2) else mag2
        
    else:
        mag = get_smallest_dif(a,b)
    # else:
    #     raise RuntimeError("Wrong domain sizes")
    # ic(mag)
    return mag