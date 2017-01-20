#####################################################
# Software License:                                 #
# --------------------------------------------------#
# The Artistic License 2.0                          #
#                                                   #
#       Copyright (c) 2016, Daniel Santoyo Gomez.   #
#                                                   #
# contact: daniel.santoyo@gmx.com                   #
#####################################################
from lib_grafica.game_constants import *


class Chunk:
    def __init__(self, index):
        self.id = index
        self.matrice = None  # {}
        self.keys_actives = []  # chiavi delle matrici attive????
        self.DEPTH = 0
        self.HEIGHT = 0
        self.WIDTH = 0

    def __repr__(self):
        t = "CHUNK\n"
        t += "\tID:" + str(self.id) + '\n'
        t += "\tpiani_matrice: " + str(len(self.matrice)) + '\n'
        for z in xrange(self.DEPTH):
            t += ("z: " + str(z)).center(80, '-') + '\n'
            for y in xrange(self.HEIGHT):
                for x in xrange(self.WIDTH):
                    t += self.matrice[z][y][x]
                t += '\n'
        return t

    def carica_matrice(self, matrice_pkl):
        self.matrice = matrice_pkl
        self.DEPTH = len(matrice_pkl)
        self.HEIGHT = len(matrice_pkl[0])
        self.WIDTH = len(matrice_pkl[0][0])
        for z in xrange(self.DEPTH):
            for y in xrange(self.HEIGHT):
                for x in xrange(self.WIDTH):
                    if walkable(self.matrice[z][y][x][0]):
                        self.matrice[z][y][x] = FREE
