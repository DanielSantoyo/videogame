#####################################################
# Software License:                                 #
# --------------------------------------------------#
# The Artistic License 2.0                          #
#                                                   #
#       Copyright (c) 2016, Daniel Santoyo Gomez.   #
#                                                   #
# contact: daniel.santoyo@gmx.com                   #
#####################################################

class Obj:
    def __init__(self, tipo, x, y, z):
        # type: (object, object, object, object) -> object
        """
        :rtype: object
        """
        self.sprite_ptr = None
        self.nome = ''
        self.x = x
        self.y = y
        self.z = z
        self.tipo = tipo
        self.quantita = 1
        self.a_terra = True
        self.bloccante = False
        self.peso = 0
