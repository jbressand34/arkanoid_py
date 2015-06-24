#!/usr/bin/python3
#-*- coding:utf-8 -*-


import config
from tkinter import *

x = []
y = []
w = []
h = []
dx = []
dy = []
surfaces = []
bonus_contenu = []

# Fonctions implémentées :

#nbBonus()
#move()
#draw()
#ajouterBonus(x, y, bonusContenu, dy=config.BONUS_SPEED)
#enleverBonus(i)
#enleverTousLesBonus()

def nbBonus():
    global x, y, w, h, dx, dy, surfaces, bonus_contenu
    if len(x)==len(y)==len(w)==len(h)==len(dx)==len(dy)==len(surfaces)==len(bonus_contenu):
        return len(x)
    else:
        raise IndexError("Les listes du package bonus.py n'ont pas la même longueur : x : "+str(len(x))+",y : "+str(len(y))+",w : "+str(len(w))+",h : "+str(len(h))+",dx : "+str(len(dx))+",dy : "+str(len(dy))+",bonus_contenu : "+str(len(bonus_contenu))+",surfaces : "+str(len(surfaces)))
    


def move():
    global y, dy, nbBonus, draw
    
    for i in range(nbBonus()):
        y[i]+=dy[i]
    draw()



def draw():
    global dx, dy, surfaces

    for i in range(nbBonus()):
        for surface in surfaces[i]:
            config.CANVAS.move(surface, dx[i], dy[i])



def ajouterBonus(x1, y1, bonus_contenu1, dy1=config.BONUS_SPEED):
    global x, y, w, h, dx, dy, surfaces, bonus_contenu

    if bonus_contenu1 == "":
        raise ValueError("Erreur tentative de creer un bonus vide")

    x.append(x1)
    y.append(y1)
    w.append(20)
    h.append(20)
    dx.append(0)
    dy.append(dy1)
    bonus_contenu.append(bonus_contenu1)
    surfaces.append([])
    surfaces1 = []

    surfaces1.append(config.CANVAS.create_rectangle(x1, y1, x1+20, y1+20, outline='grey70', fill='purple'))

    if bonus_contenu1 in config.BONUS:
        config.CANVAS.itemconfig(surfaces1[0], outline='dark green', fill='green3')

        if bonus_contenu1 == "barre_agrandie":
            surfaces1.append(config.CANVAS.create_polygon([x[nbBonus()-1]+w[nbBonus()-1]/2-1, y[nbBonus()-1]+4, x[nbBonus()-1]+3, y[nbBonus()-1]+h[nbBonus()-1]/2, x[nbBonus()-1]+w[nbBonus()-1]/2-1, y[nbBonus()-1]+h[nbBonus()-1]-4], outline='yellow4', fill='yellow2', width=1))

            surfaces1.append(config.CANVAS.create_polygon([x[nbBonus()-1]+w[nbBonus()-1]/2+1, y[nbBonus()-1]+4, x[nbBonus()-1]+w[nbBonus()-1]-3, y[nbBonus()-1]+h[nbBonus()-1]/2,x[nbBonus()-1]+w[nbBonus()-1]/2+1, y[nbBonus()-1]+h[nbBonus()-1]-4], outline='yellow4', fill='yellow2', width=1))


        elif bonus_contenu1 == "ajout_balle":
            surfaces1.append(config.CANVAS.create_polygon([x[nbBonus()-1]+4, y[nbBonus()-1]+h[nbBonus()-1]/2-2, x[nbBonus()-1]+w[nbBonus()-1]/2-2, y[nbBonus()-1]+h[nbBonus()-1]/2-2, x[nbBonus()-1]+w[nbBonus()-1]/2-2, y[nbBonus()-1]+4, x[nbBonus()-1]+w[nbBonus()-1]/2+2, y[nbBonus()-1]+4, x[nbBonus()-1]+w[nbBonus()-1]/2+2, y[nbBonus()-1]+h[nbBonus()-1]/2-2,x[nbBonus()-1]+w[nbBonus()-1]-4, y[nbBonus()-1]+h[nbBonus()-1]/2-2, x[nbBonus()-1]+w[nbBonus()-1]-4, y[nbBonus()-1]+h[nbBonus()-1]/2+2, x[nbBonus()-1]+w[nbBonus()-1]/2+2, y[nbBonus()-1]+h[nbBonus()-1]/2+2, x[nbBonus()-1]+w[nbBonus()-1]/2+2, y[nbBonus()-1]+h[nbBonus()-1]-4, x[nbBonus()-1]+w[nbBonus()-1]/2-2, y[nbBonus()-1]+h[nbBonus()-1]-4, x[nbBonus()-1]+w[nbBonus()-1]/2-2, y[nbBonus()-1]+h[nbBonus()-1]/2+2, x[nbBonus()-1]+4, y[nbBonus()-1]+h[nbBonus()-1]/2+2], outline='yellow4', fill='yellow2', width=1))

        elif bonus_contenu1 == "balle_feu":
            surfaces1.append(config.CANVAS.create_rectangle(x[nbBonus()-1]+5, y[nbBonus()-1]+5, x[nbBonus()-1]+w[nbBonus()-1]-5, y[nbBonus()-1]+h[nbBonus()-1]-5, outline='yellow4', fill='red2', width=1))


    elif bonus_contenu1 in config.MALUS:
        config.CANVAS.itemconfig(surfaces1[0], outline='dark red', fill='red3')

        if bonus_contenu1 == 'barre_retrecie':
            surfaces1.append(config.CANVAS.create_polygon([x[nbBonus()-1]+3, y[nbBonus()-1]+4, x[nbBonus()-1]+w[nbBonus()-1]/2-1, y[nbBonus()-1]+h[nbBonus()-1]/2, x[nbBonus()-1]+3, y[nbBonus()-1]+h[nbBonus()-1]-4], outline='yellow4', fill='yellow2', width=1))

            surfaces1.append(config.CANVAS.create_polygon([x[nbBonus()-1]+w[nbBonus()-1]-3, y[nbBonus()-1]+4, x[nbBonus()-1]+w[nbBonus()-1]/2+1, y[nbBonus()-1]+h[nbBonus()-1]/2, x[nbBonus()-1]+w[nbBonus()-1]-3, y[nbBonus()-1]+h[nbBonus()-1]-4], outline='yellow4', fill='yellow2', width=1))

    else:
        raise ValueError("Le bonus "+bonus_contenu1+" n'est pas connu.")

    surfaces[nbBonus()-1] = surfaces1


def enleverBonus(i):
    global x, y, w, h, dx, dy, surfaces, bonus_contenu, nbBonus

    if i<nbBonus():
        x = x[:i]+x[i+1:]
        y = y[:i]+y[i+1:]
        w = w[:i]+w[i+1:]
        h = h[:i]+h[i+1:]
        dx = dx[:i]+dx[i+1:]
        dy = dy[:i]+dy[i+1:]

        for surface in surfaces[i]:
            config.CANVAS.delete(surface)
            
        surfaces = surfaces[:i]+surfaces[i+1:]
        bonus_contenu = bonus_contenu[:i]+bonus_contenu[i+1:]
    else:
        raise IndexError("L'indice "+i+" est > au nb de bonus : "+nbBonus())



def enleverTousLesBonus():
    global nbBonus, enleverBonus

    for i in range(nbBonus()):
        enleverBonus(0)
