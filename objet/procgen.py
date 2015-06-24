#!/usr/bin/python3
from random import *
from tkinter import *
import config

# utile ici que pour test unitaire
TESTING = False
DIFFICULTY = 0  # de 0 à 100

# À importé d'autres fichiers au futur..
X = config.BRIQUE_NB_X  # Nb de colonne de briques
Y = config.BRIQUE_NB_Y  # Nb de rangée de briques

''' NOTE TO SELF:
 PQ ça plante lorsque tkinter n'est pas inclus en global ??
'''


# Reçoit la seed, renverra soit un niveau sous forme de string, soit une liste de brique. à voir.
def procgen(graine, difficulty):
    def enlever(tab, prcnt):  # prcnt = pourcent à enlever
        if (TESTING):
            print("' Generation des trous...")
        for x in range(X):
            for y in range(Y):
                if (prcnt > randrange(0, 100)):
                    tab[x][y] = 0
        if (TESTING):
            print("' 'ok")
    ##############
    seed(graine)

    # Generation bruit blanc SANS ABSENCE DE BRIQUE
    noise = White_noise(config.BRIQUE_MIN_PV, config.BRIQUE_MAX_PV)

    # Generation de trous (%)
    enlever(noise, 30)

    # Parsage du bruit en dictionnaire
    briques = parse_noise_imp(noise)

    # distribution des types de brique (%)
    distrib_types(briques, difficulty, 20)

    # distribution des types de brique (%)
    distrib_bonus(briques, difficulty, 20)

    # à ce stade, brique sous forme de liste de dico.
    if (TESTING):
        return briques
    else:
        return parse_imp_to_obj(briques)


def White_noise(min, max):
    '''
    TODO : Faire en sorte que selon difficulté, les pv obtenues tendent vers
    MIN_PV ou MAX_PV
    Idée : génerer gaussienne associé à la position des hp
    '''
    # Initialisation liste
    tab = list()
    for x in range(X):
        tab.append(list())
        for y in range(Y):
            tab[x].append(0)

    if (TESTING):
        print("' Generation bruit blanc...")
    for x in range(X):
        for y in range(Y):
            tab[x][y] = randrange(min, max)
    if (TESTING):
        print("' 'ok")
    return tab


def parse_noise_imp(noise):
    if (TESTING):
        print("' Parsing to dictionnary...")
        pas_x = width//config.BRIQUE_NB_X
        pas_y = height//config.BRIQUE_NB_Y
    else:
        pas_x = config.BRIQUE_W
        pas_y = config.BRIQUE_H
    d_briques = list()

    for x in range(X):
        for y in range(Y):
            if (noise[x][y] != 0):
                r_x = (not(TESTING)) * config.BRIQUE_OFFSET_X + x*pas_x
                r_y = (not(TESTING)) * config.BRIQUE_OFFSET_Y + y*pas_y
                '''
                 'w': r_x+pas_x, 'h': r_y+pas_y,
                '''
                d_briques.append({'x': r_x, 'y': r_y, 'pv': noise[x][y],
                                  'w': pas_x, 'h': pas_y,
                                  'bonus': '', 'bonus_contenu': '',
                                  'surface': None})
    if (TESTING):
        print("' 'ok")
    return d_briques


def distrib_types(briques, difficulty, prcnt):
    if (TESTING):
        print("' Distribution des types de briques...")
    prcnt_bonus = prcnt/100 * (100-difficulty)
    prnct_malus = prcnt-prcnt_bonus
    nb_briques_b = int(prcnt_bonus/100 * len(briques))
    nb_briques_m = int(prnct_malus/100 * len(briques))
    briques_non_affectees = list(briques)

    while nb_briques_b > 0:
        n = randrange(0, len(briques_non_affectees))
        briques_non_affectees[n]['bonus'] = config.BRIQUE_TYPE_B[n % len(config.BRIQUE_TYPE_B)]
        briques_non_affectees.remove(briques_non_affectees[n])
        nb_briques_b -= 1

    while nb_briques_m > 0:
        n = randrange(0, len(briques_non_affectees))
        briques_non_affectees[n]['bonus'] = config.BRIQUE_TYPE_M[n % len(config.BRIQUE_TYPE_M)]
        briques_non_affectees.remove(briques_non_affectees[n])
        nb_briques_m -= 1

    if (TESTING):
        print("' 'ok")


