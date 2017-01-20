####################################################
# Software License:                                 #
# --------------------------------------------------#
# The Artistic License 2.0                          #
#                                                  #
#       Copyright (c) 2016, Daniel Santoyo Gomez.  #
#                                                  #
# contact: daniel.santoyo@gmx.com                   #
####################################################
from random import randint

from lib_grafica.game_constants import *


class Pathfinder:
    # '''pathfinder class to manage the paths on the game. use Wavefront'''

    def __init__(self):
        print "[PATHFINDER]: creation"
        self.wf_matrix = {}
        self.DEPTH = 0
        self.HEIGHT = 0
        self.WIDTH = 0

    def explore_matrix(self, what, quote=0):
        # '''search in the matrix a value and returns a counter of tath value'''
        counter = 0
        if quote != 0:
            for y in xrange(self.HEIGHT):
                for x in xrange(self.WIDTH):
                    if self.wf_matrix[quote][y][x] == what:
                        counter += 1
            return counter
        for z in xrange(self.DEPTH):
            for y in xrange(self.HEIGHT):
                for x in xrange(self.WIDTH):
                    if self.wf_matrix[z][y][x] == what:
                        counter += 1
        return counter

    def found_value(self, x, y, z, value):
        # funzione self.found_value(x,y,z,cosa) return True se si trova False se errore oppure non trova...
        if x < 0 or x >= self.WIDTH:
            return False
        if y < 0 or y >= self.HEIGHT:
            return False
        if z < 0 or z >= self.DEPTH:
            return False
        if self.wf_matrix[z][y][x] == value:
            return True
        return False

    def write_on_matrix(self, x, y, z, value):
        # flag = False
        mod = False  # controllo per controllare se c'e' un bloccco...
        values = [-1, 1]
        for v in values:
            if self.found_value(x + v, y, z, FREE):
                self.wf_matrix[z][y][x + v] = str(value + 1)
                mod = True
            # flag = self.found_value(x+v,y,z,'G')or flag
            if self.found_value(x + v, y, z, 'v'):
                if self.found_value(x + v, y, z - 1, FREE):
                    self.wf_matrix[z - 1][y][x + v] = str(value + 1)
                    mod = True
                    # flag = self.found_value(x+v,y,z-1,'G')or flag
            if self.found_value(x + v, y, z, '^'):
                if self.found_value(x + v, y, z + 1, FREE):
                    self.wf_matrix[z + 1][y][x + v] = str(value + 1)
                    mod = True
                    # flag = self.found_value(x+v,y,z+1,'G')or flag
        for v in values:
            if self.found_value(x, y + v, z, FREE):
                self.wf_matrix[z][y + v][x] = str(value + 1)
                mod = True
            # flag = self.found_value(x,y+v,z,'G')or flag
            if self.found_value(x, y + v, z, 'v'):
                if self.found_value(x, y + v, z - 1, FREE):
                    self.wf_matrix[z - 1][y + v][x] = str(value + 1)
                    mod = True
                    # flag = self.found_value(x,y+v,z-1,'G')or flag
            if self.found_value(x, y + v, z, '^'):
                if self.found_value(x, y + v, z + 1, FREE):
                    self.wf_matrix[z + 1][y + v][x] = str(value + 1)
                    mod = True
                    # flag = self.found_value(x+v,y,z+1,'G')or flag
        return mod

    def create_wf_matrix(self, matrix):
        # '''create a wavefront matrix'''
        for k in matrix.keys():
            self.wf_matrix[k] = []
            for j in matrix[k]:
                self.wf_matrix[k].append([])
                for i in j:
                    self.wf_matrix[k][-1].append(i)
        self.DEPTH = len(self.wf_matrix)
        self.HEIGHT = len(self.wf_matrix[0])
        self.WIDTH = len(self.wf_matrix[0][0])
        # --------------------------------------------------#
        # scegli un valore casuale nella matrice piu' alta
        x = randint(0, W_WORLD - 1)
        y = randint(0, H_WORLD - 1)
        z = max(self.wf_matrix.keys())
        num_spaces = self.explore_matrix(FREE, z)
        while num_spaces == 0:
            z -= 1
            num_spaces = self.explore_matrix(FREE, z)
        while True:
            if self.wf_matrix[z][y][x] == FREE:
                break
            x = randint(0, W_WORLD - 1)
            y = randint(0, H_WORLD - 1)
        # --------------------------------------------------#
        # aggiusta i bordi dei piani, v ^ e i tile di acqua
        values = [-1, 1]
        for k in xrange(self.DEPTH):
            for j in xrange(self.HEIGHT):
                for i in xrange(self.WIDTH):
                    for v in values:  # T_DOWN
                        if self.found_value(i, j, k, FREE) and self.found_value(i + v, j, k,
                                                                                T_VOID) and self.found_value(i + v, j,
                                                                                                             k - 1,
                                                                                                             FREE):
                            self.wf_matrix[k][j][i + v] = T_DOWN
                        if self.found_value(i, j, k, FREE) and self.found_value(i, j + v, k,
                                                                                T_VOID) and self.found_value(i, j + v,
                                                                                                             k - 1,
                                                                                                             FREE):
                            self.wf_matrix[k][j + v][i] = T_DOWN

                    for v in values:  # T_UP
                        if self.found_value(i, j, k, FREE) and \
                                self.found_value(i, j, k + 11, FREE) and \
                                self.found_value(i + v, j, k, T_HIDE) and \
                                self.found_value(i + v, j, k + 1, FREE):
                            self.wf_matrix[k][j][i + v] = T_UP
                        if self.found_value(i, j, k, FREE) and self.found_value(i, j, k + 1, FREE) and self.found_value(
                                i, j + v, k, T_HIDE) and self.found_value(i, j + v, k + 1, FREE):
                            self.wf_matrix[k][j + v][i] = T_UP
                    if self.wf_matrix[k][j][i] == T_ACQUA:
                        self.wf_matrix[k][j][i] = T_HIDE
                    if k < Z_SEA:
                        if self.wf_matrix[k][j][i] == FREE:
                            self.wf_matrix[k][j][i] = T_HIDE

        # --------------------------------------------------#
        # popola la matrice con il Wavefront
        start = 0
        self.wf_matrix[z][y][x] = start

        for k in xrange(self.DEPTH):
            for j in xrange(self.HEIGHT):
                for i in xrange(self.WIDTH):
                    if self.wf_matrix[k][j][i] == start:
                        self.write_on_matrix(i, j, k, start)
                        index = 1
        print "[PATHFINDER]:==== creation of wavefront map ==================="
        while True:
            mod = False
            for k in xrange(self.DEPTH):
                for j in xrange(self.HEIGHT):
                    for i in xrange(self.WIDTH):
                        if self.wf_matrix[k][j][i] == str(index):
                            mod = self.write_on_matrix(i, j, k, index) or mod
            index += 1
            if not mod:
                break

    def next_step(self, x, y, z, index):
        # '''go back searching index-1'''
        values = [-1, 1]
        for v in values:
            if self.found_value(x + v, y, z, index):
                path = (x + v, y, z)
                return path
            if self.found_value(x + v, y, z, '^'):
                if self.found_value(x + v, y, z + 1, index):
                    path = (x + v, y, z + 1)
                    return path
            if self.found_value(x + v, y, z, 'v'):
                if self.found_value(x + v, y, z - 1, index):
                    path = (x + v, y, z - 1)
                    return path
        for v in values:
            if self.found_value(x, y + v, z, index):
                path = (x, y + v, z)
                return path
            if self.found_value(x, y + v, z, '^'):
                if self.found_value(x, y + v, z + 1, index):
                    path = (x, y + v, z + 1)
                    return path
            if self.found_value(x, y + v, z, 'v'):
                if self.found_value(x, y + v, z - 1, index):
                    path = (x, y + v, z - 1)
                    return path
        return False

    def get_path(self, where):
        # '''handles the request for a path from start(x,y,z) to goal(x,y,z)'''
        if len(where) == 1:
            return []
        xstart, ystart, zstart = [x for x in where[0]]
        xgoal, ygoal, zgoal = [x for x in where[1]]
        print "xgoal, ygoal, zgoal: ", xgoal, ygoal, zgoal
        x = xstart
        y = ystart
        z = zstart
        final_index = self.wf_matrix[zgoal][ygoal][xgoal]
        # print "final index", final_index
        index = self.wf_matrix[zstart][ystart][xstart]
        delta = 1 if (int(final_index) - int(index)) > 0 else -1
        path = []
        while final_index != index:
            index = str(int(self.wf_matrix[z][y][x]) + delta)
            [x, y, z] = self.next_step(x, y, z, index)
            if (x, y, z) not in path:
                path.append((x, y, z))
                # index = str(int(self.wf_matrix[z][y][x]) + delta)

        if x == xgoal and y == ygoal and z == zgoal:
            return path
        # search for final path
        for t in xrange(10):  # 10 tentativi per trovare il percorso semplice
            if x != xgoal:
                delta = 1 if (x - xgoal) > 0 else -1
                x -= delta
                index = self.wf_matrix[z][y][x]
                if index.isdigit():
                    path.append((x, y, z))
                    continue
                else:
                    x += delta
            if y != ygoal:
                delta = 1 if (y - ygoal) > 0 else -1
                y -= delta
                index = self.wf_matrix[z][y][x]
                if index.isdigit():
                    path.append((x, y, z))
                    continue
                else:
                    y += delta
            if x == xgoal and y == ygoal and z == zgoal:
                break
        print "final path ", path
        return path
