import numpy as np
import constraint as cn

import warnings

from enum import Enum
import plotly.express as px
from icecream import ic
ic.configureOutput(includeContext=True)


THRESHOLD = 1
COLORWAY = ["#25283d","#8f3985","#ee6c4d","#07beb8","#f5b841"]
#px.colors.sequential.Jet
#['#702632', '#A4B494', '#495867', '#912F40', "#81909E", "#F4442E", "#DB7C26", "#BB9BB0"]
    

class NoSolError(Exception):
    pass

class ActionError(Exception):
    pass

class AdjustmentError(Exception):
    pass

class SpatialRel(Enum):
    """Spatial relation"""
    NO_RELATION = 0
    ADJACENT = 1
    INTERSECTING = 2
    CONTAINS = 3
    CONTAINING = 4

class Axes(Enum):
    X = 0
    Y = 1
    Z = 2

class Orient(Enum):
    """Orientation"""
    NONE = 0
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    TOP = 5
    BOTTOM = 6

    @property
    def axis(self):
        axes = [None, Axes.Y, Axes.Y, Axes.X, Axes.X, Axes.Z, Axes.Z]
        d = {ix:ax for ix, ax in enumerate(axes)}

        return d[self.value]
    
    @property
    def basis(self):
        axes = [None, False, True, False, True, False, True]
        d = {ix:ax for ix, ax in enumerate(axes)}

        return d[self.value]
    
    @property
    def partner(self):
        axes = [None, self.SOUTH, self.NORTH, self.WEST, self.EAST, self.BOTTOM, self.TOP]
        d = {ix:ax for ix, ax in enumerate(axes)}

        return d[self.value]

class Face(cn.Problem):
    def __init__(self, axis: Axes, name: str,  normal: Orient):
        cn.Problem.__init__(self)
        self.nrange = range(0, 50)
        self.addVariable(axis, self.nrange)
        self.axis = axis
        self.name = name
        self.viz_data = {}
        self.viz_type = "shape"
        self.partner = None
        self.normal = normal
        self.sols = None
        self.state = []
        self.parent_node = None
        self.state_update()
    
    def get_face_sols(self):
        self.full_name = f"{self.parent_node}.{self.name}" # TODO fix

        self.sols = get_problems_sols(self)
        if not self.sols:
            self.go_to_last_sol()
            raise NoSolError(f"No sols for {self.parent_node}.{self.name} ")
        self.orig_sols = True if set(self.sols) == set(self.nrange) else False
        return self.sols

    def state_update(self):
        if self.get_face_sols():
            self.state.append(domain_range(self.sols))
        return 
    
    def reset_face(self):
        self.reset()
        self.addVariable(self.axis, self.nrange)

    def go_to_last_sol(self):
        self.reset_face()
        self.addConstraint(cn.InSetConstraint(self.state[-1]))
    
    def create_viz_data(self):
        v = VisualHelpers()
        res = v.create_viz_data(self)
        if res:
            self.viz_data, self.viz_type = res



    

class NodeFaces():
    def __init__(self, parent_node):
        self.faceN = Face(Axes.Y, "faceN", Orient.NORTH)
        self.faceS = Face(Axes.Y, "faceS", Orient.SOUTH)
        self.faceE = Face(Axes.X, "faceE", Orient.EAST)
        self.faceW = Face(Axes.X, "faceW", Orient.WEST)
        self.faceT = Face(Axes.Z, "faceT", Orient.TOP)
        self.faceB = Face(Axes.Z, "faceB", Orient.BOTTOM)
        self.face_list = [self.faceN, self.faceS, self.faceE, self.faceW, self.faceT, self.faceB]
        self.parent_node = parent_node
        self.assign_relations()

    def assign_relations(self):
        f=lambda l:l and l[1::-1]+f(l[2:])
        flip_faces = f(self.face_list)
        for face1, face2 in zip(self.face_list, flip_faces):
            face1.partner = face2

        for ix, face in enumerate(self.face_list):
            face.parent_node = self.parent_node

    def get_node_sols(self): 
        face_sols = {}
        for face in self.face_list:
            curr_sols = face.get_face_sols()
            if len(curr_sols) < 1:
                face_sols[face.name] = "No Solutions" 
                # TODO rais error 
            else:
                face_sols[face.name] = domain_range(curr_sols)
    
        return face_sols

class NodeProperties:
    def __init__(self, name="Test", length=1, width=1, height=1, level_height=0, index=0):
        self.name = name
        self.length = length # E-W
        self.width = width # N-S 
        self.height = height # T-B
        self.level_height = level_height
        self.index = index
        # TODO extend so that can account for minimal node infomation ie -> add functions..

        # values that start as the same for all nodes 
        self.pos = np.zeros(3)
        self.faces = NodeFaces(self.index)
        self.constrained = False # not all axes are fixed 

        # values that are updated over time 
        self.correct_nb = []




class VisualHelpers():
    def create_viz_data(self, face: Face): 
        domain = list(range(50))
        sols = face.get_face_sols()
        d = None
        type = None
        if len(sols) < 1:
            return None
        
        elif len(sols) == 1:
            type = "lines"
            y = domain
            x = sols*len(domain)
            if face.axis == Axes.X:
                d = {"y" : y, "x": x}
                # return d, type
            elif face.axis == Axes.Y:
                d = {"y" : x, "x": y}
                # return d, type
        else:
            type = "shape"
            if face.axis == Axes.X:
                y = domain
                x1 = [min(sols)]*len(domain)
                x2 = [max(sols)]*len(domain)
                d1 = {"y" : y,
                    "x" : x1,
                    "fill":"tonextx"}
                d2 = {"y" : y,
                    "x" : x2,}
                d = {"d1": d1, "d2": d2}
            
            elif face.axis == Axes.Y:
                x = domain
                y1 = [min(sols)]*len(domain)
                y2 = [max(sols)]*len(domain)
                d1 = {"x" : x,
                    "y" : y1,
                    "fill":"tonexty"}
                d2 = {"x" : x,
                    "y" : y2,}
                d = {"d1": d1, "d2": d2}
        return d, type



def domain_range(domain: list):
    if len(domain) == 1:
        return (domain)
    elif len(domain) > 1:
        return (min(domain), max(domain))
    
def get_problems_sols(p: cn.Problem):
    return [list(z.values())[0] for z in p.getSolutions()]

def variable_constraint(x, face_i1:Face, face_i2:Face, dist: int, debug=False):
    set1 = [ix - dist + THRESHOLD for ix  in face_i1.sols]
    set2 = [ix - THRESHOLD for ix in face_i2.sols]
    
    valid_len = len(set1) if len(set1) < len(set2) else len(set2)
    for i in list(range(valid_len)):
        if set1[i] <= x <= set2[i]:
            return x









# def create_face_vars():
#     problem = cn.Problem()
#     x_range = range(0, 100)
#     y_range = range(0,100)
#     problem.addVariable(Axes.Z, x_range)
#     problem.addVariable(Axes.Y, y_range)
#     return problem


# class NodeFaces():
#     def __init__(self):
#         self.faceN = create_face_vars()
#         self.faceS = create_face_vars()
#         self.faceE = create_face_vars()
#         self.faceW = create_face_vars()
#         self.faceT = create_face_vars()
#         self.faceB = create_face_vars()



        

    


