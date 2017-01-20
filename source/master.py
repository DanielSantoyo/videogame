#####################################################
# Software License:                                 #
# --------------------------------------------------#
# The Artistic License 2.0                          #
#                                                   #
#       Copyright (c) 2016, Daniel Santoyo Gomez.   #
#                                                   #
# contact: daniel.santoyo@gmx.com                   #
#####################################################
import sys
import threading
import traceback
from time import sleep

from pygame import mouse

from lib_eventi import minatore
from lib_grafica import main_grafica
from lib_grafica.game_constants import *
from lib_grafica.main_grafica import coordinate_iso
from lib_grows import chunk
from lib_grows import genesi
from lib_grows.genesi import World_maker
from lib_pathfinders.PathFinder import *

THREAD_LOCK = threading.Lock()
DEBUG = 0
INITIALIZE = 1
K_LSHIFT = 304


class Gui_manager():
    """classe per la gestione dei comandi di GUI"""
    X_Index = 523
    Y_Index = 243
    blank_size = 3
    Button_size = 26
    Icon_width = Button_size + blank_size
    Icon_height = Button_size + blank_size
    Icons_col = 4  # numero di icone per colonne
    Icons_row = 8  # numero di icone per righe
    menu_width = 120
    key_pressed = 0
    map_pointer = None

    def __init__(self):
        self.actual_selection = -1  # None
        self.tile_selection = []
        self.tile_selected_index = []

    def clickon(self, x, y, xmap, ymap, zmap):

        # print self.key_pressed

        index = -1
        if x > self.X_Index and x < self.X_Index + self.menu_width:
            if y > self.Y_Index and y < self.Y_Index + self.Icon_height * self.Icons_row:
                if (x - self.X_Index) % self.Icon_width < self.Button_size and \
                                        (y - self.Y_Index) % self.Icon_height < self.Button_size:
                    index = (x - self.X_Index) / self.Icon_width + ((
                                                                        y - self.Y_Index) / self.Icon_height) * self.Icons_col
        if index != -1:
            self.actual_selection = index

        if index == 3:
            print "salva"

        if index == -1:
            if xmap != -1 and ymap != -1 and zmap != -1:
                if (xmap, ymap, zmap) not in self.tile_selection:
                    self.tile_selection.append((xmap, ymap, zmap))
                    if self.key_pressed == K_LSHIFT:
                        # paralellepipedo tra xmap, ymap, zmap e l'ultimo valore di tile selezionato.
                        # ogni tile valido (!= VOID) dentro il paralellepipedo viene aggiunto alla selezione.
                        values = self.tile_selection[-2]
                        print (xmap, ymap, zmap), self.tile_selection[-2]
                        self.key_pressed = 0
                        for k in xrange(abs(zmap - values[2])):
                            for j in xrange(abs(ymap - values[1])):
                                for i in xrange(abs(xmap - values[0])):
                                    xx = min(xmap, values[0]) + i
                                    yy = min(ymap, values[1]) + j
                                    zz = min(zmap, values[2]) + k
                                    if self.map_pointer[zz][yy][xx] != T_VOID:
                                        if (xx, yy, zz) not in self.tile_selection:
                                            self.tile_selection.append((xx, yy, zz))


