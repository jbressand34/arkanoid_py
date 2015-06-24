#!/usr/bin/python3
from random import *
from tkinter import *
import config


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
        for x in range(X):
            for y in range(Y):
                if (prcnt > randrange(0, 100)):
                    tab[x][y] = 0

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

    # distribution des bonus de brique (%)
    distrib_bonus(briques, difficulty, 20)

    #retour du dictionnaire de briques :
    return briques

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

    for x in range(X):
        for y in range(Y):
            tab[x][y] = randrange(min, max)
    return tab


def parse_noise_imp(noise):
    pas_x = config.BRIQUE_W
    pas_y = config.BRIQUE_H
    d_briques = list()

    for x in range(X):
        for y in range(Y):
            if (noise[x][y] != 0):
                r_x = config.BRIQUE_OFFSET_X + x*pas_x
                r_y = config.BRIQUE_OFFSET_Y + y*pas_y
                '''
                 'w': r_x+pas_x, 'h': r_y+pas_y,
                '''
                d_briques.append({'x': r_x, 'y': r_y, 'pv': noise[x][y],
                                  'w': pas_x, 'h': pas_y,
                                  'bonus': '', 'bonus_contenu':'',
                                  'surface': None})
    return d_briques


def distrib_types(briques, difficulty, prcnt):
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


def distrib_bonus(briques, difficulty, prcnt):
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


