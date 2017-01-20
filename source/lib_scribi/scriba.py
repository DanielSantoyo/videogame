#####################################################
# Software License:                                 #
# --------------------------------------------------#
# The Artistic License 2.0                          #
#                                                   #
#       Copyright (c) 2016, Daniel Santoyo Gomez.   #
#                                                   #
# contact: daniel.santoyo@gmx.com                   #
#####################################################
from random import choice
from random import randint

vocali = "a,i,u".split(",")
consonanti = "b,d,p,f,ch,k,ph,chh,kh,gh,s,sh,m,n,gn,l,ll,r,w,y".split(",")
fine_sil = "s,l,ll,r,n,m,w,y,p,k".split(",")


def nome_random(s):
    if s == 'M':
        mono = '''ghum,lum,fil,bil,bum,rik,ruk'''.split(',')
        voc = '''a,i,ur'''.split(',')
    else:
        mono = '''gam,kim,fal,wil,lum,rig,gha,na,yin,phi'''.split(',')
        voc = '''a,i,as'''.split(',')
    if randint(0, 1):
        t = choice(mono) + choice(voc) + choice(mono) * randint(0, 1)
    else:
        t = choice(voc) * randint(0, 1) + choice(mono) + choice(voc)
    t = (t[:1]).upper() + t[1:]
    return t


def cognome_random():
    mono = '''tuk,duk,kuun,muun,lum,ghan,miil'''.split(',')
    voc = '''a,i,u'''.split(',')
    if randint(0, 1):
        t = choice(mono) + choice(voc) + choice(mono) * randint(0, 1)
    else:
        t = choice(voc) * randint(0, 1) + choice(mono) + choice(voc)
    t = (t[:1]).upper() + t[1:]
    return t


def parola_permessa():
    '''(La struttura sillabica Le possibili forme sillabiche sono rappresentate
dalla seguente formula:(C)V(C)-CV(C). Le parole monosillabiche contengono
almeno una consonante (CV o VC o CVC), e nei polisillabi, la terza
sillaba e le seguenti hanno la seguente formula: CV(C). Le consonanti che
possono apparire alla fine di una sillaba sono: s, l/ll, r, n/m, w, y, p, k. A
fine parola possono essere presenti tutte tranne la p. Non sono possibili
gruppi YI, WU e prima di una consonante UW. I suffissi si aggiustano a
questo schema sillabico.'''

    dim = randint(1, 3)
    parola = ""
    if dim == 1:  # parola monosillabica
        types = randint(0, 2)
        if types == 0:
            parola = choice(consonanti) + choice(vocali)
        elif types == 1:
            parola = choice(vocali) + choice(consonanti)
        elif types == 2:
            parola = choice(consonanti) + choice(vocali) + choice(consonanti)
    else:
        for i in xrange(dim):
            if i == 0:  # (C)V(C)
                parola += randint(0, 1) * choice(consonanti) + choice(vocali) + randint(0, 1) * choice(fine_sil)
            else:
                parola += choice(consonanti) + choice(vocali) + randint(0, 1) * choice(fine_sil)

    # check parola... YI WU UW...
    if "YI" in parola or "WU" in parola or "UW" in parola:
        return parola_permessa()
    return parola
