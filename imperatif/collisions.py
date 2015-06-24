#!/usr/bin/python3

import briques, balles, barres, bonus, animationsArtifice, animationsExplosion, config

flags = []


# Fonctions implémentées :

# typeCollision(1x1, 1x2, 1y1, 1y2, 2x1, 2x2, 2y1, 2y2)
# collision(1x1, 1x2, 1y1, 1y2, 2x1, 2x2, 2y1, 2y2)
# gestionCollisionBalleBarre(i, j)
# gestionCollisionBalleBrique(i, j)
# gestionCollisionBonusBarre(i, j) 
# gestionCollisionBallesBarres()
# gestionCollisionBallesBriques()
# gestionCollisionBallesMurs()
# gestionCollisionBonusBarres() 
# gestionCollisions()           

def typeCollision(ax1, ax2, ay1, ay2, bx1, bx2, by1, by2):
    '''Fonction renvoyant le type de collision.'''
    if ay1 < by2 and ay2 > by1:
        return "BORD_VERTICAL"
    elif ax1 < bx2 and ax2 > bx1:
        return "BORD_HORIZONTAL"
    else: #  cas limite
        # print("TYPE COLLISION NON GERE")
        return



def collision(ax1, ax2, ay1, ay2, bx1, bx2, by1, by2):
    '''Fonction renvoyant vrai si il y a collision, faux sinon.'''

    touche = False
    
    if ax1<bx2 and ax2>bx1 \
       and ay1<by2 and ay2>by1:
            touche = True
    return touche

    

def gestionCollisionBalleBarre(i, j):
    '''Fonction calculant la collision entre la ieme balle et la jeme barre.
       Les changements à faire sont mis sous forme de dictionnaire dans la liste flags du package courant.
    '''
    global typeCollision, collision
    #on calcule les coordonnées futures de la balle et de la barre qu'elles auront la frame suivante.

    ballew = balles.w[i]
    balleh = balles.h[i]

    ballex01 = balles.x[i]
    ballex02 = ballex01+ballew
    balley01 = balles.y[i]
    balley02 = balley01+balleh

    balleDx = balles.dx[i]
    balleDy = balles.dy[i]

    ballex1 = ballex01+balleDx
    ballex2 = ballex02+balleDx
    balley1 = balley01+balleDy
    balley2 = balley02+balleDy




    barrew = barres.w[j]
    barreh = barres.h[j]

    barrex01 = barres.x[j]
    barrex02 = barrex01+barrew
    barrey01 = barres.y[j]
    barrey02 = barrey01+barreh

    barreDx = barres.dx[j]

    barrex1 = barrex01+barreDx
    barrex2 = barrex02+barreDx
    barrey1 = barrey01
    barrey2 = barrey02

    if collision(ballex1, ballex2, balley1, balley2, barrex1, barrex2, barrey1, barrey2):

        type = typeCollision(ballex01, ballex02, balley01, balley02, barrex01, barrex02, barrey01, barrey02)
        if type == "BORD_VERTICAL":
            balles.dx[i] = -balleDx + barreDx
            if abs(barreDx-balleDx) < abs(barreDx):
                balles.dx[i] = barreDx
        
        elif type == "BORD_HORIZONTAL":
            ''' from geogebra :
                5.5x/t
                6x*x / t^2 - 3
                pour vitesse constante (supposition d'incidence verticale)
            '''

            pos = ballex01 - barrex01 - barrew/2
            # *0.75 (et non pas 1) pour éviter que la balle parte trop vite sur les côtés
            # -> on modère son dx
            balles.dx[i] = config.SPEED * (balleDx*0.25 + 5.5*pos/barrew)
            balles.dy[i] = config.SPEED * ((6*pos*pos)/(barrew * barrew) - 3)

            # limiteur de vitesse (sinon illisible)
            if (balles.dx[i] > 10):
                balles.dx[i] = 10
            elif balles.dx[i] < -10:
                balles.dx[i] = -10




