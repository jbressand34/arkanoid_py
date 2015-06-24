#!/usr/bin/python3
#-*- coding:utf-8 -*-


import config
from math import pi, sin, cos, sqrt
from random import randrange
from tkinter import *

#explosion

#Animation

RAYON_APPARITION_TORNADE = 30
RAYON_APPARITION_ETINCELLE = 70
NBELEM_DEBUT_TORNADE = 3
NBELEM_DEBUT_ETINCELLE = 10
FRAMELEFT_DEBUT_EXPLOSION = 90
PASELEM_APPARITION_TORNADE = 50//NBELEM_DEBUT_TORNADE
PASELEM_APPARITION_ETINCELLE = 50//NBELEM_DEBUT_ETINCELLE

xExplosion = []
yExplosion = []
frameleftExplosion = []
nbTornadesRestantesExplosion = []
nbEtincellesRestantesExplosion = []

#Tornade

COULEURS_TORNADE = ['grey','orange','white']
FRAMELEFT_DEBUT_TORNADE = 50
DIAMETRE_BOULE = 30
ECART_BOULE_CENTRE = 3

xTornade = [] #liste de listes
yTornade = [] #liste de listes
frameleftTornade = [] #liste de listes
surfacesTornade = []  #liste de listes de listes 

#Etincelle

RAYON_CARRE = 5
FRAMELEFT_DEBUT_ETINCELLE = 50
NBCOUCHES_ETINCELLE = 4

xEtincelle = [] #liste de listes
yEtincelle = [] #liste de listes
frameleftEtincelle = [] #liste de listes
surfacesEtincelle = [] #liste de listes de listes

#Fonctions implémentées ici :

# nbExplosion()
# explosionsMove()
# explosionMove(i)
# ajouterExplosion(x,y)
# enleverExplosion(i)
# enleverExplosions()

# nbTornade(i)
# tornadeMove(i, j)
# ajouterTornade(i)
# enleverTornade(i, j)

# nbEtincelle()
# etincelleMove(i, j)
# ajouterEtincelle(i)
# enleverEtincelle(i, j)

#Fonctions animation artifice



def nbExplosion():
    global xExplosion, yExplosion, frameleftExplosion, nbTornadesRestantesExplosion, nbEtincellesRestantesExplosion, xTornade, yTornade, frameleftTornade, surfacesTornade, xEtincelle, yEtincelle, frameleftEtincelle, surfacesEtincelle

    if len(xExplosion)==len(yExplosion)==len(frameleftExplosion)==len(nbTornadesRestantesExplosion)==len(nbEtincellesRestantesExplosion)==len(xTornade)==len(yTornade)==len(frameleftTornade)==len(surfacesTornade)==len(xEtincelle)==len(yEtincelle)==len(frameleftEtincelle)==len(surfacesEtincelle):
        return len(xExplosion)
    else:
        raise IndexError("Les listes du package animationsExplosion.py n'ont pas la meme longueur.")



def explosionsMove():
    global nbExplosion, explosionMove, enleverExplosion, frameleftExplosion

    explosionsAenlever = []

    for i in range(nbExplosion()):
        frameleftExplosion[i] -= 1
        if frameleftExplosion[i]:
            explosionMove(i)
        else:
            explosionsAenlever.append(i)

    explosionsAenlever.sort(reverse=True)
    for i in explosionsAenlever:
        enleverExplosion(i)



def explosionMove(i):
    global frameleftExplosion, frameleftTornade, frameleftEtincelle, ajouterTornade, ajouterEtincelle, enleverTornade, enleverEtincelle, tornadeMove, etincelleMove, nbTornadesRestantesExplosion, nbEtincellesRestantesExplosion, nbTornade, nbEtincelle, PASELEM_APPARITION_ETINCELLE, PASELEM_APPARITION_TORNADE

    if frameleftExplosion[i]%PASELEM_APPARITION_ETINCELLE == 0 and frameleftExplosion[i] > 40 and nbEtincellesRestantesExplosion[i]:
        nbEtincellesRestantesExplosion[i] -= 1
        ajouterEtincelle(i)

    if frameleftExplosion[i]%PASELEM_APPARITION_TORNADE == 0 and frameleftExplosion[i] > 40 and nbTornadesRestantesExplosion[i]:
        nbTornadesRestantesExplosion[i] -= 1
        ajouterTornade(i)
        
    tornadesAenlever = []
    etincellesAenlever = []

    for j in range(nbTornade(i)):
        frameleftTornade[i][j] -= 1
        if frameleftTornade[i][j]:
            tornadeMove(i, j)
        else:
            tornadesAenlever.append(j)

    for j in tornadesAenlever:
        enleverTornade(i, j)

    for j in range(nbEtincelle(i)):
        frameleftEtincelle[i][j] -= 1
        if frameleftEtincelle[i][j]:
            etincelleMove(i, j)
        else:
            etincellesAenlever.append(j)

    for j in etincellesAenlever:
        enleverEtincelle(i, j)




