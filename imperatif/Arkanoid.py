#!/usr/bin/python3
#-*- coding:utf-8 -*-

from tkinter import *
from random import randrange
import balles, barres, briques, bonus, animationsArtifice, animationsExplosion, collisions, config

# Variables globales

SEED = "klqhnc!vcrcmzyt"
VIES = 3

# Fonctions

def update():
    global root, changerNiveau, VIES

    if briques.hasBriqueBreakable() or animationsExplosion.nbExplosion() or animationsArtifice.NBANIMATIONS:
        if balles.nbBalle() or bonus.nbBonus():
            collisions.gestionCollisions()
            balles.move()
            barres.move()
            bonus.move()
            animationsExplosion.explosionsMove()
            animationsArtifice.animationsArtificeMove()
            config.SPEED += config.SPEED_PER_FRAME
            root.after(1000//(config.FPS), update)
        elif VIES:
            VIES -= 1
            barres.enleverBarres()
            barres.ajouterBarre(config.WIDTH/2-100, 500)
            balles.enleverBalles()
            config.SPEED = config.BALLE_SPEED_INIT
            balles.ajouterBalle(config.WIDTH/2-10+randrange(-5, 5), 350)
            root.after(1000//(config.FPS), update)
        else:
            print("PERDU")
            root.quit()
    else:
        changerNiveau()

def depart():
    global update, SEED
    #ajout des briques
    briques.initialiserBriques(SEED)
    #ajout de la barre
    barres.ajouterBarre(config.WIDTH/2-100, 500)
    #ajout de la balle
    balles.ajouterBalle(config.WIDTH/2-10+randrange(-5, 5), 350)
    #mise en route du jeu
    update()

def changerNiveau():
    global SEED, update
    briques.enleverBriques()
    SEED += "0"
    briques.initialiserBriques(SEED)
    barres.enleverBarres()
    barres.ajouterBarre(config.WIDTH/2-100, 500)
    balles.enleverBalles()
    config.SPEED = config.BALLE_SPEED_INIT
    balles.ajouterBalle(config.WIDTH/2-10+randrange(-5, 5), 350)
    animationsArtifice.enleverAnimationsArtifice()
    animationsExplosion.enleverExplosions()
    bonus.enleverTousLesBonus()
    update()

# EVENT

def right_key(event):
    barres.dx[0] = config.BARRE_SPEED

def right_key_release(event):
    if barres.dx[0] > 0:
        barres.dx[0] = 0

def left_key(event):
    barres.dx[0] = -config.BARRE_SPEED

def left_key_release(event):
    if barres.dx[0]<0:
        barres.dx[0] = 0


# Créations des widgets

root = Tk()
root.title("Arkanoid")
root.minsize(width=config.WIDTH+5, height=config.HEIGHT+5)
config.CANVAS = Canvas(root, width=config.WIDTH, height=config.HEIGHT, bg="grey10")
config.CANVAS.pack() 

# Activation des touches directionnelles

root.bind('<Right>', right_key)
root.bind('<Left>', left_key)
root.bind('<KeyRelease-Right>', right_key_release)
root.bind('<KeyRelease-Left>', left_key_release)

#Demarrage du jeu

depart()
root.mainloop()
