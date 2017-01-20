####################################################
# Software License:                                 #
# --------------------------------------------------#
# main_grafica.py, a pygame library to handle the Graphics of the game. 
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
import sys
import threading
import traceback

import pygame
from pygame.locals import *

from game_constants import *

THREAD_LOCK = threading.Lock()


class Sprite:
    """classe usata per la gestione delle immagini per gli eventi"""

    def __init__(self):
        self.indice = -1
        self.image = None
        self.tile = None
        self.rect = None
        self.nome_sprite = ''
        self.verso = 0
        self.width = 36
        self.sx = 0
        self.sy = 0
        self.sz = 0
        self.zlimit = 0


def load_image(nome):  # carica un immagine
    """carica un'immagine con colore di trasparenza 123,123,123"""
    path = r"../graphics/" + nome + '.png'
    imm = pygame.image.load(path).convert()
    imm.set_colorkey(TRANSPARENCY)
    return imm


class GraphicHandler(threading.Thread):
    """classe per la gestione della grafica. Thread"""

    def __init__(self, name_in):
        threading.Thread.__init__(self)
        pygame.init()
        # ################ manage ###############################
        self.name = name_in
        self.running = True
        self.FPSCLOCK = pygame.time.Clock()
        self.counter = 0  # contatore per aggiornare le informazioni dei tile...
        self.zlimit = 0
        # ################# display ###############################
        self.DISPLAYSURF = pygame.display.set_mode((W, H), DOUBLEBUF | HWSURFACE, 32)
        pygame.display.set_caption('SmallBarrel-Miners')
        # self.basicFont = pygame.font.SysFont("Ubuntu",DIMCHAR)
        self.display = pygame.Surface((W, H))  # per settare lo sfondo
        self.displayRect = self.display.get_rect()
        self.selection = True  # False
        self.display_selection = False
        # ################# RAM ###########################
        self.offsetx = 0
        self.offsety = 0
        print "[GRAPHICS]: load RAM\t"
        self.matrice_tiles = None  # chunk tiles (matrice[z][y][x])

        self.background = load_image('background')
        self.backgroundRect = self.background.get_rect()
        self.backgroundRect.topleft = (0, 0)
        self.water = None  # self.load_image(r'results/sea')
        self.mappa = []  # array di immagini da caricare
        self.mappa_up = []  # altre immagini da caricare
        self.mappaRect = None  # self.mappa[0].get_rect()
        self.sprites = []  # vettore con gli sprite usati dagli eventi
        self.used_indexes = []
        self.sprite_sel = load_image('Sel')
        self.sprite_selRect = self.sprite_sel.get_rect()
        self.menu = load_image('menu')
        self.menuRect = self.menu.get_rect()

        # self.selected_tile = load_image('tile5') # EDIT da cambiare!!!!
        # self.selected_tileRect = self.selected_tile.get_rect()
        self.sprites_selected = []  # sprite per selezionare dei tiles

    def __repr__(self):
        t = self.name + "-> Active"
        return t

    def __raise__error(self):
        print "!!!!!!!!!!!!!!!# WARNING: " + self.name + " IS DOWN !!!!!!!!!!!!!!!"
        self.running = False
        print sys.exc_info()

    def carica_mappa(self):
        """carica le immagini del chunk dalla cartella results"""
        self.mappa = []
        self.mappa_up = []
        z = 0
        for z in xrange(len(self.matrice_tiles)):  # dimz
            sprite = load_image(r"results/hill_" + str(z) + "_d")
            self.mappa.append(sprite)
        for z in xrange(len(self.matrice_tiles)):  # dimz
            sprite = load_image(r"results/hill_" + str(z) + "_u")
            self.mappa_up.append(sprite)
        self.zlimit = z
        # self.water = self.load_image(r'results/sea')

    def push_selection_sprite(self, indice):
        """aggiunge uno sprite all'array sprites_selected"""
        single_sprite = Sprite()
        single_sprite.nome_sprite = "tile9"  # WARNING da cambiare!!!
        single_sprite.image = load_image(single_sprite.nome_sprite)
        single_sprite.image.set_alpha(100)
        single_sprite.image.set_colorkey((255, 255, 255))
        single_sprite.indice = int(indice)
        single_sprite.rect = single_sprite.image.get_rect()
        # self.used_indexes.append(int(indice))
        self.sprites_selected.append(single_sprite)

    def push_single_sprite(self, name, indice):
        """aggiunge uno sprite all'array sprites"""
        single_sprite = Sprite()
        single_sprite.nome_sprite = name
        single_sprite.image = load_image(single_sprite.nome_sprite)
        single_sprite.indice = int(indice)
        single_sprite.rect = single_sprite.image.get_rect()
        # self.used_indexes.append(int(indice))
        self.sprites.append(single_sprite)

    # def pop_single_sprite(self, indice):

    def update(self):
        """aggiorna la grafica"""
        # disegna lo sfondo
        self.mappaRect.midbottom = (self.offsetx + W / 2, self.offsety + H)
        self.display.blit(self.background, self.backgroundRect)
        # carica gli eventi mobili
        sprites = []
        for sprite in self.sprites:
            sprite.tile = sprite.image.subsurface(sprite.width * sprite.verso, 0, sprite.width, sprite.width)
            sprite.rect.bottomleft = coordinate_iso(sprite.sx, sprite.sy, sprite.sz)
            sprite.rect.x += self.offsetx
            sprite.rect.y += self.offsety
            sprites.append(sprite)
        for sprite in self.sprites_selected:
            sprite.rect.topleft = coordinate_iso(sprite.sx, sprite.sy, sprite.sz)
            sprite.rect.x += self.offsetx
            sprite.rect.y += self.offsety - DY

        sprites.sort(key=lambda s: s.rect.y)  # EDTI????
        sprites.sort(key=lambda s: s.sz)  # EDTI????

        for land in xrange(self.zlimit + 1):  # disegna i minatori e i tile
            self.display.blit(self.mappa[land], self.mappaRect)
            for sprite in sprites:
                if sprite.sz == land - 1:
                    self.display.blit(sprite.tile, sprite.rect)
            self.display.blit(self.mappa_up[land], self.mappaRect)
            for sprite in sprites:
                if sprite.sz == land - 1:
                    self.display.blit(sprite.tile.subsurface(0, 0, MINER_WIDTH, MINER_HEIGHT / 2), sprite.rect)
            for sprite in self.sprites_selected:  # disegna i tile selezionati
                if sprite.sz == land - 1:
                    self.display.blit(sprite.image, sprite.rect)

        if self.selection:
            if self.display_selection:
                self.display.blit(self.sprite_sel, self.sprite_selRect)

        self.display.blit(self.menu, self.menuRect)  # disegna il menu di GUI
        self.DISPLAYSURF.blit(self.display, self.displayRect)

    def run(self):
        print "Starting " + self.name + '\t'
        while self.running:
            try:
                self.FPSCLOCK.tick(FPS)
                THREAD_LOCK.acquire()
                self.update()
                pygame.display.update()
                THREAD_LOCK.release()
                self.counter = (self.counter + 1) % FPS
            except RuntimeError:
                print '-' * 80
                traceback.print_exc(file=sys.stdout)
                print '-' * 80
                self.__del__()
        pygame.quit()

    def __del__(self):
        print "Stopping " + self.name


def coordinate_iso(x, y, z):
    """trasforma le coordinate da cartesiane in isometriche"""
    xo = W / 2 + (x - y - 1) * DX
    yo = (x + y) * DY - z * DZ + Y_OFFSET
    return xo, yo
