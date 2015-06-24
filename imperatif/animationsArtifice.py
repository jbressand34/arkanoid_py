#!/usr/bin/python3
#-*- coding:utf-8 -*-


import config
from math import pi, sin, cos, sqrt
from random import randrange
from tkinter import * 

#feux d'artifice

#Animation

NBANIMATIONS = 0
RAYON_ANIMATION_ARTIFICE = 50
NBELEM_DEBUT_ANIMATION_ARTIFICE = 5
FRAMELEFT_DEBUT_ANIMATION_ARTIFICE = 90
PASELEM_ANIMATION_ARTIFICE = 50//NBELEM_DEBUT_ANIMATION_ARTIFICE

xAnimationArtifice = []
yAnimationArtifice = []
frameleftAnimationArtifice = []
nbElementsRestantsAnimationArtifice = []
nbElementsPresents = []

#Elements d'animations

COULEURS_ELEMENT_ARTIFICE = ['#99FF66','#FFCC33','#33FF00','#6600FF', '#00CCFF']
FRAMELEFT_DEBUT_ELEMENT_ARTIFICE = 50
NBLIGNES_ELEMENT_ARTIFICE = 14
LONGUEUR_TRAIT_ELEMENT_ARTIFICE = 10
THETA_ELEMENT_ARTIFICE = 2*pi/NBLIGNES_ELEMENT_ARTIFICE
COS_ELEMENT_ARTIFICE = []  #Le calcul du cos et du sin étant lourd, on l'enregistre
SIN_ELEMENT_ARTIFICE = []  # pour ne pas avoir à recalculer
for i in range(NBLIGNES_ELEMENT_ARTIFICE):
    COS_ELEMENT_ARTIFICE.append(cos(i*THETA_ELEMENT_ARTIFICE))
    SIN_ELEMENT_ARTIFICE.append(sin(i*THETA_ELEMENT_ARTIFICE))

xElementArtifice = [] #liste de listes
yElementArtifice = [] #liste de listes
frameleftElementArtifice = [] #liste de listes
rayonsElementArtifice = [] #liste de listes
numerosTraitsRestantsElementArtifice = [] #liste de listes de listes  aie aie aie
surfacesElementArtifice = []  #liste de listes de listes 


#Fonctions implémentées ici :

# animationsArtificeMove()
# animationArtificeMove(i)
# ajouterAnimationArtifice(x,y)
# enleverAnimationArtifice(i)
# enleverAnimationsArtifice()

# disparaitreTrait(i, j)
# elementArtificeMove(i, j)
# ajouterElementArtifice(i)
# enleverElementArtifice(i, j)


#Fonctions animation artifice



def animationsArtificeMove():
    global animationArtificeMove, enleverAnimationArtifice, NBANIMATIONS, nbElementsRestantsAnimationArtifice, PASELEM_ANIMATION_ARTIFICE, frameleftAnimationArtifice, nbElementsPresents, rayonsElementArtifice, frameleftElementArtifice, xElementArtifice, yElementArtifice, numerosTraitsRestantsElementArtifice


    animationsArtificeAenlever = []
    for i in range(NBANIMATIONS):
        if not frameleftAnimationArtifice[i]:
            animationsArtificeAenlever.append(i)
    
    #utilisation du multiprocessing pour afficher les feux d'artifice
    # source : http://stackoverflow.com/questions/4413821/multiprocessing-pool-example/4415314#4415314
    # ca a planté : FAIL
    #po = multiprocessing.Pool()
    #for i in range(len(animationsArtificeAconserver)):
        #po.apply_async(animationArtificeMove,(i,))

    #avec du multithreading
    #Reflexion : l'utilisation de thread est l'utilisation d'un processus qui jongle entre les threads et les exécutent petit à petit   
    #L'interet des thread n'est pas la puissance de calcul (car c'est toujours un seul processus qui effectue les threads), c'est utile lorsque une thread ne fait rien pendant un moment (par exemple l'attente de reponse du client depuis un serveur). Ou alors pour lisser les différentes taches : elles ne s'éxecutent plus les unes après les autres mais ensemble. Mais le temps total d'éxécution reste le meme.
    #Le multiprocessing permet l'utilisation de plusieurs processus : donc l'intéret évident est la puissance de calcul.
    #liens = []
    
    #for i in range(len(animationsArtificeAconserver)):
        #j = animationsArtificeAconserver[i]
        #a=threading.Thread(None, animationArtificeMove, None, (j,), {})
        #liens.append(a)
        #a.start()

    #for lien in liens:
        #print("On attend la fin du thread")
        #lien.join()
        #print("Fin du thread")


    #sans threading ni multiprocessing
    animationsArtificeAenlever.sort(reverse=True)
    for i in animationsArtificeAenlever:
        enleverAnimationArtifice(i)

    for i in range(NBANIMATIONS):
        frameleftAnimationArtifice[i] -= 1
        for j in range(nbElementsPresents[i]):
            frameleftElementArtifice[i][j] -= 1
        animationArtificeMove(i, NBANIMATIONS, nbElementsRestantsAnimationArtifice[i], nbElementsPresents[i], PASELEM_ANIMATION_ARTIFICE, frameleftAnimationArtifice[i], rayonsElementArtifice[i], frameleftElementArtifice[i], xElementArtifice[i], yElementArtifice[i], numerosTraitsRestantsElementArtifice[i])





