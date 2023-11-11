import numpy as np
import constraint as cn

from enum import Enum


class SpatialRel(Enum):
    """Spatial relation"""
    NO_RELATION = 0
    ADJACENT = 1
    INTERSECTING = 2
    CONTAINS = 3
    CONTAINING = 4

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
    def vector(self):
        orient_vectors = {
            0: (0,0,0),
            1: (0,1,0), # north
            2: (0,-1,0), # south
            3: (1,0,0), # east
            4: (-1,0,0), # west
            5: (0,0,1), # top
            6: (0,0,-1) # bottom
        }
        orient_vectors = { k:np.array(v) for (k,v) in orient_vectors.items()}

        return orient_vectors[self.value]

class Face(cn.Problem):
    def __init__(self, face):
        cn.Problem.__init__(self)
        nrange = range(-100, 100)
        self.addVariable(face, nrange)
        self.axis = face

    def get_face_sol(self):
        assert len(self.getSolutions()) == 1, "Not a unique solution"
        self.solution = [*self.getSolution().values()][0]
        return self.solution
    

class NodeFaces():
    def __init__(self):
        self.faceN = Face("y")
        self.faceS = Face("y")
        self.faceE = Face("x")
        self.faceW = Face("x")
        self.faceT = Face("z")
        self.faceB = Face("z")
    
    def see_curr_sols(self): # TODO clean this up 
        face_sols = {}
        for face in vars(self):
            curr_sols = [list(z.values())[0] for z in self.__getattribute__(face).getSolutions()]
            if len(curr_sols) < 1:
                face_sols[face] = "No Solutions"

            elif len(curr_sols) == 1:
                face_sols[face] = curr_sols[0]
            else:
                face_sols[face] = {
                    "min": min(curr_sols),
                    "max": max(curr_sols),
                }
    
        return face_sols

class NodeProperties:
    def __init__(self, name="Test", length=1, width=1, height=1, level_height=0):
        self.name = name
        self.length = length
        self.width = width
        self.height = height
        self.level_height = level_height
        self.pos = np.zeros(3)
        self.faces = NodeFaces()

        # TODO extend so that can account for minimal node infomation 













# def create_face_vars():
#     problem = cn.Problem()
#     x_range = range(0, 100)
#     y_range = range(0,100)
#     problem.addVariable("x", x_range)
#     problem.addVariable("y", y_range)
#     return problem


# class NodeFaces():
#     def __init__(self):
#         self.faceN = create_face_vars()
#         self.faceS = create_face_vars()
#         self.faceE = create_face_vars()
#         self.faceW = create_face_vars()
#         self.faceT = create_face_vars()
#         self.faceB = create_face_vars()



        

    


