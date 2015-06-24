#!/usr/bin/python3
#-*- coding:utf-8 -*-

import config
from tkinter import *

x = []
y = []
w = []
h = []
dx = []
surfaces = []
bonus = []
bonus_frameleft = []


# Fonctions implémentées :

# nbBarre()
# move()
# draw()
# ajouterBarre(x1, y1, w1, h1, dx1, bonus1="", bonus_frameleft1=0)
# enleverBarre(i)
# enleverBarres()
# gestionBonus(i)
# applyBonus(i, bonus1, frameleft=config.BONUS_LENGTH)

def nbBarre():
    global x, y, w, h, dx, surfaces, bonus, bonus_frameleft
    if len(x)==len(y)==len(w)==len(h)==len(dx)==len(surfaces)==len(bonus)==len(bonus_frameleft):
        return len(x)
    else:
        raise IndexError("Les listes du package balles.py n'ont pas la même longueur.")


def move():
    global x, dx, nbBarre, draw, gestionBonus

    for i in range(nbBarre()):
        if x[i]+dx[i]>0 and x[i]+dx[i]+w[i]<config.WIDTH:
            x[i] += dx[i]
        gestionBonus(i)
    draw()



def draw():
    global x, y, w, h, surfaces, bonus, nbBarre

    for i in range(nbBarre()):
        config.CANVAS.coords(surfaces[i], x[i], y[i], x[i]+w[i], y[i]+h[i])



def ajouterBarre(x1, y1, w1=config.BARRE_W, h1=30, dx1=0, bonus1="", bonus_frameleft1=0):
    global x, y, w, h, dx, surfaces, bonus, bonus_frameleft

    x.append(x1)
    y.append(y1)
    w.append(w1)
    h.append(h1)
    dx.append(dx1)
    surfaces.append(config.CANVAS.create_rectangle(x1, y1, x1+w1, y1+h1, fill="grey25", outline="grey65"))
    bonus.append(bonus1)
    bonus_frameleft.append(bonus_frameleft1)
    


def enleverBarre(i):
    global x, y, w, h, dx, surfaces, bonus, bonus_frameleft, nbBarre

    if i < nbBarre() :
        x = x[:i]+x[i:]
        y = y[:i]+y[i:]
        w = w[:i]+w[i:]
        h = h[:i]+h[i:]
        dx = dx[:i]+dx[i:]
        config.CANVAS.delete(surfaces[i])
        surfaces = surfaces[:i]+surfaces[i:]
        bonus = bonus[:i]+bonus[i:]
        bonus_frameleft = bonus_frameleft[:i]+bonus_frameleft[i:]
    else:
        raise IndexError("L'indice "+i+" est > au nb de barres : "+nbBarre())


def enleverBarres():
    global x, y, w, h, dx, surfaces, bonus, bonus_frameleft
    x = []
    y = []
    w = []
    h = []
    dx = []
    for surface in surfaces:
        config.CANVAS.delete(surface)
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
    
    def resize(dw):
        w[i] += dw
        x[i] -= dw//2

    if bonus1=="":
        if bonus[i] == "barre_retrecie":
            resize(50)
        elif bonus[i] == "barre_agrandie":
            resize(-50)
        bonus_frameleft[i] = 0
        bonus[i] = ""

    elif bonus1=="barre_retrecie":
        if bonus[i]=="barre_agrandie":
            applyBonus(i, "")
        elif bonus[i]=="":
            resize(-50)
            bonus_frameleft[i]=frameleft
            bonus[i]="barre_retrecie"
        elif bonus[i]=="barre_retrecie":
            bonus_frameleft[i]=frameleft

    elif bonus1=="barre_agrandie":
        if bonus[i]=="barre_retrecie":
            applyBonus(i, "")
        elif bonus[i]=="":
            resize( 50)
            bonus_frameleft[i]=frameleft
            bonus[i]="barre_agrandie"
        elif bonus[i]=="barre_agrandie":
            bonus_frameleft[i]=frameleft

    else :
        print("Erreur :  Le bonus "+bonus1+" n'est pas connu par la barre.") 
