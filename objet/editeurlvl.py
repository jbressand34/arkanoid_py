#!/usr/bin/python3

from tkinter import *
from pickle import *
from element_jeu import *
import config
import os

class EditeurLvl(object):
    def __init__(self):
        self.nbBriques = 0
        self.vie = 1
        self.x = 40
        self.y = 30
        self.bonus_malus = ''
        self.type_brique = ''
        self.briques = list()
        self.labels = list()

        global helpcan
        helpfen = Tk()
        helpcan = Canvas(helpfen)
        helpcan.pack()

        self.labels.append(Label(helpcan, text = "O vies correspond à l'abscence de brique."))
        self.labels.append(Label(helpcan, text = "Appuyez sur entrée pour ajouter une brique avec les paramètres suivants :"))
        self.labels.append(Label(helpcan, text = "Vie : "+str(self.vie)))
        self.labels.append(Label(helpcan, text = "Bonus ou malus : "+str(self.bonus_malus)))
        self.labels.append(Label(helpcan, text = "Type de brique : "+str(self.type_brique)))

        self.labels.append(Label(helpcan, text = ""))

        self.labels.append(Label(helpcan, text = "Vie 0 : w"))
        self.labels.append(Label(helpcan, text = "Vie 1 : x"))
        self.labels.append(Label(helpcan, text = "Vie 2 : c"))
        self.labels.append(Label(helpcan, text = "Vie 3 : v"))

        self.labels.append(Label(helpcan, text = ""))

        self.labels.append(Label(helpcan, text = "Explosive : a"))
        self.labels.append(Label(helpcan, text = "Indestructible : z"))
        self.labels.append(Label(helpcan, text = "Normale : e"))

        self.labels.append(Label(helpcan, text = ""))

        self.labels.append(Label(helpcan, text = "Ajout d'une balle : q"))
        self.labels.append(Label(helpcan, text = "Barre agrandie : s"))
        self.labels.append(Label(helpcan, text = "Balle de feu : d"))
        self.labels.append(Label(helpcan, text = "Barre rétrécie : f"))
        self.labels.append(Label(helpcan, text = "Aucun bonus ou malus : g"))

        self.labels.append(Label(helpcan, text = ""))

        for label in self.labels:
            label.pack()

        self.updateaffichage()

        root = Tk()
        root.title("Editeur de niveaux")
        root.minsize(width=800+5, height=600+5)


        config.CANVAS = Canvas(root, width=800, height=600, bg="grey10")

        config.CANVAS.focus_set()

        config.CANVAS.bind('<Return>', self.ajoutBrique)

        config.CANVAS.bind("<w>", self.setVies0)
        config.CANVAS.bind("<x>", self.setVies1)
        config.CANVAS.bind("<c>", self.setVies2)
        config.CANVAS.bind("<v>", self.setVies3)

        config.CANVAS.bind("<a>", self.setTypeExplo)
        config.CANVAS.bind("<z>", self.setTypeIndes)
        config.CANVAS.bind("<e>", self.setTypeNormal)

        config.CANVAS.bind("<q>", self.setBonAjoutBall)
        config.CANVAS.bind("<s>", self.setBonBarreAgrandie)
        config.CANVAS.bind("<d>", self.setBonBalleFeu)
        config.CANVAS.bind("<f>", self.setMalBarreRetrecie)
        config.CANVAS.bind("<g>", self.setBonMalNone)

        config.CANVAS.pack()

        root.mainloop()

    # prends une liste de briques et l'inscrit dans un fichier dans le repertoire levels
    def write(self,nomlvl):
        NomFichier = nomlvl+'.lvl'
        file = open('levels/'+str(NomFichier),'wb')
        dump(self.briques,file)
        file.close()

    def fenenregistrement(self):
        for brique in self.briques:
            brique.surface = None
        global form
        form = Tk()
        lab = Label(form, text="Nom de niveau :")
        global box
        box = Entry(form)
        but = Button(form, text="Valider", command=self.enregistrerLvl)
        lab.pack()
        box.pack()
        but.pack()

    def enregistrerLvl(self):
        self.write(box.get())
        form.quit()


    def updateaffichage(self):
        self.labels[2].config(text = "Vie : "+str(self.vie))
        self.labels[3].config(text = "Bonus ou malus : "+str(self.bonus_malus))
        self.labels[4].config(text = "Type de brique : "+str(self.type_brique))

    ##############################
    #### EVENTS
    def ajoutBrique(self, event):
        if (self.nbBriques < 11*8) :
            if (self.vie > 0) :
                self.briques.append(Brique(self.x, self.y, self.vie, self.bonus_malus, self.type_brique))
            self.nbBriques+=1
            self.x = (self.nbBriques % 11)*64+40
            self.y = int(self.nbBriques / 11)*32+30
        else :
            config.CANVAS.unbind("<Return>")
            config.CANVAS.unbind("<w>")
            config.CANVAS.unbind("<x>")
            config.CANVAS.unbind("<c>")
            config.CANVAS.unbind("<v>")

            config.CANVAS.unbind("<a>")
            config.CANVAS.unbind("<z>")
            config.CANVAS.unbind("<e>")

            config.CANVAS.unbind("<q>")
            config.CANVAS.unbind("<s>")
            config.CANVAS.unbind("<d>")
            config.CANVAS.unbind("<f>")
            config.CANVAS.unbind("<g>")

            self.fenenregistrement()
        self.updateaffichage()

    def setTypeExplo(self, event):
        self.type_brique = 'explosive'
        self.updateaffichage()

    def setTypeIndes(self, event):
        self.type_brique = 'indestructible'
        self.updateaffichage()

    def setTypeNormal(self, event):
        self.type_brique = ''
        self.updateaffichage()

    def setBonAjoutBall(self, event):
        self.bonus_malus = 'ajout_balle'
        self.updateaffichage()

    def setBonBarreAgrandie(self, event):
        self.bonus_malus = 'barre_agrandie'
        self.updateaffichage()

    def setBonBalleFeu(self, event):
        self.bonus_malus = 'balle_feu'
        self.updateaffichage()

    def setMalBarreRetrecie(self, event):
        self.bonus_malus = 'barre_retrecie'
        self.updateaffichage()

    def setBonMalNone(self, event):
        self.bonus_malus = ''
        self.updateaffichage()

    def setVies0(self, event):
        self.vie = 0
        self.updateaffichage()

    def setVies1(self, event):
        self.vie = 1
        self.updateaffichage()

    def setVies2(self, event):
        self.vie = 2
        self.updateaffichage()

    def setVies3(self, event):
        self.vie = 3
        self.updateaffichage()



if __name__ == "__main__":
    EditeurLvl()

'''
# crée une fenetre affichant les niveaux enregistrés dans le dossier levels
def fenetre_lvl():
    fen_lvl = Tk()
    fen_lvl.title("Niveaux disponibles :")
    buttons=list()
    levels = os.listdir('levels')
    if len(levels) == 0:
        txt = Label(fen_lvl,text="Il n'y a pas de niveaux disponibles.")
        txt.pack()
    else:
        txt = Label(fen_lvl,text="Niveaux disponibles :", height=2)
        txt.pack()
        for lvl in levels:
            # crée un bouton par niveau dispo lançant le jeu avec ce niveau
            buttons.append(Button(fen_lvl, text=lvl, width=20))#, command=jouerNiveau(lvl)+fen_lvl.quit()))
    buttons.append(Button(fen_lvl, text="Quitter", command=fen_lvl.quit))
    for button in buttons:
        button.pack()

    fen_lvl.mainloop()
'''
