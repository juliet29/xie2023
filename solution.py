import matplotlib.pyplot as plt
import numpy as np

import networkx as nx
import constraint as cn

from operator import itemgetter

from helpers import *
from setup import *
from actions import * 

class Solution(SetUp):
    def __init__(self):
        SetUp.__init__(self)

    def set_start_node():
        # get the first node from the tree 
        # set S, W, B => 0 
        # constain matching faces 
        pass