def ajouterExplosion(x, y):
    global xExplosion, yExplosion, frameleftExplosion, nbTornadesRestantesExplosion, nbEtincellesRestantesExplosion, xTornade, yTornade, xEtincelle, yEtincelle, frameleftTornade, frameleftEtincelle, surfacesTornade, surfacesEtincelle, ajouterTornade, ajouterEtincelle, nbExplosion, FRAMELEFT_DEBUT_EXPLOSION, FRAMELEFT_DEBUT_TORNADE, FRAMELEFT_DEBUT_ETINCELLE, NBELEM_DEBUT_TORNADE, NBELEM_DEBUT_ETINCELLE

    #création animation

    xExplosion.append(x)
    yExplosion.append(y)
    frameleftExplosion.append(FRAMELEFT_DEBUT_EXPLOSION)
    nbTornadesRestantesExplosion.append(NBELEM_DEBUT_TORNADE)
    nbEtincellesRestantesExplosion.append(NBELEM_DEBUT_ETINCELLE)
    xTornade.append([])
    yTornade.append([])
    frameleftTornade.append([])
    surfacesTornade.append([])
    xEtincelle.append([])
    yEtincelle.append([])
    frameleftEtincelle.append([])
    surfacesEtincelle.append([])

    #ajout d'un élément Tornade

    nbTornadesRestantesExplosion[nbExplosion()-1] -= 1
    ajouterTornade(nbExplosion()-1)

    #ajout d'un élément Etincelle

    nbEtincellesRestantesExplosion[nbExplosion()-1] -= 1
    ajouterEtincelle(nbExplosion()-1)




def enleverExplosion(i):
    global xExplosion, yExplosion, frameleftExplosion, nbTornadesRestantesExplosion, nbEtincellesRestantesExplosion, xTornade, yTornade, frameleftTornade, surfacesTornade, xEtincelle, yEtincelle, frameleftEtincelle, surfacesEtincelle, enleverTornade, enleverEtincelle, nbExplosion, nbTornade, nbEtincelle


    if i < nbExplosion():

        for j in range(nbTornade(i)):
            enleverTornade(i, 0)
        for j in range(nbEtincelle(i)):
            enleverEtincelle(i, 0)

        xExplosion = xExplosion[:i]+xExplosion[i+1:]
        yExplosion = yExplosion[:i]+yExplosion[i+1:]
        frameleftExplosion = frameleftExplosion[:i]+frameleftExplosion[i+1:]
        nbTornadesRestantesExplosion = nbTornadesRestantesExplosion[:i]+nbTornadesRestantesExplosion[i+1:]
        nbEtincellesRestantesExplosion = nbEtincellesRestantesExplosion[:i]+nbEtincellesRestantesExplosion[i+1:]
        xTornade = xTornade[:i]+xTornade[i+1:]
        yTornade = yTornade[:i]+yTornade[i+1:]
        frameleftTornade = frameleftTornade[:i]+frameleftTornade[i+1:]
        surfacesTornade = surfacesTornade[:i]+surfacesTornade[i+1:]

        xEtincelle = xEtincelle[:i]+xEtincelle[i+1:]
        yEtincelle = yEtincelle[:i]+yEtincelle[i+1:]
        frameleftEtincelle = frameleftEtincelle[:i]+frameleftEtincelle[i+1:]
        surfacesEtincelle = surfacesEtincelle[:i]+surfacesEtincelle[i+1:]

    else:
        raise IndexError("Echec enleverExplosion : l'indice "+str(i)+" est supérieur au nb d'explosion : "+str(nbExplosion()))



def enleverExplosions():
    global enleverExplosion, nbExplosion

    for i in range(nbExplosion()):
        enleverExplosion(0)



#Fonctions Tornade


def nbTornade(i):
    global nbExplosion, xTornade, yTornade, frameleftTornade, surfacesTornade

    if i<nbExplosion():
        if len(xTornade[i])==len(yTornade[i])==len(frameleftTornade[i])==len(surfacesTornade[i]):
            return len(xTornade[i])
        else:
            raise IndexError("Les listes dans le package animationsExplosions correspondantes aus tornades de l'explosion n°"+i+" n'ont pas la meme longueur." )
    else:
        raise IndexError("L'indice i est supérieure au nombre d'explosions : "+nbExplosion())



