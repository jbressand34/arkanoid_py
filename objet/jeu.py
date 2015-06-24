#!/usr/bin/python3

from tkinter import *
from math import sqrt
from random import *
from pickle import *
from element_jeu import *
from collision import *
from animations import *
import procgen
import config

TESTING = False

def readFile(NomFichier):
    ''' Ouvre un fichier de niveau et renvoie une liste de briques '''
    file = open('levels/'+NomFichier+'.lvl','rb')
    briques = load(file)
    file.close()
    return briques

def writeFile(briques,nomlvl):
    for brique in briques:
        brique.surface = None
    file = open('levels/'+nomlvl+'.lvl','wb')
    dump(briques,file)
    file.close()

class Jeu(object):
    def __init__(self, mode="auto", seed=str(randint(0, 999999999999))):
        self.mode = mode
        self.etape = None
        self.bandeau = {}
        config.SCORE = 0
        config.SPEED = config.BALLE_SPEED_INIT
        self.vies = 3

        self.seed = seed
        self.difficulty = 20  # 20%

        # On active les touches directionnelles si le jeu n'est pas en mode automatique
        if self.mode != "auto":
            config.CANVAS.bind('<B1-Motion>', self.B1_key)
            config.CANVAS.bind('<ButtonRelease-1>', self.B1_release)
            config.CANVAS.bind('<Right>', self.right_key)
            config.CANVAS.bind('<Left>', self.left_key)
            config.CANVAS.bind('<KeyRelease-Right>', self.right_key_release)
            config.CANVAS.bind('<KeyRelease-Left>', self.left_key_release)
            if self.mode == "campagne" or self.mode == "arcade":
                self.initBandeau()
                if self.mode == "campagne":
                    self.seed = 0
            elif self.mode == "coop":
                self.vies = 1
                config.CANVAS.bind('<Q>', self.Q_key)
                config.CANVAS.bind('<D>', self.D_key)
                config.CANVAS.bind('<q>', self.Q_key)
                config.CANVAS.bind('<d>', self.D_key)
                config.CANVAS.bind('<KeyRelease-Q>', self.Q_key_release)
                config.CANVAS.bind('<KeyRelease-D>', self.D_key_release)
                config.CANVAS.bind('<KeyRelease-q>', self.Q_key_release)
                config.CANVAS.bind('<KeyRelease-d>', self.D_key_release)
        config.CANVAS.focus_set()

        # Creation mur
        self.murs = list()
        self.murs.append(Mur(-200, 0, 200, config.HEIGHT))
        self.murs.append(Mur(0, -200, config.WIDTH, 200))
        self.murs.append(Mur(config.WIDTH+1, 0, 200, config.HEIGHT))

        # Creation Bonus
        self.bonus = list()

        # Creation balles
        self.balles = list()

        # Creation barres
        self.barres = list()
        if (self.mode == "auto"):
            self.barres.append(Barre(config.WIDTH/2-50, 550))
        elif (self.mode == "arcade" or self.mode == "campagne"):
            self.barres.append(Barre(config.WIDTH/2-50, 500))
        elif (self.mode == "coop"):
            self.barres.append(Barre(3*config.WIDTH/4-50, 550))
            self.barres.append(Barre(config.WIDTH/4-50, 500))
        else:
            print("MODE DE JEU INCONNU :", self.mode)

        # Creation Animations
        self.animations = list()

        # Creation briques
        self.briques = list()
        self.changerNiveau()

    def changerNiveau(self):
        '''Fonction gérant le passage à un nouveau niveau'''

        tmp = 0
        for balle in self.balles:
            balle.x = self.barres[tmp%(1+int(self.mode=="coop"))].x+\
                      self.barres[tmp%(1+int(self.mode=="coop"))].w//2-10 + randrange(-5, 5)
            balle.y = self.barres[tmp%(1+int(self.mode=="coop"))].y-200
            balle.dx = randrange(-5, 5)/10
            balle.dy = randrange(2, 4)
            config.CANVAS.coords(balle.surface, balle.x, balle.y, balle.x+balle.w, balle.y+balle.h)
            tmp += 1
        del tmp

        if (config.SCORE == 0):
            self.balles.append(Balle(self.barres[0].x+self.barres[0].w//2-10 + randrange(-5, 5), 350))
            if (self.mode == "coop"):
                self.balles.append(Balle(self.barres[1].x+self.barres[1].w/2-10 + randrange(-5, 5), 400))
        # Suppression bonus
        for b in self.bonus:
            self.bonus.remove(b)
        self.bonus = []

        # Suppression animations
        for animation in self.animations:
            animation.die()
        self.animations = list()

        # Suppression puis création briques
        if (self.mode == 'arcade' or self.mode == 'coop' or self.mode == 'auto'):
            if config.SCORE != 0:  # si ce n'est pas le premier niveau
                self.seed = str(int(self.seed, 36) + 1)
                self.difficulty = max(self.difficulty, self.difficulty+10)
            self.briques = procgen.procgen(self.seed, self.difficulty)
        elif (self.mode == 'campagne'):
            if (self.seed < 9):
                self.briques = readFile(str(self.seed))
                for brique in self.briques:
                    brique.draw()
                self.seed += 1
            else:
                print("Campagne terminée !!! TODO : A gérer score et fin")

        # affichage Bandeau
        config.CANVAS.tag_raise("bandeau")

    def mort(self):
        '''Fonction étant appelée lorsque le joueur a laissé passer toutes
           les balles.
           Si le joueur n'a plus de vie alors cette fonction appelle
           la fonction self.gameOver'''
        self.vies -= 1
        if (self.bandeau != {}):
                config.CANVAS.delete(self.bandeau['vie'][self.vies])
        # Si il reste une vie au joueur
        if self.vies >= 1:
            for balle in self.balles:
                self.balles.remove(balle)

            if (self.mode == "coop"):
                self.barres[0].x = 3*config.WIDTH/4-self.barres[0].w/2
                self.barres[1].x = config.WIDTH/4-self.barres[1].w/2
                config.CANVAS.coords(self.barres[1].surface, self.barres[1].x, self.barres[1].y,
                                     self.barres[1].x+self.barres[1].w,
                                     self.barres[1].y+self.barres[1].h)
                self.balles.append(Balle(self.barres[1].x+self.barres[1].w/2 - 10+randrange(-5, 5), 400))
            else:
                self.barres[0].x = config.WIDTH/2-self.barres[0].w/2
            self.balles.append(Balle(self.barres[0].x+self.barres[0].w/2 - 10+randrange(-5, 5), 350))

            config.CANVAS.coords(self.barres[0].surface, self.barres[0].x, self.barres[0].y,
                                 self.barres[0].x+self.barres[0].w, self.barres[0].y+self.barres[0].h)
            config.CANVAS.tag_raise("bandeau")
        else: # partie finie
            for barre in self.barres:
                barre.dx = 0
            config.CANVAS.unbind('<Button-1>')
            config.CANVAS.unbind('<ButtonRelease-1>')
            config.CANVAS.unbind('<Right>')
            config.CANVAS.unbind('<Left>')
            config.CANVAS.unbind('<Q>')
            config.CANVAS.unbind('<D>')
            config.CANVAS.unbind('<q>')
            config.CANVAS.unbind('<d>')
            config.CANVAS.unbind('<KeyRelease-Right>')
            config.CANVAS.unbind('<KeyRelease-Left>')
            config.CANVAS.unbind('<KeyRelease-Q>')
            config.CANVAS.unbind('<KeyRelease-D>')
            config.CANVAS.unbind('<KeyRelease-q>')
            config.CANVAS.unbind('<KeyRelease-d>')

    def updateBandeau(self):
        if self.bandeau != {}:
            config.CANVAS.itemconfig(self.bandeau['score'], text=str(config.SCORE))
            config.CANVAS.itemconfig(self.bandeau['highscore'], text="1000")

    def initBandeau(self):
        '''Fonction gérant l'affichage du bandeau en bas de l'écran.
           Le bandeau affiche : le score, le highscore et les vies.
        '''
        self.bandeau = {}
        self.bandeau['aux'] = list()
        self.bandeau['vie'] = list()

        #On affiche le rectangle d'arriere plan
        self.bandeau['aux'].append(
            config.CANVAS.create_rectangle(0, config.HEIGHT-50, config.WIDTH,
                                           config.HEIGHT, outline='grey15',
                                           width=1, fill='grey5', tag="bandeau"))
        self.bandeau['aux'].append(
            config.CANVAS.create_text(10, config.HEIGHT-22, anchor=W,
                                      font=("Droidsan", 20), text="Score:",
                                      fill="grey80", tag="bandeau"))
        self.bandeau['score'] =\
            config.CANVAS.create_text(100, config.HEIGHT-22, anchor=W,
                                      font=("Droidsan", 20), text=str(config.SCORE),
                                      fill="grey80", tag="bandeau")
        self.bandeau['aux'].append(
            config.CANVAS.create_text(400, config.HEIGHT-22, anchor=W,
                                      font=("Droidsan", 20), text="Highscore:",
                                      fill="grey80", tag="bandeau"))
        self.bandeau['highscore'] = \
            config.CANVAS.create_text(550, config.HEIGHT-22, anchor=W, font=("Droidsan", 20),
                                      text="1000", fill="grey80", tag="bandeau")
        #On affiche les vies.
        y = config.HEIGHT-14
        x = config.WIDTH-60
        for i in range(self.vies):
            self.bandeau['vie'].append(
                config.CANVAS.create_rectangle(x, y, x+40, y+10, outline='grey60',
                                               width=1, fill='grey45', tag="bandeau"))
            y -= 15

    def hasBalle(self):
        '''Fonction renvoyant True si il reste au moins une balle en jeu,
           False sinon. Cette fonction supprime les balles qui sont sortis du jeu.'''
        nbBalle = 0
        ballesAsupprimer = []
        for balle in self.balles:
            if balle.y < self.barres[0].y+10:
                nbBalle += 1
            elif balle.y > config.HEIGHT:
                ballesAsupprimer.append(balle)

        for balle in ballesAsupprimer:
            self.balles.remove(balle)

        if (self.mode == "coop"):
            return nbBalle >=2
        else:
            return nbBalle >=1

    def hasBreakableBrick(self):
        '''Fonction renvoyant True si il reste au moins une brique destructible
           en jeu. False sinon.'''
        hasBreakableBrick = False
        for brique in self.briques:
            if brique.bonus != "indestructible":
                hasBreakableBrick = True
        return hasBreakableBrick

    def explosion(self, x, y):
        '''Enleve trois vies a chaque brique dans un rayon autour du centre de l'explosion.'''
        rayonExplosion = 100
        briquesNormalesAenlever = []
        briquesExplosivesAenlever = []
        for brique in self.briques:
            #Si un des coins de la brique est dans le rayon de l'explosion
            #alors la brique est touché.
            r1 = sqrt((x-brique.x)**2+(y-brique.y)**2) #distance du centre de l'explosion par rapport
                                                       #au coin supérieure gauche de la brique.
            r2 = sqrt((x-brique.x-brique.w)**2+(y-brique.y)**2) #coin supérieur droit.
            r3 = sqrt((x-brique.x)**2+(y-brique.y-brique.h)**2) #coin inférieur gauche.
            r4 = sqrt((x-brique.x-brique.w)**2+(y-brique.y-brique.h)**2) #coin inferieur droit

            if r1<rayonExplosion or r2<rayonExplosion or r3<rayonExplosion or r4<rayonExplosion :
                if brique.bonus != "indestructible":
                    brique.pv -= 3
                    if brique.pv <= 0:
                        if brique.bonus == "explosive":
                            briquesExplosivesAenlever.append(brique)
                        else:
                            briquesNormalesAenlever.append(brique)
                    else:
                        brique.draw()

        #On enleve chaque brique de la liste briquesNormalesAenlever
        for brique in briquesNormalesAenlever:
            self.animations.append(AnimationFeuArtifice(x, y))
            self.briques.remove(brique)

        #Avant de gérer les explosions de chaque brique explosive, on les enlève
        #de self.briques mais on les garde dans la liste locale briquesExplosivesAenlever.
        #Pourquoi ne pas les supprimer et gérer leurs explosions dans la meme boucle ?
        #La fonction self.explosion(x, y) parcourt self.briques et inflige un dégat
        #à celles se trouvant dans le rayon de l'explosion.
        #Les briques explosives se trouvant dans le rayon de l'explosion explosent à leur tour.
        #Pour eviter de faire exploser plusieurs fois les meme briques explosives (ce qui renverrait
        #une ValueError car faire exploser une brique detruite, c'est acceder a un élément de
        #self.briques qui a été enlevé), on enleve d'abord les briques explosives de la liste
        #self.briques (tout en en gardant une référence dans briquesExplosivesAenlever),
        #puis une fois qu'elles ont toutes été enlevées, on les fait exploser.

        #On enleve de self.briques les briques explosives (tout en les gardant en mémoire
        #dans briquesExplosivesAenlever)
        for brique in briquesExplosivesAenlever:
            self.briques.remove(brique)
            self.animations.append(AnimationExplosion(brique.x, brique.y))

        #On peut maintenant les faire exploser.
        for brique in briquesExplosivesAenlever:
            self.explosion(brique.x, brique.y)

    def update(self):
        def deplacementBarreAuto():
            '''Fonction plaçant la barre en dessous de la balle'''
            # Si la balle est en mouv horizontale
            if (self.balles[0].dx != 0):
                self.barres[0].dx = self.balles[0].x+(self.balles[0].w//2) - (self.barres[0].x + (self.barres[0].w//2))
            #Sinon (décalage < 10).
            if (self.barres[0].x + self.barres[0].dx) < 0 or \
               (self.barres[0].x + self.barres[0].dx + self.barres[0].w) > config.WIDTH:
                #On remet à 0 le déplacement de la barre.
                self.barres[0].dx = 0

        flags = list()
        for balle in self.balles:
            flags += GestionCollision(balle, self.briques)
            flags += GestionCollision(balle, self.murs)
            flags += GestionCollision(balle, self.barres)
        for barre in self.barres:
            flags += GestionCollision(barre, self.murs)
            flags += GestionCollision(barre, self.bonus)

        for flag in flags:
            if flag['event'] == "animationArtifice.create":
                self.animations.append(AnimationFeuArtifice(flag['x'], flag['y']))
                self.updateBandeau()
            elif flag['event'] == "explosion.create":
                self.animations.append(AnimationExplosion(flag['x'], flag['y']))
                self.explosion(flag['x'], flag['y'])
                self.updateBandeau()
            elif flag['event'] == "bonus.create":
                self.bonus.append(Bonus(flag['x'], flag['y'], flag['bonus']))
                config.CANVAS.tag_raise("bandeau")
            elif flag['event'] == "bonus.ajout_balle":
                self.balles.append(Balle(flag['x']+randrange(-5, 5), flag['y']-15, 0, -3*config.SPEED))
                config.CANVAS.tag_raise("bandeau")
            elif flag['event'] == "bonus.balle_feu":
                for balle in self.balles:
                    balle.applybonus('balle_feu')
            elif TESTING:
                print("flag non traité :", flag)

        #Si le jeu est en mode automatique alors on déplace automatiquement la barre.
        if self.mode == "auto":
            deplacementBarreAuto()

        #Si toutes le balles sont sorties de l'écran alors le joueur perd une vie.
        if not self.hasBalle() and self.vies>0:
            self.mort()

        #Si toutes les briques destructibles ont été détruite alors on change de niveau.
        elif not self.hasBreakableBrick():
            self.changerNiveau()

        for balle in self.balles:
            balle.move()
            balle.gestionbonus()
        for barre in self.barres:
            barre.move()
            barre.gestionbonus()
        for bonus in self.bonus:
            bonus.move()
        for animation in self.animations:
            if animation.frameleft:
                animation.move()
            else:
                animation.die()
                self.animations.remove(animation)

        config.SPEED += config.SPEED_PER_FRAME

        if (TESTING):
            config.CANVAS.after(1000//config.FPS, self.update)

    ##############################
    # ### EVENTS

    def B1_key(self, event):
        centre_x = self.barres[0].x+self.barres[0].w/2
        self.barres[0].dx = max(-config.BARRE_SPEED,
                                min(config.BARRE_SPEED,
                                    (event.x-centre_x)/20))

    def B1_release(self, event):
        self.barres[0].dx = 0

    def right_key(self, event):
        self.barres[0].dx = config.BARRE_SPEED

    def right_key_release(self, event):
        if (self.barres[0].dx > 0):
            self.barres[0].dx = 0

    def left_key(self, event):
        self.barres[0].dx = -config.BARRE_SPEED

    def left_key_release(self, event):
        if (self.barres[0].dx < 0):
            self.barres[0].dx = 0

    def D_key(self, event):
        self.barres[1].dx = config.BARRE_SPEED

    def D_key_release(self, event):
        if (self.barres[1].dx > 0):
            self.barres[1].dx = 0

    def Q_key(self, event):
        self.barres[1].dx = -config.BARRE_SPEED

    def Q_key_release(self, event):
        if (self.barres[1].dx < 0):
            self.barres[1].dx = 0

if __name__ == "__main__":
    TESTING = True
    root = Tk()
    root.title("Arkanoid")
    root.minsize(width=800+5, height=600+5)
    config.CANVAS = Canvas(root, width=800, height=600, bg="grey10")
    config.CANVAS.pack()
    jeu = Jeu("arcade")
    jeu.update()
    config.CANVAS.mainloop()
