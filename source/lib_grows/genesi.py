# ###################################################
# Software License:                                 #
# --------------------------------------------------#
# genesi.py, a pygame library to create the images of the game.
# Copyright (C) 2016  Daniel Santoyo Gomez

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# contact: daniel.santoyo@gmx.com
import cPickle
import os.path
import threading
from random import randint

import pygame
from lib_eventi import oggetto
from lib_grafica.game_constants import *
from lib_scribi import scriba
from pygame import image as py_image

from perlin_noise import PerlinNoise


def miner_random(m):  # EDIT: da sistemare
    """
    :type m: miner
    """
    m.nome = scriba.nome_random(m.sesso)
    m.cognome = scriba.cognome_random()
    m.eta = randint(1, 50)
    m.vista = randint(8, 10)  # (3, 8)
    # vitalita = [1, 1, 1, 1, 2, 2, 3, 4, 5, 6, 6, 7, 8, 9, 10, 11, 12,\
    #  12, 13, 14, 14, 15, 16, 16, 17, 17, 18, 18, 18, 19, 19, 19, 20, 20,\
    #  20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 19, 19, 19, 19, 19, 18,\
    #  18, 18, 18, 18, 17, 17, 17, 16, 16, 16, 16, 15, 15, 15, 14, 14, 14,\
    #  13, 13, 13, 13, 12, 12, 12, 11, 11, 11, 11, 10, 10, 10, 9, 9, 9, 9,\
    #  9, 8, 8, 8, 8, 7, 7, 7, 7, 7, 6, 6, 6, 6]
    # n.vitalita = vitalita[n.eta]+randint(1,3)
    # n.salute = n.vitalita
    # forza = [1, 1, 1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,\
    #  16, 17, 18, 19, 19, 20, 20, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22,\
    #  22, 22, 22, 22, 21, 21, 21, 20, 20, 20, 19, 19, 18, 18, 17, 17, 16,\
    #  16, 15, 15, 14, 14, 13, 13, 12, 12, 11, 11, 10, 10, 9, 9, 9, 8, 8,\
    #  7, 7, 7, 6, 6, 5, 5, 5, 5, 4, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1]
    # n.forza = forza[n.eta]+randint(1,3)
    # t = 0
    # arr = []
    # for i in range(n.eta):
    # if(i%2)==0:
    # t += randint(0,2)
    # n.intelligenza = t
    # t = 0
    # for i in range(n.eta):
    # if(i%3)==0:
    # t += randint(0,2)
    # if t > 20:
    # t = 20
    # n.saggezza = t
    # t = 0
    # for i in range(3):
    # t += randint(1,7)
    # n.carisma = t
    # #psico
    # t = 0
    # for i in range(3):
    # t += randint(1,7)
    # n.umilta = t
    # t = 0
    # for i in range(3):
    # t += randint(1,7)
    # n.compassione = t
    # t = 0
    # for i in range(3):
    # t += randint(1,7)
    # n.carattere = t
    # #modifica velocita'
    return m


# ----------------------------------------------------------------------#

def create_barrel(pos):  # temp
    """ temp """
    obj = oggetto.Obj(0, pos[0], pos[1], pos[2])
    obj.nome = 'Barile'
    return obj


def make_perlin_mountains(num):  # processo (lento) di creazione mappe con PerlinNoise
    print "[WORLD MAKER]: generation of perlin_maps\t"
    for k in xrange(num):
        print "%3.2f %%" % (float(k * 100.0 / num)), "\r",
        P = PerlinNoise()
        matr = P.run(W_WORLD, H_WORLD, 0.25, [0.065, 0.125, 0.25, 0.5, 0.7, 1, 1.6, 1.8, 2],
                     D_WORLD + randint(-2, 2))
        t = ''
        for i in range(W_WORLD):
            for j in range(H_WORLD):
                t += str(matr[i + j * W_WORLD]).ljust(2, ' ') + ' '
            t += '\n'

        with open(r"lib_grows/perlin_maps/collina" + str(k) + ".txt", "w") as out:
            out.write(t)


def load_tile(element, side=1):  # side = 1: bottom, side = 0: top
    """
    :type side: object
    :param element:
    :param side:
    :return:
    """
    if element == T_VOID:
        return False
    else:
        if side == 1:
            # tile = Image.load(r"../graphics/tile"+element+".png")
            if element == T_ACQUA:
                tile = py_image.load(r"../graphics/tile" + element + ".png")
                return tile
            if element.startswith(T_SABBIA):
                tile = py_image.load(r"../graphics/tile0_base.png")
            else:
                tile = py_image.load(r"../graphics/tile" + element + ".png")
                tile = tile.subsurface(0, (BLOCCOY / 2), BLOCCOX, BLOCCOY / 2)  # left top width height
        # tile = tile.subsurface(0,side*(BLOCCOY/2),BLOCCOX,BLOCCOY/2)#left top width height
        else:
            tile = py_image.load(r"../graphics/tile" + element + ".png")
            if T_ACQUA == element:
                return False
            tile = tile.subsurface(0, 0, BLOCCOX, BLOCCOY / 2)  # left top width height
            if element.startswith(T_SABBIA):
                tile = py_image.load(r"../graphics/tile" + T_SABBIA + "_top_" + element.split('_')[-1] + ".png")
    return tile


