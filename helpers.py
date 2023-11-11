import numpy as np
import constraint as cn

from enum import Enum
from visuals import *
import plotly.express as px


COLORWAY = ["#25283d","#8f3985","#ee6c4d","#07beb8","#f5b841"]
#px.colors.sequential.Jet
#['#702632', '#A4B494', '#495867', '#912F40', "#81909E", "#F4442E", "#DB7C26", "#BB9BB0"]

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
    def __init__(self, axis: Axes, name: str):
        cn.Problem.__init__(self)
        self.nrange = range(0, 50)
        self.addVariable(axis, self.nrange)
        self.axis = axis
        self.name = name
        self.viz_data = {}
        self.viz_type = "shape"
    
    def get_face_sols(self):
        self.sols = [list(z.values())[0] for z in self.getSolutions()]
        self.orig_sols = True if set(self.sols) == set(self.nrange) else False
        self.len_sols = len(self.sols)
        return self.sols
    
    def create_viz_data(self):
        v = VisualHelpers()
        res = v.create_viz_data(self)
        if res:
            self.viz_data, self.viz_type = res


    # def get_face_sol(self):
    #     assert len(self.getSolutions()) == 1, "Not a unique solution"
    #     self.solution = [*self.getSolution().values()][0]
    #     return self.solution
    

class NodeFaces():
    def __init__(self):
        self.faceN = Face(Axes.Y, "faceN")
        self.faceS = Face(Axes.Y, "faceS")
        self.faceE = Face(Axes.X, "faceE")
        self.faceW = Face(Axes.X, "faceW")
        self.faceT = Face(Axes.Z, "faceT")
        self.faceB = Face(Axes.Z, "faceB")
        self.face_list = [self.faceN, self.faceS, self.faceE, self.faceW, self.faceT, self.faceB]
    
    def get_node_sols(self): # TODO clean this up 
        face_sols = {}
        for face in self.face_list:
            curr_sols = face.get_face_sols()
            if len(curr_sols) < 1:
                face_sols[face.name] = "No Solutions"

            elif len(curr_sols) == 1:
                face_sols[face.name] = curr_sols[0]
            else:
                face_sols[face.name] = {
                    "min": min(curr_sols),
                    "max": max(curr_sols),
                }
    
        return face_sols

class NodeProperties:
    def __init__(self, name="Test", length=1, width=1, height=1, level_height=0, index=0):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.level_height = level_height
        self.index = index
        # TODO extend so that can account for minimal node infomation ie -> add functions..


        self.pos = np.zeros(3)
        self.faces = NodeFaces()
        self.constrained = False # not all axes are fixed 


class VisualHelpers():
    def create_viz_data(self, face: Face): # TODO put this in the face class...
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
            x0 = min(sols)
            x1 = max(sols)
            y0 = min(domain) - 10
            y1 = max(domain) + 10
            if face.axis == Axes.X:
                d = {
                    "x0": x0,"x1": x1,"y0": y0,"y1": y1
                }
                # return d, type
            elif face.axis == Axes.Y:
                d = {
                    "y0": x0,"y1": x1,"x0": y0,"x1": y1
                }
        return d, type













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



        

    


