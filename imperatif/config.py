'''
On mettra ici nos variables globales à importer dans les autres modules
'''

FPS = 50
WIDTH = 800
HEIGHT = 600

BRIQUE_OFFSET_X = 50
BRIQUE_OFFSET_Y = 30
BRIQUE_NB_X = 11        # Nb de colonne de briques
BRIQUE_NB_Y = 8        # Nb de rangée de briques
BRIQUE_W = 64
BRIQUE_H = 32
BRIQUE_MIN_PV = 1  # Min inclus
BRIQUE_MAX_PV = 5  # Max exclus
BRIQUE_TYPE_B = ['explosive']
BRIQUE_TYPE_M = ['indestructible']

BONUS_LENGTH = 400
BONUS_SPEED = 2
BONUS = ['ajout_balle', 'barre_agrandie', 'balle_feu']
MALUS = ['barre_retrecie']

BALLE_SPEED_INIT = 1.0
SPEED_PER_FRAME = 0.0003
SPEED = BALLE_SPEED_INIT

BARRE_SPEED = 6
BARRE_W = 100

CANVAS = None
