#!/usr/bin/python3
#-*- coding:utf-8 -*-

import config, animationsExplosion, animationsArtifice, bonus, procgen
from tkinter import *
from math import sqrt

RAYON_EXPLOSION = 100

briques = []  #liste contenant des tupes de la forme (x,y,w,h)
vies = []     #liste contenant des entiers
surfaces = [] #liste contenant des surfaces.
type = []    #liste contenant des string : "indestructible", "explosive"
bonus_contenu = [] #liste contenant des string : "ajout_balle", "balle_feu", "barre_retrecie", "barre_agrandie" ...


#Implémentation des fonctions

#hasBriqueBreakable()
#nbBrique()
#ajouterBrique(x1, y1, nbVie=1, type1="", bonus_contenu1="")
#draw(i) 
#enleverBrique(i)
#enleverBriques() 
#explosion(x, y)
#initialiserBriques(seed, difficulte=20)


def hasBriqueBreakable():
    global nbBrique, type
    retour = False

    i=0
    while i < nbBrique() and not retour:
        if type[i] != "indestructible":
            retour = True
        i += 1
    return retour

def nbBrique():
    '''Renvoie le nombre de briques'''
    global briques, vies, surfaces, type, bonus_contenu

    if len(briques)==len(vies)==len(surfaces)==len(bonus_contenu)==len(type):
        return len(briques)
    else:
        raise IndexError("Les listes contenues dans le package briques n'ont pas la meme longueur.")



def ajouterBrique(x1, y1, nbVie=1, type1="", bonus_contenu1=""):
    '''ajoute une brique'''

    global nbBrique, briques, vies, surfaces, type, bonus_contenu, draw

    briques.append((x1, y1, config.BRIQUE_W, config.BRIQUE_H))
    if nbVie >= config.BRIQUE_MIN_PV and nbVie <= config.BRIQUE_MAX_PV:
        vies.append(nbVie)
    else:
        raise ValueError("Erreur : tentative d'ajout de brique ayant un nombre de vies non acceptable : "+nbVie)
    surfaces.append(None)

    if type1 in config.BRIQUE_TYPE_B+config.BRIQUE_TYPE_M+[""]:
        type.append(type1)
    else:
        raise ValueError("Le type de brique "+type1+" n'est pas reconnu.")

    if bonus_contenu1 in config.BONUS+config.MALUS+[""]:
        bonus_contenu.append(bonus_contenu1)
    else:
        raise ValueError("Le bonus de brique "+bonus_contenu1+" n'est pas reconnu.")

    draw(nbBrique()-1)
    
    
        
def draw(i):
    '''Dessine la ieme brique.'''

    global nbBrique, briques, vies, surfaces, type, bonus_contenu

    if i<nbBrique():

        if surfaces[i]==None and vies[i]:
            surfaces[i] = config.CANVAS.create_rectangle(briques[i][0], briques[i][1], briques[i][0]+briques[i][2], briques[i][1]+briques[i][3], outline='blue', fill='green', tags=('unknown'))

        if vies[i]:
            if type[i]=="explosive":
                config.CANVAS.itemconfig(surfaces[i], width=(vies[i])//2, outline='indian red', fill='red3', tags=('brique'))
            elif type[i]=="indestructible":
                config.CANVAS.itemconfig(surfaces[i], width=2, outline='grey90', fill='grey80', tags=('brique'))
            else:
                config.CANVAS.itemconfig(surfaces[i], width=(vies[i])//2, outline='grey50', fill='grey'+str(15+vies[i]*5), tags=('brique'))
    else:
        raise ValueError("L'indice "+i+" de la brique à dessiner est supérieur au nombre de briques : "+nbBrique())



def enleverBrique(i):
    '''Enlève la ieme brique.'''
    global briques, vies, surfaces, type, bonus_contenu, nbBrique

    if i<nbBrique():
        briques = briques[:i]+briques[i+1:]
        vies = vies[:i]+vies[i+1:]
        type = type[:i]+type[i+1:]
        bonus_contenu = bonus_contenu[:i]+bonus_contenu[i+1:]
        config.CANVAS.delete(surfaces[i])
        surfaces = surfaces[:i]+surfaces[i+1:]
    else:
        raise ValueError("Erreur : l'indice de la brique à supprimer : "+i+" est supérieur au nombre de briques : "+nbBrique())


def enleverBriques():
    '''Enlève toutes les briques.'''
    global nbBrique, enleverBrique

    for i in range(nbBrique()):
        enleverBrique(0)
    

def explosion(x, y):
    '''créer une explosion infligeant un dégat aux briques environnantes'''

    global nbBrique, enleverBrique, briques, vies, type, bonus_contenu, RAYON_EXPLOSION


    #ca va etre dur a supprimer les briques
    #car chacune est désignée par un indice
    #seulement cette indice n'est plus valable 
    #si une des brique a été enlevé
    # l'indice change
    
    explosions = [] #contient des tuples de la forme (x,y)

    i = 0

    for j in range(nbBrique()):
        #Si un des coins de la brique est dans le rayon de l'explosion alors la brique est touché
        
        #distance du centre de l'explosion par rapport au coin supérieure gauche de la brique.
        r1 = sqrt((x-briques[i][0])**2+(y-briques[i][1])**2) 
        #coin supérieur droit.
        r2 = sqrt((x-briques[i][0]-briques[i][2])**2+(y-briques[i][1])**2) 
        #coin inférieur gauche.
        r3 = sqrt((x-briques[i][0])**2+(y-briques[i][1]-briques[i][3])**2) 
        #coin inferieur droit.
        r4 = sqrt((x-briques[i][0]-briques[i][2])**2+(y-briques[i][1]-briques[i][3])**2) 


        #Si la brique est dans le rayon de l'explosion
        if r1<RAYON_EXPLOSION or r2<RAYON_EXPLOSION or r3<RAYON_EXPLOSION or r4<RAYON_EXPLOSION:
            xAnim = briques[i][0]+briques[i][2]//2
            yAnim = briques[i][1]+briques[i][3]//2
            if type[i] == "indestructible":
                #on increment l'indice
                i += 1

            elif type[i] == "explosive":
                #on ajoute une explosion
                #on supprime la brique
                animationsExplosion.ajouterExplosion(xAnim, yAnim)
                explosions.append((xAnim,yAnim))
                enleverBrique(i)

                    
            elif type[i] == "" :
                #on creer un bonus
                #on creer un feu d'artifice
                #on supprime la brique
                if bonus_contenu[i] != "":
                    bonus.ajouterBonus(xAnim, yAnim, bonus_contenu[i])
                animationsArtifice.ajouterAnimationArtifice(xAnim, yAnim)
                enleverBrique(i)
        #si la brique n'est pas dans le rayon de l'explosion
        else:
            i += 1

    for tuple in explosions:
        explosion(tuple[0], tuple[1])




def initialiserBriques(seed, difficulte=20):
    global ajouterBrique, enleverBriques

    enleverBriques()
    dicoBriques = procgen.procgen(seed, difficulte)
    for dico in dicoBriques:
        ajouterBrique(dico['x'], dico['y'], dico['pv'], dico['bonus'], dico['bonus_contenu'])