def tornadeMove(i, j):
    global nbExplosion, nbTornade, xTornade, yTornade, frameleftTornade, surfacesTornade, COULEURS_TORNADE, ECART_BOULE_CENTRE, DIAMETRE_BOULE

    if i<nbExplosion():
        if j<nbTornade(i):

            k = frameleftTornade[i][j]%3
            
            for l in range(3):
                theta = (pi/6)+((k+l)%3)*2*pi/3
                xBoule = xTornade[i][j] + ECART_BOULE_CENTRE*cos(theta) - DIAMETRE_BOULE//2
                yBoule = yTornade[i][j] - ECART_BOULE_CENTRE*cos(theta) - DIAMETRE_BOULE//2
                config.CANVAS.coords(surfacesTornade[i][j][l], xBoule, yBoule, xBoule+DIAMETRE_BOULE, yBoule+DIAMETRE_BOULE)

        else:
            raise IndexError("Les listes dans le package animationsExplosion correspondants aux tornades de l'explosion n°"+i+" n'ont pas la meme longueur." )
    else:
        raise IndexError("L'indice i est supérieure au nombre d'explosions : "+nbExplosion())




def ajouterTornade(i):
    global nbExplosion, xExplosion, yExplosion, xTornade, yTornade, frameleftTornade, surfacesTornade, FRAMELEFT_DEBUT_TORNADE, COULEURS_TORNADE, RAYON_APPARITION_TORNADE, DIAMETRE_BOULE, ECART_BOULE_CENTRE 

    if i<nbExplosion():
        xAnim = xExplosion[i]
        yAnim = yExplosion[i]
        distanceAnimationElement = randrange(RAYON_APPARITION_TORNADE)
        thetaElement = randrange(24)*pi/12
        xElem = xAnim + distanceAnimationElement*cos(thetaElement)
        yElem = yAnim - distanceAnimationElement*sin(thetaElement)
        surfaces = []
        for j in range(3):
            theta = (pi/6)+j*2*pi/3
            xBoule = xElem + (ECART_BOULE_CENTRE*cos(theta)) - DIAMETRE_BOULE//2
            yBoule = yElem - (ECART_BOULE_CENTRE*sin(theta)) - DIAMETRE_BOULE//2
            surfaces.append(config.CANVAS.create_oval(xBoule, yBoule, xBoule+DIAMETRE_BOULE, yBoule+DIAMETRE_BOULE, fill=COULEURS_TORNADE[j], outline=COULEURS_TORNADE[j]))

        xTornade[i].append(xElem)
        yTornade[i].append(yElem)
        frameleftTornade[i].append(FRAMELEFT_DEBUT_TORNADE)
        surfacesTornade[i].append(surfaces)
    else:
        raise IndexError("L'indice "+i+" est supérieur au nombre d'explosion : "+nbExplosion())



def enleverTornade(i, j):
    global nbExplosion, nbTornade, xTornade, yTornade, frameleftTornade, surfacesTornades

    if i<nbExplosion():
        if j<nbTornade(i):
            xTornade[i] = xTornade[i][:j]+xTornade[i][j+1:]
            yTornade[i] = yTornade[i][:j]+yTornade[i][j+1:]
            frameleftTornade[i] = frameleftTornade[i][:j]+frameleftTornade[i][j+1:]

            for surface in surfacesTornade[i][j]:
                config.CANVAS.delete(surface)
            surfacesTornade[i] = surfacesTornade[i][:j]+surfacesTornade[i][j+1:]
        else:
            raise IndexError("L'indice "+j+" est supérieur au nombre de tornade : "+nbTornade()+", de l'explosion n°"+i)
    else:
        raise IndexError("L'indice "+i+" est supérieur au nb d'explosion : "+nbExplosion())




#Fonctions Etincelle


def nbEtincelle(i):
    global nbExplosion, xEtincelle, yEtincelle, frameleftEtincelle, surfacesEtincelle

    if i<nbExplosion():
        if len(xEtincelle[i])==len(yEtincelle[i])==len(frameleftEtincelle[i])==len(surfacesEtincelle[i]):
            return len(xEtincelle[i])
        else:
            raise IndexError("Les listes dans le package animationsExplosions correspondantes aus tornades de l'explosion n°"+i+" n'ont pas la meme longueur." )
    else:
        raise IndexError("L'indice i est supérieure au nombre d'explosions : "+nbExplosion())



def etincelleMove(i, j):
    global nbExplosion, nbEtincelle, xEtincelle, yEtincelle, frameleftEtincelle, surfacesEtincelle

    if i<nbExplosion():
        if j<nbEtincelle(i):

            if frameleftEtincelle[i][j]%4 == 0:
                if len(surfacesEtincelle[i][j])>1:
                    config.CANVAS.delete(surfacesEtincelle[i][j][0])
                    config.CANVAS.delete(surfacesEtincelle[i][j][1])
                    surfacesEtincelle[i][j] = surfacesEtincelle[i][j][2:]
                else:
                    for surface in surfacesEtincelle[i][j]:
                        config.CANVAS.delete(surface)
                    surfacesEtincelle[i][j] = []
        else:
            raise IndexError("Les listes dans le package animationsExplosion correspondants aux étincelles de l'explosion n°"+i+" n'ont pas la meme longueur." )
    else:
        raise IndexError("L'indice i est supérieure au nombre d'explosions : "+nbExplosion())