class World_maker(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.tiles = []
        self.matrix = {}
        self.name = name
        self.pkl_name = ""
        self.dimx = 0
        self.dimy = 0
        self.dimz = 0
        self.maximun = 0

    def open_textual_matrix(self, filename):
        """
        :param filename: filename
        :return: boolean
        """
        if os.path.isfile(filename + '.pkl'):
            print "[WORLD MAKER]: load", filename, "\t"
            self.matrix = cPickle.load(open(filename + ".pkl", "rb"))
            load = True
            self.pkl_name = filename + '.pkl'
        else:
            """apre un file di testo casuale con interi separati da spazio, toglie il \n alla fine di ogni riga
            e trasforma tutti i valori in interi. restituisce un array"""
            filename = filename.strip('.txt')
            with open(filename + '.txt', "r") as openfile:
                matr = map(lambda v: v[:-1].split(), openfile.readlines())
                matr = reduce(lambda xx, yy: (xx + yy), matr)
                matr = map(lambda xx: int(xx), matr)
            self.pkl_name = filename + '.pkl'
            for index in range(max(matr) + OVERHEIGHT):  # qua viene creata l'altezza massima del chunk
                self.matrix[index] = [[] for _ in range(H_WORLD)]
                for y in range(H_WORLD):
                    t = []
                    for x in range(W_WORLD):
                        value = T_VOID
                        if matr[x + y * W_WORLD] >= index:
                            value = T_ERBA
                        t.append(value)
                    self.matrix[index][y] = t
            self.dimz = len(self.matrix)
            self.dimy = len(self.matrix[0])
            self.dimx = len(self.matrix[0][0])
            load = False
        self.maximun = len(self.matrix)
        return load

    def get_dims(self):
        self.dimz = len(self.matrix)
        self.dimy = len(self.matrix[0])
        self.dimx = len(self.matrix[0][0])

    def make_mountain(self, nome=""):
        """
        :rtype: object
        :param nome:
        :return: Nothing
        """
        """carica una collina casuale dalla memoria ROM e prepara la matrice"""
        if nome == "":
            # verifica l'esistenza di una montagna gia' creata in graphics/results
            nome = r"lib_grows/perlin_maps/collina" + str(randint(0, 19))
            for i in xrange(20):
                filename = r"../graphics/results/collina" + str(i)
                if os.path.isfile(filename + ".pkl"):
                    nome = filename
                    print "[WORLD MAKER]: found " + filename + ".pkl in memory... load\t"
                    break

        if not self.open_textual_matrix(nome):
            # modifica il chunk, gestisci i tile erba e la sabbia
            for z in xrange(Z_SEA + 1):
                for y in xrange(self.dimy):
                    for x in xrange(self.dimx):
                        if self.matrix[z][y][x] == T_VOID:
                            if z <= Z_SEA:
                                self.matrix[z][y][x] = T_ACQUA

            z = Z_SEA
            for y in xrange(self.dimy):
                for x in xrange(self.dimx):
                    if self.matrix[z][y][x] == T_ERBA:
                        if y < self.dimy - 1:
                            if self.matrix[z][y + 1][x] == T_ACQUA:
                                self.matrix[z][y][x] = T_SABBIA
                            if x > 0:
                                if self.matrix[z][y + 1][x - 1] == T_ACQUA:
                                    self.matrix[z][y][x] = T_SABBIA
                            if x < self.dimx - 1:
                                if self.matrix[z][y + 1][x + 1] == T_ACQUA:
                                    self.matrix[z][y][x] = T_SABBIA
                        if x < self.dimx - 1:
                            if self.matrix[z][y][x + 1] == T_ACQUA:
                                self.matrix[z][y][x] = T_SABBIA
                        if x > 0:
                            if self.matrix[z][y][x - 1] == T_ACQUA:
                                self.matrix[z][y][x] = T_SABBIA
                        if y > 0:
                            if self.matrix[z][y - 1][x] == T_ACQUA:
                                self.matrix[z][y][x] = T_SABBIA
                            if x < self.dimx - 1:
                                if self.matrix[z][y - 1][x + 1] == T_ACQUA:
                                    self.matrix[z][y][x] = T_SABBIA
                            if x > 0:
                                if self.matrix[z][y - 1][x - 1] == T_ACQUA:
                                    self.matrix[z][y][x] = T_SABBIA
            for z in xrange(self.dimz):
                for y in xrange(self.dimy):
                    for x in xrange(self.dimx):
                        if self.matrix[z][y][x] == T_ERBA:
                            if z < self.dimz - 1:
                                if y < self.dimy - 1 and x < self.dimx - 1:
                                    if self.matrix[z + 1][y][x] == T_ERBA:
                                        if self.matrix[z][y + 1][x] == T_ERBA and self.matrix[z][y][x + 1] == T_ERBA:
                                            self.matrix[z][y][x] = T_HIDE
                                            continue

                                if z < Z_SEA and self.matrix[z + 1][y][x] == T_VOID:
                                    self.matrix[z][y][x] = T_SABBIA
                                    continue
                                if self.matrix[z + 1][y][x] != T_VOID:
                                    self.matrix[z][y][x] = T_TERRA_HIDE
                            if z >= Z_SNOW:  # gestisci la neve
                                if self.matrix[z][y][x] == T_ERBA:
                                    self.matrix[z][y][x] = T_NEVE
                            border_type = 0
                            if self.matrix[z][y][x - 1] == T_VOID:
                                border_type |= 1
                            if self.matrix[z][y - 1][x] == T_VOID:
                                border_type |= 2
                            self.matrix[z][y][x] += '_' + str(border_type)

                if x == self.dimx - 1 or y == self.dimy:
                    if self.matrix[z][y][x].startswith(T_SABBIA):
                        self.matrix[z][y][x] = "f" + T_SABBIA

        else:
            self.get_dims()

    def conservatore(self, num):  # "picklellatore" per le matrici testuali
        print "scrittura pickle in corso"
        for i in range(num):
            print "%3.2f %%" % (float(i * 100.0 / num)), "\r",
            nome = r"lib_grows/perlin_maps/collina" + str(i) + ".txt"
            self.matrix = {}
            self.make_mountain(nome)
            cPickle.dump(self.matrix, open(nome.split('.')[0] + '.pkl', "wb"))

    def genera_immagini_chunk(self):
        filename = r"../graphics/results/" + self.pkl_name.split('/')[-1]
        if os.path.isfile(filename):
            print "[WORLD MAKER]: nothing to save..."
            return
        z_max = self.maximun
        dz_height = int(z_max * (BLOCCOY - 2 * DY))
        height = int(2 * DY * (self.dimy - 1) + BLOCCOY + dz_height)
        width = int(BLOCCOX * self.dimx)
        print "[WORLD MAKER]: generation of chunk images\t"
        background_final = pygame.Surface((width, height))
        background_final.set_colorkey(TRANSPARENCY)
        background_final.fill(TRANSPARENCY)
        for z in range(self.dimz):
            background = pygame.Surface((width, height))  # immagine con i tiles bassi
            foreground = pygame.Surface((width, height))  # immagine con i tiles alti
            background.fill(TRANSPARENCY)
            foreground.fill(TRANSPARENCY)
            background.set_colorkey(TRANSPARENCY)
            foreground.set_colorkey(TRANSPARENCY)
            for y in range(self.dimy):
                for x in range(self.dimx):
                    t_type = self.matrix[z][y][x]
                    tile = load_tile(t_type, 1)
                    tile_up = load_tile(t_type, 0)
                    if tile:
                        xo = width / 2 + (x - y - 1) * DX
                        yo = (x + y) * DY - z * DZ + dz_height
                        tileRect = tile.get_rect()
                        tileRect.topleft = (int(xo), int(yo))  # +BLOCCOY/2)
                        if not t_type.startswith(T_SABBIA) and not t_type.startswith(T_ACQUA):
                            tileRect.topleft = (int(xo), int(yo) + BLOCCOY / 2)
                        background.blit(tile, tileRect)
                    if tile_up:
                        xo = width / 2 + (x - y - 1) * DX
                        yo = (x + y) * DY - z * DZ + dz_height
                        tileRect = tile_up.get_rect()
                        tileRect.topleft = (int(xo), int(yo))

                        foreground.blit(tile_up, tileRect)

            background_final.blit(background, background.get_rect())
            background_final.blit(foreground, background.get_rect())
            data = py_image.tostring(background, "RGBA")
            surf = py_image.fromstring(data, (width, height), 'RGBA', False)
            py_image.save(surf, r"../graphics/results/hill_" + str(z) + "_d.png")
            data = py_image.tostring(foreground, "RGBA")
            surf = py_image.fromstring(data, (width, height), 'RGBA', False)
            py_image.save(surf, r"../graphics/results/hill_" + str(z) + "_u.png")
        py_image.save(background_final, r"../graphics/results/all_hill.png")
        cPickle.dump(self.matrix, open(r"../graphics/results/" + self.pkl_name.split('/')[-1], "wb"))

    def start(self):  # start Thread
        print self.name + ": start"
        self.make_mountain()
        self.genera_immagini_chunk()
        return self.matrix

    def __del__(self):
        print self.name + ": complete creation\t"

# W = World_maker("test")
# W.open_textual_matrix("./lib_grows/perlin_maps/collina6")
# W.get_dims()
# W.genera_immagini_chunk()