def animationArtificeMove(i, nombre_animations, nombre_element_restant, nombre_element_present, pas_element, frameleft_animation, rayon_element, frameleft_element, x_element, y_element, numerosTraitsRestants):
    global ajouterElementArtifice, enleverElementArtifice, elementArtificeMove


    if i<nombre_animations:
        if frameleft_animation%pas_element == 0 and frameleft_animation > 40 and nombre_element_restant:
            ajouterElementArtifice(i)
            nombre_element_present += 1
        
        elementArtificeAenlever = []

        for j in range(nombre_element_present):
            if frameleft_element[j]>0:
                elementArtificeMove(i, j, nombre_element_present, rayon_element[j], frameleft_element[j], x_element[j], y_element[j], numerosTraitsRestants[j], nombre_animations)
            else:
                elementArtificeAenlever.append(j)

        elementArtificeAenlever.sort(reverse=True)

        for j in elementArtificeAenlever:
            if j < nombre_element_present:
                enleverElementArtifice(i, j)
                nombre_element_present -= 1
            else:
                raise IndexError("L'indice "+str(j)+" est supérieur au nombre d'éléments : "+str(nombre_element_present))

    return 0



def ajouterAnimationArtifice(x, y):
    global xAnimationArtifice, yAnimationArtifice, frameleftAnimationArtifice, nbElementsRestantsAnimationArtifice, xElementArtifice, yElementArtifice, frameleftElementArtifice, rayonsElementArtifice, numerosTraitsRestantsElementArtifice, surfacesElementArtifice, ajouterElementArtifice, FRAMELEFT_DEBUT_ELEMENT_ARTIFICE, NBELEM_DEBUT_ANIMATION_ARTIFICE, NBANIMATIONS, nbElementsPresents

    #création animation

    NBANIMATIONS += 1
    xAnimationArtifice.append(x)
    yAnimationArtifice.append(y)
    frameleftAnimationArtifice.append(FRAMELEFT_DEBUT_ANIMATION_ARTIFICE)
    nbElementsRestantsAnimationArtifice.append(NBELEM_DEBUT_ANIMATION_ARTIFICE)
    xElementArtifice.append([])
    yElementArtifice.append([])
    frameleftElementArtifice.append([])
    rayonsElementArtifice.append([])
    numerosTraitsRestantsElementArtifice.append([])
    surfacesElementArtifice.append([])
    nbElementsPresents.append(0)

    #ajout d'un élément Artifice

    nbElementsRestantsAnimationArtifice[NBANIMATIONS-1] -= 1
    ajouterElementArtifice(NBANIMATIONS-1)