def ajoutCarre(i, iCarre, jCarre):
    global xEtincelle, yEtincelle, surfacesEtincelle, RAYON_CARRE, NBCOUCHES_ETINCELLE

    j = len(surfacesEtincelle[i])-1

    xOrigin = xEtincelle[i][j] - RAYON_CARRE//2 - (NBCOUCHES_ETINCELLE - 1)*RAYON_CARRE
    yOrigin = yEtincelle[i][j] - RAYON_CARRE//2 - (NBCOUCHES_ETINCELLE - 1)*RAYON_CARRE
    xCarre = xOrigin + iCarre*RAYON_CARRE
    yCarre = yOrigin + jCarre*RAYON_CARRE
    surfacesEtincelle[i][j].append(config.CANVAS.create_rectangle(xCarre, yCarre, xCarre+RAYON_CARRE, yCarre+RAYON_CARRE, fill='red', outline='red'))


def ajouterEtincelle(i):
    global ajoutCarre, nbExplosion, xExplosion, yExplosion, xEtincelle, yEtincelle, frameleftEtincelle, surfacesEtincelle, FRAMELEFT_DEBUT_ETINCELLE, RAYON_APPARITION_ETINCELLE, NBCOUCHES_ETINCELLE

    if i<nbExplosion():
        xAnim = xExplosion[i]
        yAnim = yExplosion[i]
        distanceAnimationElement = randrange(RAYON_APPARITION_ETINCELLE)
        thetaElement = randrange(24)*pi/12
        xElem = xAnim + distanceAnimationElement*cos(thetaElement)
        yElem = yAnim - distanceAnimationElement*sin(thetaElement)
        surfacesEtincelle[i].append([])
        xEtincelle[i].append(xElem)
        yEtincelle[i].append(yElem)
        frameleftEtincelle[i].append(FRAMELEFT_DEBUT_ETINCELLE)

        gauche = []
        droite = []
        haut = []
        bas = []

        iCarre = 0
        jCarre = 0
        for nbCouche in range(NBCOUCHES_ETINCELLE):
            if nbCouche != 0:
                iCarre += 1
                jCarre += 1

            for k in range(3-nbCouche):
                gauche.append((0, 2*k))
                droite.append((2*(3-nbCouche), 2*k+2))
                haut.append((2*k+2,0))
                bas.append((2*k, 2*(3-nbCouche)))

            for k in range(3-nbCouche):
                ugauche = gauche[randrange(len(gauche))]
                udroite = droite[randrange(len(droite))]
                uhaut =   haut[randrange(len(haut))]
                ubas = bas[randrange(len(bas))]
                ajoutCarre(i, iCarre+ugauche[0], jCarre+ugauche[1])
                ajoutCarre(i, iCarre+udroite[0], jCarre+udroite[1])
                ajoutCarre(i, iCarre+uhaut[0], jCarre+uhaut[1])
                ajoutCarre(i, iCarre+ubas[0], jCarre+ubas[1])
                gauche.remove(ugauche)
                droite.remove(udroite)
                haut.remove(uhaut)
                bas.remove(ubas)

            if nbCouche == NBCOUCHES_ETINCELLE -1:
                ajoutCarre(i, iCarre, jCarre)

    else:
        raise IndexError("L'indice "+i+" est supérieur au nombre d'explosion : "+nbExplosion())



def enleverEtincelle(i, j):
    global nbExplosion, nbEtincelle, xEtincelle, yEtincelle, frameleftEtincelle, surfacesEtincelles

    if i<nbExplosion():
        if j<nbEtincelle(i):
            xEtincelle[i] = xEtincelle[i][:j]+xEtincelle[i][j+1:]
            yEtincelle[i] = yEtincelle[i][:j]+yEtincelle[i][j+1:]
            frameleftEtincelle[i] = frameleftEtincelle[i][:j]+frameleftEtincelle[i][j+1:]

            for surface in surfacesEtincelle[i][j]:
                config.CANVAS.delete(surface)
            surfacesEtincelle[i] = surfacesEtincelle[i][:j]+surfacesEtincelle[i][j+1:]
        else:
            raise IndexError("L'indice "+j+" est supérieur au nombre d'étincelle : "+nbEtincelle()+", de l'explosion n°"+i)
    else:
        raise IndexError("L'indice "+i+" est supérieur au nb d'explosion : "+nbExplosion())
