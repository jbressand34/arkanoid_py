#!/usr/bin/python3

from element_jeu import *
from tkinter import *
from math import *
import config

'''
NOTE : Traitement flags après chaque appel de GestionCollision, sinon risque de liste dans listes.
'''

'''
TODO :
Renvoyer Dictionnaire au lieu de listes, afin de pouvoir gérer des coordonnées en externe,
                                         ou des classes (ex à actualiser)
Gestion Barre/Bonus
Gestion explosive
'''

TESTING = False


def CollisionSegSeg(A_x, A_y, B_x, B_y, O_x, O_y, P_x, P_y):
    def CollisionDroiteSeg(A_x, A_y, B_x, B_y, O_x, O_y, P_x, P_y):
        AB_x = B_x - A_x
        AB_y = B_y - A_y
        AP_x = P_x - A_x
        AP_y = P_y - A_y
        AO_x = O_x - A_x
        AO_y = O_y - A_y
        if ((AB_x*AP_y - AB_y*AP_x)*(AB_x*AO_y - AB_y*AO_x) < 0):
            return True
        else:
            return False

    if (CollisionDroiteSeg(A_x, A_y, B_x, B_y, O_x, O_y, P_x, P_y) == False):
        return False  # inutile d'aller plus loin si le segment [OP] ne touche pas la droite (AB)
    if (CollisionDroiteSeg(A_x, A_y, B_x, B_y, O_x, O_y, P_x, P_y) == False):
        return False
    return True

def Angle(A_x, A_y, B_x, B_y):
    def ProdScal(A_x, A_y, B_x, B_y):
        return A_x * B_x + A_y * B_y

    def Norme(A_x, A_y):
        return sqrt((A_x)**2 + (A_y)**2)

    b = Norme(A_x, A_y) * Norme(B_x, B_y)
    Angle = acos(
                ProdScal(A_x, A_y, B_x, B_y) /
                b)
    return Angle


def GestionCollision(r1, lr2):
    # r1 = entité destructice
    def Collision(r1, r2):
        # n_1_* déjà calculés
        # définition des positions prévues à la prochaine frame.
        # si chevauchement des surfaces, true. Sinon, false.
        n_2_x = r2.x + r2.dx
        n_2_y = r2.y + r2.dy
        n_2_x2 = n_2_x + r2.w
        n_2_y2 = n_2_y + r2.h

        # Ligne si dessous obtenue par application de De Morgan
        # sur conditions de non chevauchement des Rect

        return n_1_x <= n_2_x2 and n_2_x <= n_1_x2 and n_1_y <= n_2_y2 and n_2_y <= n_1_y2

    def TypeCollision(r1, r2):
        if (r1.bonus == "balle_feu" and r2.__class__.__name__ == "Brique" and r2.bonus != "indestructible"):
            return "TRANSPERCE"
        elif (r1.y < r2_y2 and r1_y2 > r2.y):
            return "BORD_VERTICAL"
        elif (r1.x < r2_x2 and r1_x2 > r2.x):
            return "BORD_HORIZONTAL"
        else:
            if (TESTING):
                print("TYPE COLLISION NON GÉRÉ")
            return

    def del_all_instances(flag):
        for elem in flags:
            if flag == elem['event']:
                flags.remove(elem)

    flags = list()

    r1_x2 = r1.w+r1.x
    r1_y2 = r1.h+r1.y

    n_1_x = r1.x + r1.dx
    n_1_y = r1.y + r1.dy
    n_1_x2 = n_1_x + r1.w
    n_1_y2 = n_1_y + r1.h

    for r2 in lr2:
        r2_x2 = r2.x+r2.w
        r2_y2 = r2.y+r2.h

        # coins de la balle entrant en collision
        if (Collision(r1, r2)):
            Type = ""
            if r1.__class__.__name__ == "Balle":
                # Balle/Barre
                if r2.__class__.__name__ == "Barre":
                    Type = TypeCollision(r1, r2)
                    if Type == "BORD_VERTICAL":
                            if (abs(-r1.dx + r2.dx) < abs(r2.dx)):
                                r1.dx = r2.dx
                            else:
                                if r2.dx == 0:
                                    r1.dx = -r1.dx
                                if (r2.dx > 0):
                                    r1.dx = min(r2.dx, -r1.dx + r2.dx)
                                elif (r2.dx < 0):
                                    r1.dx = max(r2.dx, -r1.dx + r2.dx)
                    elif Type == "BORD_HORIZONTAL":
                        ''' from geogebra :
                        5.5x/t
                        6x*x / t^2 - 3
                        pour vitesse constante (supposition d'incidence verticale)
                        '''
                        pos = r1.x + r1.w/2 - (r2.x + r2.w/2)

                        # *0.75 (et non pas 1) pour simulation de frottement
                        r1.dx = (r1.dx*0.75 + 5.5*pos/r2.w)
                        r1.dy = ((6*pos*pos)/(r2.w * r2.w) - 3)

                        # passage à angle
                        sign = 1 if (r1.dx > 0) else -1
                        ang = Angle(1, 0, r1.dx, r1.dy) * sign
                        norme = 3*config.SPEED

                        # repassage en cartésien (méthode permettant de garder vitesse constante)
                        r1.dx = norme * cos(ang)
                        r1.dy = -abs(norme * sin(ang))

                # Balle/Mur, Balle/Brique
                elif (r2.__class__.__name__ == "Mur" or
                      r2.__class__.__name__ == "Brique"):
                    # Forcement sur bords verticaux
                    Type = TypeCollision(r1, r2)
                    if Type == "BORD_VERTICAL":
                        flags.append({'event': "r1.invert_dx"})
                    elif Type == "BORD_HORIZONTAL":
                        flags.append({'event': "r1.invert_dy"})
                    elif Type == "TRANSPERCE":
                        pass
                    else:  # Cas limite
                        if (CollisionSegSeg(r2.x, r2.y, r2.x+r2.w, r2.y, r1.x,
                                            r1.y, r1.x+r1.dx, r1.y+r1.dy)
                            or CollisionSegSeg(r2.x, r2.y+r2.h, r2.x+r2.w, r2.y+r2.h,
                                               r1.x, r1.y, r1.x+r1.dx, r1.y+r1.dy)):
                            flags.append({'event': "r1.invert_dy"})
                        else:
                            flags.append({'event': "r1.invert_dx"})
                    if (r2.__class__.__name__ == "Brique" and r2.bonus != "indestructible"):
                        r2.pv -= 1
                        if (r2.pv >= 1):
                            r2.draw()
                        else:
                            lr2.remove(r2)
                            if r2.bonus == "explosive":
                                flags.append({'event': "explosion.create", 'x': r2.x+r2.w/2,
                                              'y': r2.y+r2.h/2})
                            else:
                                flags.append({'event': "animationArtifice.create", 'x': r2.x+r2.w/2,
                                              'y': r2.y+r2.h/2})
                            if (r2.bonus_contenu):
                                flags.append({'event': "bonus.create", 'x': r2.x+r2.w/2,
                                              'y': r2.y+r2.h/2, 'bonus': r2.bonus_contenu})

            # Barre/Bonus
            elif (r1.__class__.__name__ == "Barre"):
                if (r2.__class__.__name__ == "Bonus"):
                    if (r2.bonus_contenu == "balle_feu"):
                        flags.append({'event': "bonus.balle_feu"})
                    elif (r2.bonus_contenu == "ajout_balle"):
                        flags.append({'event': "bonus.ajout_balle",
                                      'x': r1.x+r1.w/2 - r2.w/2,
                                      'y': r1.y})
                    elif (r2.bonus_contenu == "barre_agrandie"):
                        r1.applybonus(r2.bonus_contenu)
                    elif (r2.bonus_contenu == "barre_retrecie"):
                        r1.applybonus(r2.bonus_contenu)
                    lr2.remove(r2)

                if (r2.__class__.__name__ == "Mur"):
                    r1.dx = 0

            else:
                print("Collision avec élément non géré :", r2.__class__.__name__)

            if (TESTING):
                print("collision ", r1.__class__.__name__, "/", r2.__class__.__name__, "\t type:", Type)
    # fin parcours lr2

    flags_processed = list()
    for flag in flags:
        if flag['event'] == "r1.invert_dx" and flag not in flags_processed:
            r1.dx = -r1.dx
            flags_processed.append(flag)
        if flag['event'] == "r1.invert_dy" and flag not in flags_processed:
            r1.dy = -r1.dy
            flags_processed.append(flag)

    # Supression
    for flag in flags_processed:
        while (flag in flags):
            flags.remove(flag)

    return flags  # renvoi des flags non traités en interne

