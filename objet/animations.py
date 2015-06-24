#!/usr/bin/python3

from tkinter import *
from element_jeu import *
from math import pi, cos, sin
from random import randrange
import config

'''
NOTE : Implémentation des classes Animation et ElemAnim.
Pour l'instant, seule l fu d'artifice est implémenté.
'''

class AnimationFeuArtifice(Rect):
    def __init__(self, x, y):
        Rect.__init__(self, x, y, 0, 0)
        self.frameleft = 90
        self.rayon = 50
        self.elements = list()
        self.nbElem = 5
        self.pasElem = 50//self.nbElem
        # on créer un élément
        self.ajouterElemAnim()
        self.nbElem -= 1

    def ajouterElemAnim(self):
        rayon = randrange(self.rayon)
        theta = randrange(24)*pi//12
        xelem = self.x + rayon*cos(theta)
        yelem = self.y - rayon*sin(theta)
        self.elements.append(ElemAnimFeuArtifice(xelem, yelem))
        self.elements[len(self.elements)-1].draw()

    def draw(self):
        pass

    def move(self):
        self.frameleft -= 1
        if self.frameleft%self.pasElem == 0 and self.frameleft > 40 and self.nbElem:
            self.ajouterElemAnim()
        for element in self.elements:
            if element.frameleft :
                element.move() 
            else:
                element.die()

    def die(self):
        for elem in self.elements:
            elem.die()

