#!/usr/bin/python3
from tkinter import *

''' Utilisation :
Attention, si fenêtre fermée autrement qu'avec "ok",
le main renverra {}. On devra alors ignorer la saisie dans
la classe jeu.
'''

TESTING = False
PSEUDO = ''
SEED = None


def main(mode):
    global PSEUDO, SEED
    PSEUDO = ''
    SEED = None
    fenetre(mode)
    out = {}
    if (PSEUDO != ''):
        out['pseudo'] = PSEUDO
    if (SEED is not None):
        out['seed'] = SEED
    return out


def fenetre(mode):
    '''
    mode défini si on est en mode campagne ou arcade : en fonction, on demande ou non un seed
    '''
    def newseed():
        import random
        if (e_seed.get() != ''):  # plante si champ vide
            e_seed.delete(0, len(e_seed.get()))
        length = 10
        valid_letters = 'abcdefghijklmnopqrstuvwxyz0123456789'
        randstr = ''.join((random.choice(valid_letters) for i in range(length)))
        e_seed.insert(0, randstr)

    def videEntree():
        e_pseudo.configure(bg='white')
        if (e_pseudo.get() != ''):  # plante si champ vide
            e_pseudo.delete(0, len(e_pseudo.get()))

    def signaleErreur():
        t_pseudo.configure(fg='red')    # colorer le fond du champ
        fen.update()
        e_pseudo.after(100, videEntree())    # après 1 seconde, effacer

    def validation():
        global PSEUDO, SEED
        destroy = True
        if (_pseudo):
            PSEUDO = e_pseudo.get()
            if (PSEUDO == '' or not PSEUDO.isalnum()):
                destroy = False
                signaleErreur()
        if (_seed):
            SEED = e_seed.get()
        if (destroy):
            fen.quit()
            fen.destroy()

    fen = Toplevel()
    fen.title("Parametrage")

    if (mode == "arcade"):
        _seed = True
        _pseudo = True
    elif (mode == "campagne"):
        _seed = False
        _pseudo = True
    elif (mode == "coop"):
        _seed = True
        _pseudo = False
    else:
        print("PROBLEME ARGUMENT DANS ", __file__, ":main(String mode)\n")

    rowpseudo = 0
    rowseed = int(_pseudo)
    rowbutton = int(_pseudo) + int(_seed)

    if (_pseudo):
        t_pseudo = Label(fen, text="Pseudo")
        t_pseudo.grid(row=rowpseudo, sticky=E, padx=2)
        e_pseudo = Entry(fen, width = 15)
        e_pseudo.grid(row=rowpseudo, column=1, columnspan = 2, pady=3, padx=3)
        e_pseudo.focus_set()

    if (_seed):
        t_seed = Label(fen, text="Seed")
        t_seed.grid(row=rowseed, sticky=E, padx=2)
        e_seed = Entry(fen, width=15)
        e_seed.grid(row=rowseed, column=1, columnspan=2, pady=3, padx=3)
        newseed()
        Button(fen, text="New seed", command=newseed).\
            grid(row=rowbutton, column=0, columnspan=2, pady=2, padx=2)
        if not _pseudo:
            e_seed.focus_set()

    Button(fen, text="Ok", command=validation).\
          grid(row=rowbutton, column=2, pady = 2)

    if (TESTING):
        print (' ok')
    fen.mainloop()

if __name__ == '__main__':
    TESTING = True
    print("test ecran parametrage..")
    print("outcome=", main("arcade"))
    print("outcome=", main("campagne"))
    print("outcome=", main("coop"))
