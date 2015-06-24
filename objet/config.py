'''
On mettra ici nos variables globales à importer dans les autres modules
'''

FPS = 50

SCORE = 0
SCORE_CAMP = None
SCORE_ARCADE = None
SCORE_PAR_BRIQUE = 10

BRIQUE_OFFSET_X = 50
BRIQUE_OFFSET_Y = 30
BRIQUE_NB_X = 11        # Nb de colonne de briques
BRIQUE_NB_Y = 8         # Nb de rangée de briques
BRIQUE_W = 64
BRIQUE_H = 32
BRIQUE_MIN_PV = 1       # Min inclus
BRIQUE_MAX_PV = 4       # Max exclus
BRIQUE_TYPE_B = ['explosive']
BRIQUE_TYPE_M = ['indestructible']

BONUS_DURATION = 400    # Durée des bonus en nb de frame
BONUS_SPEED = 1.0       # Vitesse de descente des bonus
BONUS = ['ajout_balle', 'barre_agrandie', 'balle_feu']
MALUS = ['barre_retrecie']

BALLE_SPEED_INIT = 1.0      # Vitesse initiale de la balle
SPEED_PER_FRAME = 0.0003    # Incrément de vitesse par frame (effectif sur rebond sur la barre)
SPEED = BALLE_SPEED_INIT

BARRE_SPEED = 6
BARRE_W = 100

CANVAS = None
WIDTH = 800
HEIGHT = 600