class ElemAnimFeuArtifice(Rect):
    def __init__(self, x, y):
        Rect.__init__(self, x, y, 0, 0)
        self.frameleft = 50
        self.rayonFeuArtifice = 20 + randrange(30) # rayon du feu d'artifice atteint à son apogée 
        self.nblignes = 14
        self.theta = 2*pi/self.nblignes
        self.cosAngle = []
        self.sinAngle = []
        self.numerosTraitsRestants = []
        for i in range(self.nblignes):
            self.numerosTraitsRestants.append(i)
            self.cosAngle.append(cos(i*self.theta))
            self.sinAngle.append(sin(i*self.theta))
        self.longueurTrait = 10
        self.couleurs=['#99FF66','#FFCC33','#33FF00','#6600FF', '#00CCFF']
        self.couleur = self.couleurs[randrange(5)]
        self.surfaces = list()

    def draw(self):
        for i in range(self.nblignes):
            x2 = self.x + self.longueurTrait*self.cosAngle[i]
            y2 = self.y - self.longueurTrait*self.sinAngle[i]
            self.surfaces.append(config.CANVAS.create_line(self.x, self.y, x2, y2, fill=self.couleur))

    def move(self):
        self.frameleft -= 1

        #à la fin, on fait disparaitre une ligne toutes les deux frames
        if self.frameleft <= 2*self.nblignes:
            self.disparaitreTrait()
        for i in range(self.nblignes):
            cosTheta = self.cosAngle[self.numerosTraitsRestants[i]]
            sinTheta = self.sinAngle[self.numerosTraitsRestants[i]]
            x1 = self.x + (self.rayonFeuArtifice*(50-self.frameleft)//50)*cosTheta
            y1 = self.y - (self.rayonFeuArtifice*(50-self.frameleft)//50)*sinTheta
            x01 = self.x + (self.rayonFeuArtifice*(49-self.frameleft)//50)*cosTheta
            y01 = self.y - (self.rayonFeuArtifice*(49-self.frameleft)//50)*sinTheta
            if x1!=x01 or y1!=y01:
                config.CANVAS.move(self.surfaces[i], x1-x01, y1-y01)


    def die(self):
        for surface in self.surfaces:
            config.CANVAS.delete(surface)

    def disparaitreTrait(self):
        '''On fait disparaitre un des traits au hasard'''
        if self.nblignes:
            num1Trait = randrange(self.nblignes)
            num2Trait = self.numerosTraitsRestants[num1Trait]

            config.CANVAS.delete(self.surfaces[num1Trait])
            self.surfaces.remove(self.surfaces[num1Trait])
            self.numerosTraitsRestants.remove(num2Trait)
            self.nblignes -= 1


class AnimationExplosion(Rect):
    def __init__(self, x, y):
        Rect.__init__(self, x, y, 0, 0)
        self.frameleft = 90
        self.rayonTornades = 30
        self.rayonEtincelles = 70
        self.tornades = list()
        self.etincelles = list()
        self.nbTornades = 3
        self.nbEtincelles = 10
        self.pasTornade = 30//self.nbTornades
        self.pasEtincelle = 50//self.nbEtincelles
        #on ajoute une tornade et une etincelle
        self.ajouterTornade()
        self.ajouterEtincelle()
        self.nbTornades -= 1
        self.nbEtincelles -= 1

    def ajouterTornade(self):
        rayon = randrange(self.rayonTornades)
        theta = randrange(24)*pi//12
        xelem = self.x + rayon*cos(theta)
        yelem = self.y - rayon*sin(theta)
        self.tornades.append(ElemAnimTornade(xelem, yelem))
        self.tornades[len(self.tornades)-1].draw()

    def ajouterEtincelle(self):
        rayon = randrange(self.rayonEtincelles)
        theta = randrange(24)*pi//12
        xelem = self.x + rayon*cos(theta)
        yelem = self.y - rayon*sin(theta)
        self.etincelles.append(ElemAnimEtincelle(xelem, yelem))
        self.etincelles[len(self.etincelles)-1].draw()

    def draw(self):
        pass

    def move(self):
        self.frameleft -= 1
        if self.frameleft%self.pasTornade == 0 and self.frameleft > 60 and len(self.tornades):
            self.ajouterTornade()
        if self.frameleft%self.pasEtincelle == 0 and self.frameleft > 40 and len(self.etincelles):
            self.ajouterEtincelle()
        for tornade in self.tornades:
            if tornade.frameleft :
                tornade.move() 
            else:
                tornade.die()
        for etincelle in self.etincelles:
            if etincelle.frameleft:
                etincelle.move()
            else:
                etincelle.die()

    def die(self):
        for tornade in self.tornades:
            tornade.die()
        for etincelle in self.etincelles:
            etincelle.die()


class ElemAnimTornade(Rect):
    '''Affiche une tornade'''
    def __init__(self,x, y):
        Rect.__init__(self, x, y, 0, 0)
        self.frameleft = 50
        self.diametreBoule = 30      #3 boules sont supperposées.
        self.ecartBouleCentre = 3 #Pour qu'on puisse voir toutes les boules et ainsi avoir l'impression de voir quelque chose tourner, les boules sont légèrement décalées par rapport au centre de l'élément d'animation
        self.couleurs = ['grey','orange','white']
        self.surfaces = list()


    def draw(self):
        for i in range(3):
            theta = (pi/6) + (2*i*pi/3)
            xballe = self.x + self.ecartBouleCentre*cos(theta) - self.diametreBoule//2
            yballe = self.y - self.ecartBouleCentre*sin(theta) - self.diametreBoule//2
            self.surfaces.append(config.CANVAS.create_oval(xballe, yballe, xballe+self.diametreBoule, yballe+self.diametreBoule, fill=self.couleurs[i], outline=self.couleurs[i]))
            

    def move(self):
        '''Toute les deux frames, on fait pivoter les boules de 2pi/3'''
        self.frameleft -= 1
        j = (self.frameleft//5)%3
        for i in range(3):
            theta = (pi/6)+((j+i)%3)*2*pi/3
            xboule = self.x + self.ecartBouleCentre*cos(theta) - self.diametreBoule//2
            yboule = self.y - self.ecartBouleCentre*sin(theta) - self.diametreBoule//2
            config.CANVAS.coords(self.surfaces[i], xboule, yboule, xboule+self.diametreBoule, yboule+self.diametreBoule)
            

    def die(self):
        for surface in self.surfaces:
            config.CANVAS.delete(surface)


class ElemAnimEtincelle(Rect):
    '''affiche une étincelle'''

    def __init__(self, x, y):
        Rect.__init__(self, x, y, 0, 0)
        self.rcarre = 5
        self.frameleft = 50
        self.surfaces = []

    def ajoutCarre(self, icarre, jcarre):
        xorigin = self.x - self.rcarre//2 - 3*self.rcarre
        yorigin = self.y - self.rcarre//2 - 3*self.rcarre
        xcarre = xorigin + icarre*self.rcarre
        ycarre = yorigin + jcarre*self.rcarre
        self.surfaces.append(config.CANVAS.create_rectangle(xcarre, ycarre, xcarre+self.rcarre, ycarre+self.rcarre, fill='red', outline='red'))


    def draw(self):
        gauche = []
        droite = []
        haut = []
        bas = []

        icarre = 0
        jcarre = 0
        for nbCouche in range(4):
            if nbCouche != 0:
                icarre += 1
                jcarre += 1
        
            for k in range(3-nbCouche):
                gauche.append((0,2*k))
                droite.append((2*(3-nbCouche),2*k+2))
                haut.append((2*k+2,0))
                bas.append((2*k,2*(3-nbCouche)))
                            
            for i in range(3-nbCouche):
                ugauche = gauche[randrange(len(gauche))]
                udroite = droite[randrange(len(droite))]
                uhaut =   haut[randrange(len(haut))]
                ubas = bas[randrange(len(bas))]
                self.ajoutCarre(icarre+ugauche[0], jcarre+ugauche[1])
                self.ajoutCarre(icarre+udroite[0], jcarre+udroite[1])
                self.ajoutCarre(icarre+uhaut[0], jcarre+uhaut[1])
                self.ajoutCarre(icarre+ubas[0], jcarre+ubas[1])
                gauche.remove(ugauche)
                droite.remove(udroite)
                haut.remove(uhaut)
                bas.remove(ubas)

            if nbCouche == 3:
                self.ajoutCarre(icarre, jcarre)


    def move(self):
        '''Toutes les 4 frames, on enlève 2 carrés'''
        self.frameleft -= 1
        if self.frameleft%4 == 0:
            if len(self.surfaces)>1:
                config.CANVAS.delete(self.surfaces[0])
                config.CANVAS.delete(self.surfaces[1])
                self.surfaces = self.surfaces[2:]
            else:
                for surface in self.surfaces:
                    config.CANVAS.delete(surface)
                self.surfaces = list()


    def die(self):
        for surface in self.surfaces:
            config.CANVAS.delete(surface)

