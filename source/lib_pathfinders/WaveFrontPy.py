#####################################################
# Software License:                                 #
# --------------------------------------------------#
# The Artistic License 2.0                          #
#                                                   #
#       Copyright (c) 2016, Daniel Santoyo Gomez.   #
#                                                   #
# contact: daniel.santoyo@gmx.com                   #
#####################################################

def trova(x, y, z, matrice, cosa):
    # funzione trova(x,y,z,cosa) return True se si trova False se errore oppure non trova...
    if x < 0 or x >= width:
        return False
    if y < 0 or y >= height:
        return False
    if z < 0 or z >= depth:
        return False
    if matrice[z][y][x] == cosa:
        return True
    return False


def scopri(x, y, z, matrice, indice):
    values = [-1, 1]
    for v in values:
        if trova(x + v, y, z, matrice, indice):
            path = (x + v, y, z)
            return path
        if trova(x + v, y, z, matrice, '^'):
            if trova(x + v, y, z + 1, matrice, indice):
                path = (x + v, y, z + 1)
                return path
        if trova(x + v, y, z, matrice, 'v'):
            if trova(x + v, y, z - 1, matrice, indice):
                path = (x + v, y, z - 1)
                return path
    for v in values:
        if trova(x, y + v, z, matrice, indice):
            path = (x, y + v, z)
            return path

        if trova(x, y + v, z, matrice, '^'):
            if trova(x, y + v, z + 1, matrice, indice):
                path = (x, y + v, z + 1)
                return path
        if trova(x, y + v, z, matrice, 'v'):
            if trova(x, y + v, z - 1, matrice, indice):
                path = (x, y + v, z - 1)
                return path


def scrivi(x, y, z, matrice, indice):
    flag = False
    values = [-1, 1]
    for v in values:
        if trova(x + v, y, z, matrice, '0'):
            matrice[z][y][x + v] = str(indice + 1)
        flag = trova(x + v, y, z, matrice, 'G') or flag
        if trova(x + v, y, z, matrice, 'v'):
            if trova(x + v, y, z - 1, matrice, '0'):
                matrice[z - 1][y][x + v] = str(indice + 1)
            flag = trova(x + v, y, z - 1, matrice, 'G') or flag
        if trova(x + v, y, z, matrice, '^'):
            if trova(x + v, y, z + 1, matrice, '0'):
                matrice[z + 1][y][x + v] = str(indice + 1)
            flag = trova(x + v, y, z + 1, matrice, 'G') or flag
    for v in values:
        if trova(x, y + v, z, matrice, '0'):
            matrice[z][y + v][x] = str(indice + 1)
        flag = trova(x, y + v, z, matrice, 'G') or flag
        if trova(x, y + v, z, matrice, 'v'):
            if trova(x, y + v, z - 1, matrice, '0'):
                matrice[z - 1][y + v][x] = str(indice + 1)
            flag = trova(x, y + v, z - 1, matrice, 'G') or flag
        if trova(x, y + v, z, matrice, '^'):
            if trova(x, y + v, z + 1, matrice, '0'):
                matrice[z + 1][y + v][x] = str(indice + 1)
            flag = trova(x + v, y, z + 1, matrice, 'G') or flag
    return matrice, flag  # , mod


height = 0
width = 0
depth = 0


def main(singletest):
    print "wavefront"
    global height
    global width
    global depth
    linea = singletest.pop(0).split(' ')
    width = int(linea[0])
    height = int(linea[1])
    depth = int(linea[2])
    xstart = int(linea[3])
    ystart = int(linea[4])
    zstart = int(linea[5])
    xgoal = int(linea[6])
    ygoal = int(linea[7])
    zgoal = int(linea[8])

    # piani = []
    # for z in range(depth):
    # piani.append(mappa(z))
    # for y in range(width):
    # piani[-1].matrice.append([])
    matrice = [[] for _ in range(depth)]
    print matrice
    j = 0
    k = 0
    for l in test:
        if k < depth:
            matrice[k].append([])
            matrice[k][j] = [l[0], l[1], l[2]]
            j += 1
            if j % height == 0:
                j = 0
                k += 1

    indice = -1

    fine = False
    for k in range(depth):
        for j in range(height):
            for i in range(width):
                if matrice[k][j][i] == 'S':
                    matrice, fine = scrivi(i, j, k, matrice, 0)
                    indice = 1
    print "====================================="
    for m in matrice:
        for p in m:
            print p
    while not fine:  # x != xgoal and y != ygoal and z != zgoal):
        # scansiona tutte le mappe
        for k in range(depth):
            for j in range(height):
                for i in range(width):
                    if matrice[k][j][i] == str(indice):
                        matrice, fine = scrivi(i, j, k, matrice, indice)
        indice += 1

    # trova percorso a retroso...
    path = [(xgoal, ygoal, zgoal)]
    x = xgoal
    y = ygoal
    z = zgoal
    while indice > 1:
        a = scopri(x, y, z, matrice, str(indice - 1))
        x = a[0]
        y = a[1]
        z = a[2]
        indice -= 1
        path.append(a)
    path.append((xstart, ystart, zstart))
    print path


test = '''3 3 3 1 1 2 1 1 0
XXX
^GX
00X
000
0^0
v@X
@v@
vSv
@@X
'''.split('\n')

if __name__ == '__main__':
    main(test)