class Master(threading.Thread):
    """classe per la gestione della comunicazione tra le librerie. Thread"""

    def __init__(self, name, mode=1):
        threading.Thread.__init__(self)
        self.name = name
        self.running = True
        self.timer = 0.02
        self.mode = mode
        self.mouse_clicked = False
        self.mouse_pos = [-1, -1, -1]
        # -----------------------------------------------------------------------------#
        # GUI
        self.gui = Gui_manager()

        # world creation
        self.miners = []
        self.objects = []
        self.objects_map = {}  # usata per ritrovare un oggetto nel self.objects in base alle sue coordinate...

        world = World_maker('[WORLDMAKER]')
        genesi.make_perlin_mountains(20)
        world.conservatore(20)
        self.matrice_tiles = world.start()
        self.gui.map_pointer = self.matrice_tiles  # puntatore a matrice_tiles
        print self.name + ": MATRICE_TILES added to [GUI]"
        THREAD_LOCK.acquire()
        self.graphics = main_grafica.GraphicHandler('[GRAPHICS]')
        self.graphics.matrice_tiles = self.matrice_tiles  # bind tra puntatori
        print self.name + ": MATRICE_TILES added to [GRAPHICS]"
        self.graphics.carica_mappa()
        self.graphics.mappaRect = self.graphics.mappa[0].get_rect()

        sleep(1)
        print self.name + ": obstacles loaded"
        self.ck_ostacoli = chunk.Chunk(0)  # ostacoli
        self.ck_ostacoli.carica_matrice(self.graphics.matrice_tiles)
        # -----------------------------------------------------------------------------#
        # pathfinder
        self.PF = Pathfinder()
        self.PF.create_wf_matrix(self.ck_ostacoli.matrice)

        # CENTRO CITTA'
        x = randint(0, W_WORLD - 1)
        y = randint(0, H_WORLD - 1)
        z = 0
        while True:
            if self.ck_ostacoli.matrice[z][y][x] == FREE and z > Z_SEA:
                break
            z += 1
            if z == D_WORLD:
                x = randint(0, W_WORLD - 1)
                y = randint(0, H_WORLD - 1)
                z = 0
        print self.name + ": Center of city:", x, y, z
        self.center_x = x
        self.center_y = y
        self.center_z = z
        # genera i minatori
        for i in range(NUM_MINERS):
            n = minatore.Miner('', i)
            n = genesi.miner_random(n)
            self.miners.append(n)
            self.graphics.push_single_sprite(n.grafica, n.indice)
            n.x = x
            n.y = y
            n.z = z
        print self.name + ": created %d miners" % NUM_MINERS
        # start miners threads
        for d in self.miners:
            d.chunk_ostacoli = self.ck_ostacoli  # puntatore al chunk ostacoli
            d.sprite_ptr = self.graphics.sprites[d.indice]  # puntatore agli sprites della graphics
            d.start()
        self.graphics.start()  # start graphics Thread
        THREAD_LOCK.release()

    def unic_id(self, x, y, z):
        """trasforma le coordinate x y e z in un valore univoco"""
        return x + y * W_WORLD + z * W_WORLD * H_WORLD

    def iso_to_xyz(self, x_pos, y_pos):
        """trasforma le coordinate da isometriche in matriciali"""
        # fai una cornice per il mouse...
        # self.graphics.display_selection = False
        if x_pos > W - self.gui.menu_width:
            self.graphics.display_selection = False
            return
        if x_pos > MOUSE_TH or x_pos < W - (
                    MOUSE_TH + self.gui.menu_width) and y_pos > MOUSE_TH or y_pos < H - MOUSE_TH:
            # controlla dalla z massima scendendo fino a -1
            done = False
            z = min(D_WORLD, self.graphics.zlimit + 2)
            xt = 0
            yt = 0
            while not done:
                z -= 1
                if z == -1:
                    break
                x = x_pos - self.graphics.offsetx - W / 2
                y = y_pos - self.graphics.offsety - Y_OFFSET + z * DZ
                xt = y + x / SQRT3
                yt = y - x / SQRT3
                # xt = min(max(0, int(round(xt / DIAGONAL))), W_WORLD - 1)
                xt = int(round(xt / DIAGONAL))
                # yt = min(max(0, int(round(yt / DIAGONAL))), H_WORLD - 1)
                yt = int(round(yt / DIAGONAL))
                if z not in self.matrice_tiles.keys():
                    continue
                if xt < 0 or xt > W_WORLD - 1:
                    continue
                if yt < 0 or yt > H_WORLD - 1:
                    continue
                if self.matrice_tiles[z][yt][xt] != T_VOID and z < self.graphics.zlimit:
                    done = True
            if done:
                if self.mouse_clicked:
                    self.mouse_pos = (xt, yt, z)
                self.graphics.sprite_selRect.midleft = coordinate_iso(xt, yt, z)
                self.graphics.sprite_selRect.x += self.graphics.offsetx
                self.graphics.sprite_selRect.y += self.graphics.offsety
                self.graphics.display_selection = True
            else:
                self.graphics.display_selection = False
                self.mouse_pos = (-1, -1, -1)

    def __repr__(self):
        t = self.name + "-> Active"
        return t

    def __raise__error(self):
        print "!!!!!!!!!!!!!!!# WARNING: " + self.name + " IS DOWN !!!!!!!!!!!!!!!"
        self.running = False
        print sys.exc_info()

    def remove_obj_from_map(self, index):
        self.objects_map.pop(index, None)

    def run(self):
        print "Starting " + self.name
        while self.running:
            try:
                sleep(self.timer)
                (xm, ym) = mouse.get_pos()

                if self.graphics.selection:
                    self.iso_to_xyz(xm, ym)
                if self.mouse_clicked:  # SX
                    self.mouse_clicked = False

                    # ------------TEST--------------------------------
                    if len(self.mouse_pos) == 0:
                        continue
                    x = self.mouse_pos[0]
                    y = self.mouse_pos[1]
                    z = self.mouse_pos[2]

                    # if self.matrice_tiles[z][y][x] == FREE:  # se lo spazio e' disponibile
                    # self.objects.append(genesi.create_barrel(self.mouse_pos))  # crea oggetto ##temporaneo
                    # self.objects_map[self.unic_id(x, y, z)] = self.objects[-1]  # puntatore a oggetto
                    # self.graphics.push_single_sprite(self.objects[-1].nome,len(self.graphics.sprites))  # aggiunge una sprite
                    # self.objects[-1].sprite_ptr = self.graphics.sprites[-1]  # aggiorna il puntatore dell'oggetto
                    # self.objects[-1].sprite_ptr.sx = self.objects[-1].x  # aggiorna le coordinate sullo schermo
                    # self.objects[-1].sprite_ptr.sy = self.objects[-1].y
                    # self.objects[-1].sprite_ptr.sz = self.objects[-1].z
                    # self.ck_ostacoli.matrice[z][y][x] = OBJECT  # aggiorna gli ostacoli

                    # ------------TEST--------------------------------

                    # -------------GUI------------------------
                    self.gui.clickon(xm, ym, x, y, z)

                    # # -------------GUI------------------------

                THREAD_LOCK.acquire()
                for m in self.miners:
                    #
                    if m.ACTION == NEED_PATH_TO_GRAB_OBJ:
                        if m.path_sender.full():
                            path = m.path_sender.get()
                            m.path = self.PF.get_path(path)  # invia la Pathfinder la richiesta dell'evento
                            print m.path
                    elif m.ACTION == GRAB_OBJ:
                        if m.sender.full():
                            pos = m.sender.get()
                            index = self.unic_id(pos[0], pos[1], pos[2])
                            if index in self.objects_map.keys():
                                print "master: raccogli oggetto", m.name
                                m.raccogli_oggetto(self.objects_map[index])
                                m.ACTION = NEED_PATH_TO_DEPOSE_OBJ
                                self.remove_obj_from_map(index)
                                self.ck_ostacoli.matrice[pos[2]][pos[1]][pos[0]] = FREE  # svuota l'ostacolo dalla mappa
                            else:
                                print "no object to grab", m.name
                                m.ACTION = NEED_PATH
                                m.path = []
                                m.pos_oggetto_vicino = None

                                # elif m.ACTION == NEED_PATH_TO_DEPOSE_OBJ:
                #### gui ####

                k = 0
                while len(self.gui.tile_selection) > len(self.gui.tile_selected_index):
                    # self.gui.tile_selected_index = []
                    # if k not in self.graphics.used_indexes:
                    # self.graphics.push_single_sprite("Barile", k)
                    self.graphics.push_selection_sprite(k)
                    self.gui.tile_selected_index.append(k)
                    self.graphics.sprites_selected[-1].sx = \
                    self.gui.tile_selection[len(self.gui.tile_selected_index) - 1][0]
                    self.graphics.sprites_selected[-1].sy = \
                    self.gui.tile_selection[len(self.gui.tile_selected_index) - 1][1]
                    self.graphics.sprites_selected[-1].sz = \
                    self.gui.tile_selection[len(self.gui.tile_selected_index) - 1][2]

                    # k += 1
                ################

                THREAD_LOCK.release()

            except RuntimeError:
                print '-' * 80
                traceback.print_exc(file=sys.stdout)
                print '-' * 80
                self.running = False
                self.__del__()

    def __del__(self):
        self.graphics.running = False
        print self.name + ": stopping miners Threads"
        for m in self.miners:
            m.running = False
        print "Stopping " + self.name
