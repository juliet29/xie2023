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
    

def create_face_vars():
    problem = cn.Problem()
    x_range = range(0, 100)
    y_range = range(0,100)
    problem.addVariable("x", x_range)
    problem.addVariable("y", y_range)
    return problem


class NodeFaces():
    def __init__(self):
        self.faceN = create_face_vars()
        self.faceS = create_face_vars()
        self.faceE = create_face_vars()
        self.faceW = create_face_vars()
        self.faceT = create_face_vars()
        self.faceB = create_face_vars()

    