def enleverAnimationArtifice(i):
    global xAnimationArtifice, yAnimationArtifice, frameleftAnimationArtifice, nbElementsRestantsAnimationArtifice, xElementArtifice, yElementArtifice, frameleftElementArtifice, rayonsElementArtifice, numerosTraitsRestantsElementArtifice, surfacesElementArtifice, enleverElementArtifice, nbElementsPresents, NBANIMATIONS


    if i < NBANIMATIONS:
        NBANIMATIONS -= 1
        for i in range(nbElementsPresents[i]):
            enleverElementArtifice(i, 0)
        xAnimationArtifice = xAnimationArtifice[:i]+xAnimationArtifice[i+1:]
        yAnimationArtifice = yAnimationArtifice[:i]+yAnimationArtifice[i+1:]
        frameleftAnimationArtifice = frameleftAnimationArtifice[:i]+frameleftAnimationArtifice[i+1:]
        nbElementsRestantsAnimationArtifice = nbElementsRestantsAnimationArtifice[:i]+nbElementsRestantsAnimationArtifice[i+1:]
        xElementArtifice = xElementArtifice[:i]+xElementArtifice[i+1:]
        yElementArtifice = yElementArtifice[:i]+yElementArtifice[i+1:]
        frameleftElementArtifice = frameleftElementArtifice[:i]+frameleftElementArtifice[i+1:]
        rayonsElementArtifice = rayonsElementArtifice[:i]+rayonsElementArtifice[i+1:]
        numerosTraitsRestantsElementArtifice = numerosTraitsRestantsElementArtifice[:i]+numerosTraitsRestantsElementArtifice[i+1:]
        surfacesElementArtifice = surfacesElementArtifice[:i]+surfacesElementArtifice[i+1:]
        nbElementsPresents = nbElementsPresents[:i]+nbElementsPresents[i+1:]

    else:
        raise IndexError("Echec enleverAnimationArtifice : l'indice "+str(i)+" est supérieur au nb d'animation : "+str(NBANIMATIONS))



def enleverAnimationsArtifice():
    global enleverAnimationArtifice, NBANIMATIONS

    for i in range(NBANIMATIONS):
        enleverAnimationArtifice(0)



#Fonctions élément artifice


def disparaitreTrait(i, j, numerosTraitsRestants):
    '''On fait disparaitre un des traits de l'élément d'animation'''
    global surfacesElementArtifice

    if len(numerosTraitsRestants):
        num1Trait = randrange(len(numerosTraitsRestants))
        num2Trait = numerosTraitsRestants[num1Trait]
      
        config.CANVAS.delete(surfacesElementArtifice[i][j][num1Trait])
        surfacesElementArtifice[i][j].remove(surfacesElementArtifice[i][j][num1Trait])
        numerosTraitsRestants.remove(num2Trait)

    return numerosTraitsRestants


