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
from random import choice as onbirth
from random import randint
from time import sleep as sleep

from lib_grafica.game_constants import *

import evento

IDLE = 0
THREAD_LOCK = threading.Lock()


class Miner(evento.Event):
    def __init__(self, nome='', indice=0):
        evento.Event.__init__(self, indice)
        self.nome = nome
        self.sesso = onbirth(['M', 'F'])
        self.eta = 0
        self.vista = 0
        # self.vitalita = 0
        # self.salute = 0
        # self.forza = 0
        # self.intelligenza = 0
        # self.saggezza = 0
        # self.carisma = 0
        # #bisogni
        # self.sonno = 0
        # self.fame = 0
        # ##self.sete = 0
        # self.noia = 0
        # self.solitudine = 0
        # self.vizio = 0
        # self.ferito = 0
        self.STATO = IDLE
        # #psicologia
        # self.umilta = 0
        # self.compassione = 0
        # self.carattere = 0
        # #societa'
        # self.ricchezza = 0
        # self.rispetto = 0
        # self.professione = ''
        self.cognome = ''
        # self.generazione = 1
        # self.abilita = []#livelli di professione
        # esterno -- OVERRIDE --???
        self.pos_oggetto_vicino = None
        self.indice = indice
        self.grafica = "miner"
        self.sprite_width = MINER_WIDTH
        # abilita'

    def __repr__(self):
        t = ''
        t += self.nome + ' ' + self.cognome + '\n'
        t += self.sesso + '\n'
        t += 'eta:' + str(self.eta) + '\n'
        # t += 'vit:'+str(self.vitalita)+'\n'
        # t += 'for:'+str(self.forza)+'\n'
        # t += 'int:'+str(self.intelligenza)+'\n'
        # t += 'sag:'+str(self.saggezza)+'\n'
        # t += 'car:'+str(self.carisma)+'\n'
        # t += 'p-umi:'+str(self.umilta)+'\n'
        # t += 'p-com:'+str(self.compassione)+'\n'
        # t += 'p-crt:'+str(self.carattere)+'\n'
        return t

    def guarda_attorno(self):  # visione sferica1
        THREAD_LOCK.acquire()
        # print self.vista
        for j in xrange(min(max(0, self.y - self.vista), H_WORLD - 1),
                        min(max(0, self.y + self.vista + 1), H_WORLD - 1)):
            for i in xrange(min(max(0, self.x - self.vista), W_WORLD - 1),
                            min(max(0, self.x + self.vista + 1), W_WORLD - 1)):
                if abs(i - self.x) + abs(j - self.y) < self.vista:
                    if self.chunk_ostacoli.matrice[self.z][j][i] == OBJECT:
                        self.pos_oggetto_vicino = (i, j, self.z)
                        self.ACTION = NEED_PATH_TO_GRAB_OBJ
                        self.path_sender.put(
                            ((self.x, self.y, self.z), self.pos_oggetto_vicino[:]))  # invia le info sulla
                        #  posizione e l'oggetto vicino
                        break
        THREAD_LOCK.release()

    def raccogli_oggetto(self, oggetto):
        self.oggetto.append(oggetto)

    def run(self):
        while self.running:
            # gestione movimento evento
            # movimento random...
            try:
                if self.STATO == IDLE:  # idle status development
                    if len(self.path) == 0:
                        verso = randint(0, 3)
                        self.try_move_random(self.x, self.y, self.z, verso)
                        if self.pos_oggetto_vicino is None:
                            self.guarda_attorno()

                    else:
                        self.move_path()
                        if self.blocked > 3:
                            sleep(self.velocita * randint(1, 4))

                        if len(self.path) == 1:
                            if self.ACTION == NEED_PATH_TO_GRAB_OBJ:
                                THREAD_LOCK.acquire()
                                self.sender.put(self.path.pop())
                                self.ACTION = GRAB_OBJ
                                print self.name, "GRAB_obj\t"
                                THREAD_LOCK.release()

                sleep(self.velocita)

            except RuntimeError:
                traceback.print_exc(file=sys.stdout)
                self.running = False
            self.sprite_ptr.sx = self.x
            self.sprite_ptr.sy = self.y
            self.sprite_ptr.sz = self.z
            for o in self.oggetto:
                o.sprite_ptr.sx = self.x
                o.sprite_ptr.sy = self.y
                o.sprite_ptr.sz = self.z
            self.sprite_ptr.verso = self.verso
