#!/usr/bin/python
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

import main_input
import master

header = '''\
#######################################
#                                     #
#     SMALLBARREL MINERS              #
#                                     #
#######################################'''


def main():
    print header
    print "Starting [MAIN]"
    hid = main_input.InputHandler('[INPUT]')
    Master = master.Master('[MASTER]')
    Master.start()  # Thread
    hid.zlimit = Master.graphics.zlimit
    hid.zlimitMax = hid.zlimit

    while hid.running:  # main game loop
        hid.run()
        Master.graphics.offsetx = hid.screen_x
        Master.graphics.offsety = hid.screen_y
        Master.graphics.zlimit = hid.zlimit
        if hid.pos:
            hid.pos = None
            Master.mouse_clicked = True
        Master.gui.key_pressed = hid.key_press
    print "END [MAIN]"
    Master.running = False
    sys.exit()


if __name__ == '__main__':
    main()
