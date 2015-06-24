#!/usr/bin/python3
from tkinter import *
from pickle import *
import config

''' Pour appeler de l'extérieur :
import top10
top10.main()
'''

'''Note: TO FIX
http://stackoverflow.com/questions/2763266/grid-within-a-frame
AJOUTER DES FRAMES
'''

TESTING = False

def load_score():
    ouverture_fichier()

def ouverture_fichier():
    file1 = open('scores_camp.sc','rb')
    file2 = open('scores_arc.sc','rb')
    config.SCORE_CAMP = load(file1)
    config.SCORE_ARCADE = load(file2)
    file1.close()
    file2.close()

def ecriture_fichier():
    file1 = open('scores_camp.sc','wb')
    file2 = open('scores_arc.sc','wb')
    dump(config.SCORE_CAMP,file1)
    dump(config.SCORE_ARCADE,file2)
    file1.close()
    file2.close()

def ajoutscore(mode,pseudo):
    if (mode == "arcade"):
        config.SCORE_ARCADE[9][0] = pseudo
        config.SCORE_ARCADE[9][1] = config.SCORE
        i = 8
        while (i>=0 and config.SCORE_ARCADE[i+1][1] > config.SCORE_ARCADE[i][1]):
            temp_pseudo = config.SCORE_ARCADE[i+1][0]
            temp_score = config.SCORE_ARCADE[i+1][1]
            config.SCORE_ARCADE[i+1][0] = config.SCORE_ARCADE[i][0]
            config.SCORE_ARCADE[i+1][1] = config.SCORE_ARCADE[i][1]
            config.SCORE_ARCADE[i][0] = temp_pseudo
            config.SCORE_ARCADE[i][1] = temp_score
            i += -1

    if (mode == "campagne"):
        config.SCORE_CAMP[9][0] = pseudo
        config.SCORE_CAMP[9][1] = config.SCORE
        i = 8
        while (i>=0 and config.SCORE_CAMP[i+1][1] > config.SCORE_CAMP[i][1]):
            temp_pseudo = config.SCORE_CAMP[i+1][0]
            temp_score = config.SCORE_CAMP[i+1][1]
            config.SCORE_CAMP[i+1][0] = config.SCORE_CAMP[i][0]
            config.SCORE_CAMP[i+1][1] = config.SCORE_CAMP[i][1]
            config.SCORE_CAMP[i][0] = temp_pseudo
            config.SCORE_CAMP[i][1] = temp_score
            i += -1
    ecriture_fichier()

def effacertoutscore():
    for i in range(10):
        config.SCORE_CAMP[i][1]=0
        config.SCORE_CAMP[i][0]="ordi"+str(i)
        config.SCORE_ARCADE[i][1]=0
        config.SCORE_ARCADE[i][0]="ordi"+str(i)
    ecriture_fichier()

def main():
    root = Tk()
    root.title('top10')

    titre1 = Label(root, text ="Campagne")
    titre1.grid(row =0, column =0, columnspan =2)
    titre1.config(padx=20, pady = 5)
    titre2 = Label(root, text ="Arcade")
    titre2.grid(row =0, column =2, columnspan =2)
    titre2.config(padx=20, pady = 5)

    load_score()

    l_scores1 = list()
    l_scores2 = list()
    l_scores3 = list()
    l_scores4 = list()
    for i in range(10):
        l_scores1.append(Label(root, text = config.SCORE_CAMP[i][0]))
        l_scores1[i].grid(row =i+1, column =0)
        l_scores1[i].config(padx=5)
        l_scores2.append(Label(root, text = config.SCORE_CAMP[i][1]))
        l_scores2[i].grid(row =i+1, column =1)
        l_scores2[i].config(padx=5)
        l_scores3.append(Label(root, text = config.SCORE_ARCADE[i][0]))
        l_scores3[i].grid(row =i+1, column =3)
        l_scores3[i].config(padx=5)
        l_scores4.append(Label(root, text = config.SCORE_ARCADE[i][1]))
        l_scores4[i].grid(row =i+1, column =4)
        l_scores4[i].config(padx=5)

    if (TESTING):
        print (' ok')
    mainloop()

if __name__ == '__main__':
    print("test top10..")
    TESTING = True;
    main()