def gestionCollisionBalleBrique(i, j):
    '''Fonction calculant la collision entre la ieme balle et la jeme brique.
       Les changements à faire sont mis sous forme de dictionnaire dans la liste flags du package courant.
    '''
    global collision, typeCollision
    #on calcule les coordonnées futures de la balle et de la brique qu'elles auront la frame suivante.

    flags = []

    ballew = balles.w[i]
    balleh = balles.h[i]

    ballex01 = balles.x[i]
    ballex02 = ballex01+ballew
    balley01 = balles.y[i]
    balley02 = balley01+balleh

    balleDx = balles.dx[i]
    balleDy = balles.dy[i]

    ballex1 = ballex01+balleDx
    ballex2 = ballex02+balleDx
    balley1 = balley01+balleDy
    balley2 = balley02+balleDy

    brique = briques.briques[j]

    briquex1 = brique[0]
    briquex2 = briquex1+brique[2]
    briquey1 = brique[1]
    briquey2 = briquey1+brique[3]

    if collision(ballex1, ballex2, balley1, balley2, briquex1, briquex2, briquey1, briquey2):

        type = typeCollision(ballex01, ballex02, balley01, balley02, briquex1, briquex2, briquey1, briquey2)
        briqueType = briques.type[j]
        briqueBonus = briques.bonus_contenu[j]
        balleBonus = balles.bonus[i]

        if briqueType == "indestructible":
            if type == "BORD_VERTICAL":
                flags.append({'event':"balle.invert_dx"})
            elif type == "BORD_HORIZONTAL":
                flags.append({'event':"balle.invert_dy"})
            else: #cas limite
                # print("TODO : Cas limite collision brique.")
                flags.append({'event':"balle.invert_dy"})
        else:
            if balleBonus != "balle_feu":
                if type == "BORD_VERTICAL":
                    flags.append({'event':"balle.invert_dx"})
                elif type == "BORD_HORIZONTAL":
                    flags.append({'event':"balle.invert_dy"})
                else: #cas limite
                    print("TODO : Cas limite collision brique.")
                    flags.append({'event':"balle.invert_dy"})                
            
            briques.vies[j] -= 1
            if briques.vies[j] >= 1:
                briques.draw(j)
            else:
                if briqueType == "explosive":
                    flags.append({'event':"explosion.create", 'x': brique[0]+brique[2]//2, 'y': brique[1]+brique[3]//2})
                    flags.append({'event':"brique.enlever"})
                else :
                    flags.append({'event':"animationArtifice.create", 'x': brique[0]+brique[2]//2, 'y': brique[1]+brique[3]//2})
                    flags.append({'event':"brique.enlever"})

                    if briqueType =="" and briqueBonus!="":
                        flags.append({'event':"bonus.create", 'x': brique[0]+brique[2]//2, 'y': brique[1]+brique[3]//2, 'bonus':briqueBonus})

    return flags



def gestionCollisonBonusBarre(i, j):
    '''Si il y a collision, on active le bonus'''
    global collision

    retour = False

    bonusx1 = bonus.x[i]+bonus.dx[i]
    bonusx2 = bonusx1+bonus.w[i]
    bonusy1 = bonus.y[i]+bonus.dy[i]
    bonusy2 = bonusy1+bonus.h[i]

    barrex1 = barres.x[j]+barres.dx[j]
    barrex2 = barrex1+barres.w[j]
    barrey1 = barres.y[j]
    barrey2 = barrey1+barres.h[j]


    if collision(bonusx1, bonusx2, bonusy1, bonusy2, barrex1, barrex2, barrey1, barrey2):
        
        retour = True

        #l'effet obtenu depend du bonus
        if bonus.bonus_contenu[i] in ["barre_agrandie","barre_retrecie"]:
            barres.applyBonus(j, bonus.bonus_contenu[i])
            bonus.enleverBonus(i)
        elif bonus.bonus_contenu[i] == "balle_feu":
            for k in range(balles.nbBalle()):
                balles.applyBonus(k, "balle_feu")
            bonus.enleverBonus(i)
        elif bonus.bonus_contenu[i] == "ajout_balle":
            xBalle = barres.x[j]+barres.w[j]//2-balles.RAYON_BALLE
            yBalle = barres.y[j]+-balles.RAYON_BALLE 
            dxBalle = 0
            dyBalle = -config.SPEED
            balles.ajouterBalle(xBalle, yBalle, dxBalle, dyBalle)
            bonus.enleverBonus(i)
        elif bonus.bonus_contenu[i] == "":
            bonus.enleverBonus(i)
        else:
            raise ValueError("Erreur : bonus contenant un type d bonus inconnu : "+bonus.bonus_contenu[i])

    return retour


def gestionCollisionBallesBarres():
    global gestionCollisionBalleBarre

    for i in range(barres.nbBarre()):
        k = 0
        for j in range(balles.nbBalle()):
            if balles.y[k] > config.HEIGHT:
                balles.enleverBalle(k)
            else:
                gestionCollisionBalleBarre(k, i)
                k += 1



def gestionCollisionBonusBarres():
    global gestionCollisonBonusBarre

    for i in range(barres.nbBarre()):
        k = 0
        for j in range(bonus.nbBonus()):
            enleverBonus = gestionCollisonBonusBarre(k,i)
            if not enleverBonus:
                k += 1

    k = 0
    for i in range(bonus.nbBonus()):
        if bonus.y[k] > config.HEIGHT:
            bonus.enleverBonus(k)
        else:
            k += 1


def gestionCollisionBallesBriques():
    global gestionCollisionBalleBrique

    flagsretour = []

    for i in range(balles.nbBalle()):
        flags = []
        k = 0
        for j in range(briques.nbBrique()):
            flags += gestionCollisionBalleBrique(i, k)
            if {'event':"brique.enlever"} in flags:
                briques.enleverBrique(k)
                flags.remove({'event':"brique.enlever"})
            else:
                k += 1

        #gestion des flags
        # flags possibles : "balle.invert_dx", "balle.invert_dy", "explosion.create", "animationArtifice.create", "bonus.create"
        flags_processed = list()
        for flag in flags:
            if flag['event'] == "balle.invert_dx" and flag not in flags_processed:
                balles.dx[i] = -balles.dx[i]
                flags_processed.append(flag)
            elif flag['event'] == "balle.invert_dy" and flag not in flags_processed:
                balles.dy[i] = -balles.dy[i]
                flags_processed.append(flag)
            elif flag['event'] == "animationArtifice.create" and flag not in flags_processed:
                animationsArtifice.ajouterAnimationArtifice(flag['x'], flag['y'])
                flags_processed.append(flag)
            elif flag['event'] == "bonus.create" and flag not in flags_processed:
                bonus.ajouterBonus(flag['x'], flag['y'], flag['bonus'])
                flags_processed.append(flag)
            elif flag['event'] == "explosion.create" and flag not in flags_processed:
                animationsExplosion.ajouterExplosion(flag['x'], flag['y'])
                briques.explosion(flag['x'], flag['y'])
                flags_processed.append(flag)

        #suppression des flags
        for flag in flags_processed :
            while (flag in flags):
                flags.remove(flag)

        #sauvegarde des flags non traités
        flagsretour += flags

    return flagsretour



def gestionCollisionBallesMurs():
    '''Applique les collisions entre les balles et les murs'''
    global collision

    for i in range(balles.nbBalle()):
        balleDy = balles.dy[i]
        balleDx = balles.dx[i]
        ballex1 = balles.x[i]+balleDx
        ballex2 = ballex1+balles.w[i]
        balley1 = balles.y[i]+balleDy
        balley2 = balley1+balles.h[i]

        #si la balle entre en collision avec le mur gauche ou le mur droit alors on inverse dx.
        if collision(ballex1, ballex2, balley1, balley2, 0, 0, 0, config.HEIGHT) or collision(ballex1, ballex2, balley1, balley2, config.WIDTH, config.WIDTH, 0, config.HEIGHT):
            balles.dx[i] = -balleDx
            
        #si la balle entre en collision avec le mur haut alors on inverse dy.
        if collision(ballex1, ballex2, balley1, balley2, 0, config.WIDTH, 0, 0):
            balles.dy[i] = -balleDy




def gestionCollisions():
    '''Fonction testant les collisions entre les balles et les barres, les briques et les murs'''
    global gestionCollisionBallesBarres, gestionCollisionBallesBriques, gestionCollisionBallesMurs, gestionCollisionBonusBarres

    gestionCollisionBallesBarres()
    gestionCollisionBallesMurs()
    flags = gestionCollisionBallesBriques()
    gestionCollisionBonusBarres()

    if len(flags):
        raise ValueError("Flags non traités : "+flags)
