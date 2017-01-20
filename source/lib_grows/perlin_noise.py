#####################################################
# Software License:                                 #
# --------------------------------------------------#
# The Artistic License 2.0                          #
#                                                   #
#       Copyright (c) 2016, Daniel Santoyo Gomez.   #
#                                                   #
# contact: daniel.santoyo@gmx.com                   #
#####################################################
import random
from math import cos


class PerlinNoise:
    """perlin noise per generare montagne. restituisce una Matrice su un unico vettore
    l'idea generale e' generare una matrice di valori causali tra -1 e 1 e poi fare
    l'interpolazione tra i valori della matrice in base alla frequenza e fare un filtro
    (smooth) di valori in un intorno di 8 caselle"""

    @staticmethod
    def Linear_interpolate(a, b, x):
        return a * (1 - x) + b * x

    def __init__(self):
        self.width = 0
        self.height = 0
        self.matrix = []
        self.complete = False

    @staticmethod
    def Cosine_Interpolate(a, b, x):
        # x > 0
        ft = x * 3.1415927  # math.pi
        f = (1 - cos(ft)) * 0.5
        return a * (1 - f) + b * f

    def Noise(self, x, y):
        x %= self.width
        y %= self.height
        return self.matrix[x + y * self.width]

    def SmoothNoise_2D(self, x, y):
        """16| 8|16
            8| 4| 8
           16| 8|16"""
        corners = (self.Noise(x - 1, y - 1) + self.Noise(x + 1, y - 1) + self.Noise(x - 1, y + 1) +
                   self.Noise(x + 1, y + 1)) / 16
        sides = (self.Noise(x - 1, y) + self.Noise(x + 1, y) + self.Noise(x, y - 1) + self.Noise(x, y + 1)) / 8
        center = self.Noise(x, y) / 4
        return corners + sides + center

    def InterpolatedNoise(self, x, y):
        """
        :type x: number
        :type y: number
        """
        integer_X = int(x)
        fractional_X = x - integer_X
        integer_Y = int(y)
        fractional_Y = y - integer_Y
        v1 = self.SmoothNoise_2D(integer_X, integer_Y)
        v2 = self.SmoothNoise_2D(integer_X + 1, integer_Y)
        v3 = self.SmoothNoise_2D(integer_X, integer_Y + 1)
        v4 = self.SmoothNoise_2D(integer_X + 1, integer_Y + 1)

        i1 = self.Cosine_Interpolate(v1, v2, fractional_X)
        i2 = self.Cosine_Interpolate(v3, v4, fractional_X)
        return self.Cosine_Interpolate(i1, i2, fractional_Y)

        # i1 = self.Linear_interpolate(v1 , v2 , fractional_X)
        # i2 = self.Linear_interpolate(v3 , v4 , fractional_X)
        # return self.Linear_interpolate(i1 , i2 , fractional_Y)

    def salva_immagine(self, total, x, y, nome):
        """debug"""
        from PIL import Image
        im = Image.new("RGB", (x * 8, y * 8), "white")
        for j in xrange(y * 8):
            for i in xrange(x * 8):
                p = total[i / 8 + (j / 8) * self.width]
                r = 100
                b = 100
                if p < 30:
                    b = 250
                    r = 50
                if p > 200:
                    r = 250
                    b = 250
                im.putpixel((i, j), (r, p / 2 + 100, b))
        im.save(nome)
        print "Immagine salvata come: " + nome

    def run(self, x, y, persistence, freqs, maxvalue):

        """colline :       freqs = [0.125,0.25,0.5,0.7,1,1.5,2]
        :param x:
        :param y:
        :param freqs:
        :return:
        :type persistence: number
        :type maxvalue: number
        """
        """terreno ruvido: freqs = [1,2,3,4,5,6,7,8]"""
        self.width = x
        self.height = y
        total = []
        for j in xrange(y):
            for i in xrange(x):
                self.matrix.append(random.randint(-1000, 1000) / 1000.0)
                total.append(0)

        Number_Of_Octaves = len(freqs)
        p = persistence
        n = Number_Of_Octaves - 1
        for k in xrange(n):
            frequency = freqs[k]
            amplitude = p ** k
            for j in xrange(y):
                for i in xrange(x):
                    total[i + j * self.width] += self.InterpolatedNoise(float(i * frequency),
                                                                        float(j * frequency)) * float(amplitude)

        minimo = min(total)
        for i in xrange(len(total)):
            total[i] += abs(minimo)
        massimo = max(total)

        rho = massimo / maxvalue
        riscalo = 1.0
        for i in xrange(len(total)):
            total[i] = int((total[i] / rho) * riscalo)  # maxValue e' il valore massimo che si vuole avere nella matrice

        self.complete = True
        return total
