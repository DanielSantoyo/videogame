####################################################
# Software License:                                 #
# --------------------------------------------------#
# main_input.py, a pygame library to handle the user inputs: keyboard and mouse.
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
import traceback

import pygame
from pygame.locals import *


class InputHandler:
    """classe per la gestione degli input da tastiera."""

    def __init__(self, name):
        self.name = name
        self.running = True
        self.screen_x = 0
        self.screen_y = 0
        self.zlimit = 0
        self.zlimitMax = 0
        self.key_press = 0
        self.pos = None
        self.left_click = False
        print "Starting " + self.name

    def run(self):
        try:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_DOWN:
                        self.screen_y -= 50
                    if event.key == K_UP:
                        self.screen_y += 50
                    if event.key == K_RIGHT:
                        self.screen_x -= 50
                    if event.key == K_LEFT:
                        self.screen_x += 50
                    if event.key == K_PAGEUP:
                        self.zlimit = min(self.zlimit + 1, self.zlimitMax)
                    if event.key == K_PAGEDOWN:
                        self.zlimit = max(self.zlimit - 1, 0)
                    self.key_press = event.key
                if event.type == MOUSEBUTTONDOWN:
                    # if pygame.mouse.get_pressed()[2]:
                    # pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0]:
                        self.left_click = True
                        # pos = pygame.mouse.get_pos()
                if event.type == MOUSEBUTTONUP:
                    if self.left_click:
                        self.pos = pygame.mouse.get_pos()
                        self.left_click = False

        except RuntimeError:
            print '-' * 80
            traceback.print_exc(file=sys.stdout)
            print '-' * 80
            self.running = False
            self.__del__()

    def __del__(self):
        print "Stopping " + self.name
