#!/usr/bin/python3

from tkinter import *
import top10
import config
import pseudo_seed
import jeu

class main():
    def __init__(self):
        self.root = Tk()
        self.root.title("Arkanoid")
        self.root.minsize(width=config.WIDTH+5, height=config.HEIGHT+5)
        config.CANVAS = Canvas(self.root, width=config.WIDTH, height=config.HEIGHT, bg="grey10")
        config.CANVAS.pack()
        self.jeu = jeu.Jeu("auto")
        self.widgets = list()
        self.pseudo = None

        self.pause = False

        config.CANVAS.bind("<Key>", self.transition)

        self.accueil()
        self.update()
        config.CANVAS.mainloop()

    def accueil(self):
        self.etape = "accueil"
        self.widgets.append(
            config.CANVAS.create_text(
                config.WIDTH//2, config.HEIGHT//2+15,
                anchor=CENTER, font=("Droidsan", 30), text="ARKANOID", fill="#FF3333"))
        self.widgets.append(
            config.CANVAS.create_text(
                config.WIDTH//2, 4*config.HEIGHT//5, anchor=CENTER, font=("Droidsan", 18),
                text="Appuyez sur une touche", fill="#FFFFFF"))

    def init_partie(self, mode):
        data = pseudo_seed.main(mode)
        if data == {}:
            print("echec saisie")
        else:
            if (mode == "arcade" or mode == "coop"):
                seed = data['seed']
            if (mode == "arcade" or mode == "campagne"):
                top10.load_score()
                self.pseudo = data['pseudo']

            config.CANVAS.delete(ALL)
            del self.jeu
            if (mode == "arcade" or mode == "coop"):
                self.jeu = jeu.Jeu(mode, seed)
            elif (mode == "campagne"):
                self.jeu = jeu.Jeu(mode)
        self.etape = "jeu"
        self.supprWidgets()
        config.CANVAS.bind('<FocusOut>', self.focus_lost)
        config.CANVAS.bind("<P>", self.pause_toggle)
        config.CANVAS.bind("<p>", self.pause_toggle)
        config.CANVAS.bind("<Pause>", self.pause_toggle)

    def menu(self):
        x = 400
        y = 300
        self.etape = "menu"
        self.widgets.append(
            config.CANVAS.create_rectangle(x-130, y-80, x+130, y+150, outline='grey',
                                           width=3, fill='grey40'))
        self.widgets.append(
            config.CANVAS.create_text(
                x, y-50, anchor=CENTER, font=("Droidsan", 25), text="ARKANOID", fill="#FFFFFF"))
        Boutons = list()
        Boutons.append(Button(config.CANVAS, text="Arcade", command=lambda: self.init_partie('arcade')))
        Boutons.append(Button(config.CANVAS, text="Campagne", command=lambda: self.init_partie('campagne')))
        Boutons.append(Button(config.CANVAS, text="Coop", command=lambda: self.init_partie('coop')))
        Boutons.append(Button(config.CANVAS, text="Top10", command=top10.main))
        Boutons.append(Button(config.CANVAS, text="Quitter", command=exit))

        for Bouton in Boutons:
            self.widgets.append(config.CANVAS.create_window(x, y, width=200, window=Bouton))
            y += 30

    def supprWidgets(self):
        for widget in self.widgets:
                config.CANVAS.delete(widget)
        del self.widgets
        self.widgets = list()

    # ####### EVENT #############################

    def transition(self, event):
        if (self.etape == "accueil"
        or (self.etape == "jeu" and self.jeu.vies == 0)):
            self.supprWidgets()
            self.menu()

    def setpause(self):
        self.pause = True
        self.widgets.append(
            config.CANVAS.create_text(
                config.WIDTH//2, config.HEIGHT//2,
                font=("Droidsan", 24), text="Pause", fill="#FF3333"))

    def focus_lost(self, event):
        if not self.pause:
            self.setpause()

    def pause_toggle(self, event):
        if self.pause:
            self.pause = False
            self.supprWidgets()
        else:
            self.setpause()
    #############################################

    def update(self):
        if self.pause:
            self.root.after(10*1000//(config.FPS), self.update)
        else:
            self.root.after(1000//config.FPS, self.update)
            self.jeu.update()
            if (not self.jeu.vies and not self.widgets):
                self.partiefinie()

    def partiefinie(self):
        self.widgets.append(
            config.CANVAS.create_text(
                config.WIDTH//2, config.HEIGHT//2,
                font=("Droidsan", 24), text="GAME OVER", fill="#FF3333"))
        if (self.jeu.mode == "arcade" and config.SCORE > config.SCORE_ARCADE[9][1])\
        or (self.jeu.mode == "campagne" and config.SCORE > config.SCORE_CAMP[9][1]):
            top10.ajoutscore(self.jeu.mode, self.pseudo)
            self.widgets.append(
                config.CANVAS.create_text(
                config.WIDTH//2, 3*config.HEIGHT//5,
                font=("Droidsan", 24), text="Bravo tu viens d'entrer dans les highscores !!!",
                fill="#FFFFFF"))
        self.widgets.append(
            config.CANVAS.create_text(
                config.WIDTH//2, 4*config.HEIGHT//5,
                anchor=CENTER, font=("Droidsan", 18),
                text="Appuyez sur une touche", fill="#FFFFFF"))
        self.pause = True
        config.CANVAS.unbind('<FocusOut>')
        config.CANVAS.unbind('<Pause>')
        config.CANVAS.unbind('<P>')
        config.CANVAS.unbind('<p>')

if __name__ == "__main__":
    main()