def distrib_bonus(briques, difficulty, prcnt):
    if (TESTING):
        print("' Distribution des bonus/malus...")
    prcnt_bonus = prcnt/100 * (100-difficulty)
    prnct_malus = prcnt-prcnt_bonus
    nb_briques_b = int(prcnt_bonus/100 * len(briques))
    nb_briques_m = int(prnct_malus/100 * len(briques))
    briques_non_affectees = list(briques)

    while nb_briques_b > 0:
        n = randrange(0, len(briques_non_affectees))
        briques_non_affectees[n]['bonus_contenu'] = config.BONUS[n % len(config.BONUS)]
        briques_non_affectees.remove(briques_non_affectees[n])
        nb_briques_b -= 1

    while nb_briques_m > 0:
        n = randrange(0, len(briques_non_affectees))
        briques_non_affectees[n]['bonus_contenu'] = config.MALUS[n % len(config.MALUS)]
        briques_non_affectees.remove(briques_non_affectees[n])
        nb_briques_m -= 1

    if (TESTING):
        print("' 'ok")


def parse_imp_to_obj(d_briques):
    from element_jeu import Brique
    o_briques = list()

    for d_brique in d_briques:
        o_briques.append(Brique(d_brique['x'], d_brique['y'], d_brique['pv'],
                                d_brique['bonus_contenu'], d_brique['bonus']))

    # for o_brique in o_briques:
    #    o_brique.draw()

    return o_briques


if __name__ == '__main__':
    import sys
    global width, height
    TESTING = True
    width = 700
    height = 300

    if len(sys.argv) <= 1:  # si pas de seed renseigné
        graine = 1337
        print("auto: Seed =", graine)
    else:
        graine = sys.argv[1]  # peut être nombre, chaîne, ...
        print("Seed =", graine)

    def itoC(i):  # int to Color
        if (i > config.BRIQUE_MAX_PV):
            print("PROBLEME: VALEUR TABLEAU (", i, ") > MAX PREVU")
            exit()

        def toHex(a):
            return "%X" % a
        '''
        #Fire gradient
        r = 255//(MAX_PV-1)*3
        R = min(r*i, 255)
        G = max(0, 1*min(r*i-255, 255))
        B = max(0, 1*min(r*i-255*2, 255))
        '''

        # Black n white
        r = 150//(config.BRIQUE_MAX_PV-1)
        R = i * r
        G = R
        B = G

        R = toHex(R)
        G = toHex(G)
        B = toHex(B)
        while len(R) < 2:
            R = "0" + R
        while len(G) < 2:
            G = "0" + G
        while len(B) < 2:
            B = "0" + B
        return ("#" + R + G + B)

    def update():  # Gestion FPS
        after(1000 / 50, update)

    root = Tk()
    root.title("Noise test")
    canvas = Canvas(root, width=width, height=height, bg="black")
    canvas.pack()
    # canvas.bind('<B1-Motion>', deplacement)
    canvas.focus_set()

    print("Generation map...")
    briques = procgen(graine, DIFFICULTY)
    print("'ok\n")
    print("Rendu..")

    for brique in briques:
        brique['surface'] = \
            canvas.create_rectangle(brique['x'], brique['y'],
                                    brique['x']+brique['w'],
                                    brique['y']+brique['h'],
                                    width=0,
                                    outline='',
                                    fill=itoC(brique['pv']),
                                    tag='')
        if (brique['bonus'] == 'explosive'):
            canvas.itemconfig(brique['surface'],
                              fill='red3', tags=('brique'))
        if (brique['bonus'] == 'indestructible'):
            canvas.itemconfig(brique['surface'], width=2, outline='grey90',
                              fill='grey80', tags=('brique'))
        if brique['bonus_contenu'] != '':
            if brique['bonus_contenu'] in config.BONUS:
                canvas.create_rectangle(brique['x']+brique['w']/3,
                                        brique['y']+brique['h']/3,
                                        brique['x']+brique['w']/2,
                                        brique['y']+brique['w']/4,
                                        width=0,
                                        outline='',
                                        fill='green',
                                        tag='')
            if brique['bonus_contenu'] in config.MALUS:
                canvas.create_rectangle(brique['x']+brique['w']/3,
                                        brique['y']+brique['h']/3,
                                        brique['x']+brique['w']/2,
                                        brique['y']+brique['w']/4,
                                        width=0,
                                        outline='',
                                        fill='red',
                                        tag='')
    print("'OK")
    mainloop()
