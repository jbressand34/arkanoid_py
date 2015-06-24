#!/usr/bin/python3
from random import *
from tkinter import *
import config

# utile ici que pour test unitaire
TESTING = False

X = config.BRIQUE_NB_X  # Nb de colonne de briques
Y = config.BRIQUE_NB_Y  # Nb de rangee de briques

# Recoit la graine et la difficulte, renvoit liste de brique
def procgen(graine, difficulty):
    def enlever(tab, prcnt):  # prcnt = pourcent a enlever
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

    # distribution des bonus de brique (%)
    distrib_bonus(briques, difficulty, 20)

    # a ce stade, brique sous forme de liste de dico.
    if (TESTING):
        return briques
    else:
        return parse_imp_to_obj(briques)