# test unitaire
# Cliquer pour déplacer la balle. Résultats printés
if __name__ == '__main__':

    def right_key(event):
        barres[0].dx = 5

    def right_key_release(event):
        if (barres[0].dx > 0):
                barres[0].dx = 0

    def left_key(event):
        barres[0].dx = -5

    def left_key_release(event):
        if (barres[0].dx < 0):
            barres[0].dx = 0

    def deplacement_balle(event):
        centre_x = balles[0].x+balles[0].w/2
        centre_y = balles[0].y+balles[0].h/2
        balles[0].dx = (event.x-centre_x)/10
        balles[0].dy = (event.y-centre_y)/10

    def update():
        flags = GestionCollision(balles[0], briques)
        flags += GestionCollision(balles[0], murs)
        flags += (GestionCollision(balles[0], barres))
        flags += (GestionCollision(barres[0], murs))

        balles[0].move()
        barres[0].move()
        for b in bonus:
            b.move()
        if (flags):
            print(" flags non traités en interne:", flags)

        root.after(1000//fps, update)
    # global TESTING
    TESTING = True

    # besoin encapsuler toute merde ci dessous en classe ??
    width = 350
    height = 350
    fps = 50

    root = Tk()
    root.title("Collision test")

    config.CANVAS = Canvas(root, width=width, height=height, bg="black")
    config.CANVAS.pack()
    config.CANVAS.bind('<B1-Motion>', deplacement_balle)
    config.CANVAS.bind('<Right>', right_key)
    config.CANVAS.bind('<Left>', left_key)
    config.CANVAS.bind('<KeyRelease-Right>', right_key_release)
    config.CANVAS.bind('<KeyRelease-Left>', left_key_release)
    config.CANVAS.focus_set()

    balles = list()
    balles.append(Balle(50, 50, 0, 1))

    barres = list()
    barres.append(Barre(100, 300))

    murs = list()
    murs.append(Mur(-200, 0, 201, height-1))
    murs.append(Mur(0, -200, width, 201))
    murs.append(Mur(width, 0, 200, height-1))
    murs.append(Mur(0, height, width, height+200))

    briques = list()
    briques.append(Brique(80, 100, 5))
    briques.append(Brique(144, 100, 5, "", "indestructible"))
    briques.append(Brique(208, 100, 5, "agrandir_barre"))
    briques.append(Brique(80, 132, 5, "", "explosive"))
    briques.append(Brique(144, 132, 5))
    briques.append(Brique(208, 132, 5))

    flags = list()

    bonus = list()

    update()
    mainloop()
