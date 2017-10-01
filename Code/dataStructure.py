# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 12:42:42 2016

@author: Licia AMICHI

"""
import numpy as np



class Node:
    def __init__(self, identifiant, matrix, t, nbHop, parent):
        self.identifiant = identifiant
        self.matrix = matrix
        self.took = t
        self.nbHop = nbHop
        self.parent = parent
        self.son = -1

