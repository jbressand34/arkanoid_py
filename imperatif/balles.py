#!/usr/bin/python3
#-*- coding:utf-8 -*-

import config
from tkinter import *

RAYON_BALLE = 20

x = []
y = []
w = []
h = []
dx = []
dy = []
surfaces = []
bonus = []
bonus_frameleft = []

# Fonctions implémentées :

#nbBalle()
#move()
#ajouterBalle(x1, y1, dx1=0, dy1=2, bonus1="", bonus_frameleft1=0)
#enleverBalle(i)
#enleverBalles()
#gestionBonus(i)
#applyBonus(i, bonus1, frameleft=config.BONUS_LENGTH)


def nbBalle():
    global x, y, w, h, dx, dy, surfaces, bonus, bonus_frameleft
    if len(x)==len(y)==len(w)==len(h)==len(dx)==len(dy)==len(surfaces)==len(bonus)==len(bonus_frameleft):
        return len(x)
    else:
        raise IndexError("Les listes du package balles.py n'ont pas la même longueur.")



def move():
    global x, y, dx, dy, nbBalle, gestionBonus, enleverBalle

    ballesAenlever = []

    for i in range(nbBalle()):
        gestionBonus(i)
        x[i] += dx[i]
        y[i] += dy[i]
        if y[i] < config.HEIGHT:
            config.CANVAS.move(surfaces[i], dx[i], dy[i])
        else:
            ballesAenlever.append(i)

    ballesAenlever.sort(reverse=True)

    for i in ballesAenlever:
        enleverBalle(i)


def ajouterBalle(x1, y1, dx1=0, dy1=config.SPEED, bonus1="", bonus_frameleft1=0):
    global x, y, w, h, dx, dy, surfaces, bonus, bonus_frameleft, RAYON_BALLE

    x.append(x1)
    y.append(y1)
    w.append(RAYON_BALLE)
    h.append(RAYON_BALLE)
    dx.append(dx1)
    dy.append(dy1)
    surfaces.append(config.CANVAS.create_rectangle(x1, y1, x1+RAYON_BALLE, y1+RAYON_BALLE, fill="grey70", outline='grey70'))
    bonus.append(bonus1)
    bonus_frameleft.append(bonus_frameleft1)
    


def enleverBalle(i):
    global x, y, w, h, dx, dy, surfaces, bonus, bonus_frameleft, nbBalle

    if i < nbBalle() :
        x = x[:i]+x[i+1:]
        y = y[:i]+y[i+1:]
        w = w[:i]+w[i+1:]
        h = h[:i]+h[i+1:]
        dx = dx[:i]+dx[i+1:]
        dy = dy[:i]+dy[i+1:]
        config.CANVAS.delete(surfaces[i])
        surfaces = surfaces[:i]+surfaces[i+1:]
        bonus = bonus[:i]+bonus[i+1:]
        bonus_frameleft = bonus_frameleft[:i]+bonus_frameleft[i+1:]
    else:
        raise IndexError("L'indice "+i+" est > au nb de balles : "+nbBalle())



def enleverBalles():
    global x, y, w, h, dx, dy, surfaces, bonus, bonus_frameleft

    for surface in surfaces:
        config.CANVAS.delete(surface)
    x = []
    y = []
    w = []
    h = []
    dx = []
    dy = []
    surfaces = []
    bonus = []
    bonus_frameleft = []



def gestionBonus(i):
    global bonus_frameleft, applyBonus

    if bonus_frameleft[i]:
        bonus_frameleft[i] -= 1
        if bonus_frameleft[i] == 0:
            applyBonus(i, '')



def applyBonus(i, bonus1, frameleft=config.BONUS_LENGTH):
    global bonus, bonus_frameleft, surfaces

    bonus[i] = bonus1
    bonus_frameleft[i] = frameleft
    if bonus1=="balle_feu":
        config.CANVAS.itemconfig(surfaces[i], fill="orange red", outline="brown")
    elif bonus1=="":
        config.CANVAS.itemconfig(surfaces[i], fill="grey70", outline="grey70")
        bonus_frameleft[i]=0