def elementArtificeMove(i, j, nombre_element_present, rayon_element, frameleft_element, xElem, yElem, numerosTraitsRestants, nombre_animation):
    global disparaitreTrait, surfacesElementArtifice
    global COS_ELEMENT_ARTIFICE, SIN_ELEMENT_ARTIFICE

    if i<nombre_animation:
        if j<nombre_element_present:

            if frameleft_element <= 2*len(numerosTraitsRestants):
                numerosTraitsRestants = disparaitreTrait(i, j, numerosTraitsRestants)

            for k in range(len(numerosTraitsRestants)):
                cosTheta = COS_ELEMENT_ARTIFICE[numerosTraitsRestants[k]]
                sinTheta = SIN_ELEMENT_ARTIFICE[numerosTraitsRestants[k]]
                x1 = xElem + ((rayon_element*(50-frameleft_element)//50)*cosTheta)
                y1 = yElem - ((rayon_element*(50-frameleft_element)//50)*sinTheta)
                x01 = xElem + ((rayon_element*(49-frameleft_element)//50)*cosTheta)
                y01 = yElem - ((rayon_element*(49-frameleft_element)//50)*sinTheta)
                if x1!=x01 or y1!=y01:
                    config.CANVAS.move(surfacesElementArtifice[i][j][k], x1-x01, y1-y01)
        else:
            raise IndexError("Les listes dans le package animationsArtifice correspondants aux éléments de l'animation Artifice n°"+i+" n'ont pas la meme longueur." )
    else:
        raise IndexError("L'indice i est supérieure au nombre d'animations d'artifice : "+str(nombre_animation))



def ajouterElementArtifice(i):
    global xAnimationArtifice, yAnimationArtifice, xElementArtifice, yElementArtifice, frameleftElementArtifice, rayonsElementArtifice, numerosTraitsRestantsElementArtifice, surfacesElementArtifice, FRAMELEFT_DEBUT_ELEMENT_ARTIFICE, NBLIGNES_ELEMENT_ARTIFICE, COULEURS_ELEMENT_ARTIFICE, LONGUEUR_TRAIT_ELEMENT_ARTIFICE, COS_ELEMENT_ARTIFICE, SIN_ELEMENT_ARTIFICE, NBANIMATIONS, nbElementsPresents

    if i<NBANIMATIONS:
        nbElementsPresents[i] += 1
        xAnim = xAnimationArtifice[i]
        yAnim = yAnimationArtifice[i]
        distanceAnimationElement = randrange(50)
        rayonElementArtifice = 25+randrange(25)
        k = randrange(NBLIGNES_ELEMENT_ARTIFICE)
        xElem = xAnim + distanceAnimationElement*COS_ELEMENT_ARTIFICE[k]
        yElem = yAnim - distanceAnimationElement*SIN_ELEMENT_ARTIFICE[k]
        couleur = COULEURS_ELEMENT_ARTIFICE[randrange(5)] 
        numerosTraitsRestants = []
        surfaces = []
        for j in range(NBLIGNES_ELEMENT_ARTIFICE):
            numerosTraitsRestants.append(j)
            x2 = xElem + LONGUEUR_TRAIT_ELEMENT_ARTIFICE*COS_ELEMENT_ARTIFICE[j]
            y2 = yElem - LONGUEUR_TRAIT_ELEMENT_ARTIFICE*SIN_ELEMENT_ARTIFICE[j]
            surfaces.append(config.CANVAS.create_line(xElem, yElem, x2, y2, fill=couleur))


        xElementArtifice[i].append(xElem)
        yElementArtifice[i].append(yElem)
        frameleftElementArtifice[i].append(FRAMELEFT_DEBUT_ELEMENT_ARTIFICE)
        rayonsElementArtifice[i].append(rayonElementArtifice)
        numerosTraitsRestantsElementArtifice[i].append(numerosTraitsRestants)
        surfacesElementArtifice[i].append(surfaces)
    else:
        raise IndexError("L'indice "+i+" est supérieur au nombre d'animations d'artifice : "+str(NBANIMATIONS))



def enleverElementArtifice(i, j):
    global xElementArtifice, yElementArtifice, frameleftElementArtifice, rayonsElementArtifice, numerosTraitsRestantsElementArtifice, surfacesElementArtifice, NBANIMATIONS, nbElementsPresents

    if i<NBANIMATIONS:
        if j<nbElementsPresents[i]:
            nbElementsPresents[i] -= 1
            xElementArtifice[i] = xElementArtifice[i][:j]+xElementArtifice[i][j+1:]
            yElementArtifice[i] = yElementArtifice[i][:j]+yElementArtifice[i][j+1:]
            frameleftElementArtifice[i] = frameleftElementArtifice[i][:j]+frameleftElementArtifice[i][j+1:]
            rayonsElementArtifice[i] = rayonsElementArtifice[i][:j]+rayonsElementArtifice[i][j+1:]
            numerosTraitsRestantsElementArtifice[i] = numerosTraitsRestantsElementArtifice[i][:j] + numerosTraitsRestantsElementArtifice[i][j+1:]
            for surface in surfacesElementArtifice[i][j]:
                config.CANVAS.delete(surface)
            surfacesElementArtifice[i] = surfacesElementArtifice[i][:j]+surfacesElementArtifice[i][j+1:]
        else:
            raise IndexError("L'indice "+j+" est supérieur au nombre d'élément : "+nbElementsPresents()+", de l'animation de type artifice n°"+i)
    else:
        raise IndexError("L'indice "+i+" est supérieur au nb d'animations de type artifice : "+str(NBANIMATIONS))
