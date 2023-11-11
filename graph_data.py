import numpy as np

from helpers import *


NODE_DATA = {
    "room_names" : ["entrance", "rest_space", "dining_space", "platform"],
    "length" : [3,3,3,1],
    "width" : [3,3,3,1],
    "height" : [3,3,3,2],
    "lev_height" : [0,0,1,1]
}

SPACE_REL = np.vectorize(lambda x: SpatialRel(x))(np.array([
    [0, 1, 1, 3],
    [1,0,2,1],
    [1,2,0,1],
    [4,1,1,0]
]))

ORIENTATIONS = np.vectorize(lambda x: Orient(x))(np.array([
    [0, 1, 0, 0],
    [2, 0, 0, 0],
    np.zeros(4, np.int8),
    np.zeros(4, np.int8)
]))


