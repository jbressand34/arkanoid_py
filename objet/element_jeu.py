import config


class Rect(object):
    # nb = 0 # Variable de classe
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.dx = 0
        self.dy = 0
        self.surface = None
        self.bonus = ""  # servira pour brique explosive, balle de feu, etc
        self.bonus_frameleft = 0  # 0 signifie infini (non traité), sinon on décrémente à chaque frame

    def create_surface(self):
        return config.CANVAS.create_rectangle(self.x, self.y, self.x+self.w,
                                              self.y+self.h, outline='blue',
                                              fill='green', tags=('unknown'))

    def move(self):
        self.x += self.dx
        self.y += self.dy
        config.CANVAS.move(self.surface, self.dx, self.dy)

    def __del__(self):
        try:
            config.CANVAS.delete(self.surface)
        except:
            pass


class Brique(Rect):
    def __init__(self, x, y, pv=1, bonus_contenu="", bonus=""):
        Rect.__init__(self, x, y, 64, 32)
        self.pv = pv
        self.bonus_contenu = bonus_contenu
        self.bonus = bonus  # utilisation abusive du nom "bonus", ici état permanent.
        self.draw()

    def draw(self):
        if (self.surface is None):
            self.surface = Rect.create_surface(self)
        if (not self.bonus):
            config.CANVAS.itemconfig(self.surface, width=(self.pv)//2, outline='grey50',
                                     fill=('grey'+str(15+self.pv*5)), tags=('brique'))
        elif (self.bonus == "explosive"):
            config.CANVAS.itemconfig(self.surface, width=(self.pv)//2, outline='indian red',
                                     fill='red3', tags=('brique'))
        elif (self.bonus == "indestructible"):
            config.CANVAS.itemconfig(self.surface, width=2, outline='grey90',
                                     fill='grey80', tags=('brique'))

    def __del__(self):
        try:
            config.CANVAS.delete(self.surface)
            config.SCORE += config.SCORE_PAR_BRIQUE
        except:
            pass

class Barre(Rect):
    def __init__(self, x, y, w=config.BARRE_W, h=30):
        Rect.__init__(self, x, y, w, h)
        self.draw()

    def draw(self):
        if (self.surface is None):
            self.surface = Rect.create_surface(self)
        config.CANVAS.itemconfig(self.surface, outline='grey60', fill='grey25', tags=('barre'))

    def redraw(self):
        config.CANVAS.delete(self.surface)
        self.surface = Rect.create_surface(self)
        self.draw()

    def gestionbonus(self):
        if (self.bonus_frameleft):
            self.bonus_frameleft -= 1
            if (self.bonus_frameleft == 0):
                self.applybonus('')

    def applybonus(self, bonus):
        def resize(self, dw):
            self.w = self.w + dw
            self.x -= dw/2
            self.redraw()

        if (bonus == ''):
            # self.w = config.BARRE_W
            # self.redraw()
            if (self.bonus == "barre_retrecie"):
                resize(self, 50)
            elif (self.bonus == "barre_agrandie"):
                resize(self, -50)
            self.bonus = ''
            self.bonus_frameleft = 0
        else:
            self.bonus_frameleft = config.BONUS_DURATION
            if (bonus == "barre_retrecie" and self.bonus != "barre_retrecie"):
                if (self.bonus == "barre_agrandie"):
                    self.applybonus('')
                else:
                    self.bonus = bonus
                    resize(self, -50)
            elif (bonus == "barre_agrandie" and self.bonus != "barre_agrandie"):
                if (self.bonus == "barre_retrecie"):
                    self.applybonus('')
                else:
                    self.bonus = bonus
                    resize(self, 50)


class Balle(Rect):
    def __init__(self, x, y, dx=0, dy=2):
        Rect.__init__(self, x, y, 20, 20)
        self.dx = dx
        self.dy = dy
        self.draw()

    def draw(self):
        if (self.surface is None):
            self.surface = Rect.create_surface(self)
        if (self.bonus == ''):
            config.CANVAS.itemconfig(self.surface, outline='grey70', fill='grey70', tags=('balle'))
        elif (self.bonus == 'balle_feu'):
            config.CANVAS.itemconfig(self.surface, outline='brown', fill='orange red', tags=('balle'))

    def redraw(self):
        config.CANVAS.delete(self.surface)
        self.surface = Rect.create_surface(self)
        self.draw()

    def applybonus(self, bonus):
        if (bonus == ''):
            self.bonus_frameleft = 0
            self.bonus = ''
            self.redraw()
        else:
            self.bonus_frameleft = config.BONUS_DURATION
            if (bonus == "balle_feu" and self.bonus != "balle_feu"):
                self.bonus = bonus
                self.redraw()

    def gestionbonus(self):
        if (self.bonus_frameleft):
            self.bonus_frameleft -= 1
            if (self.bonus_frameleft == 0):
                self.applybonus('')


class Mur(Rect):
    def __init__(self, x, y, x2, y2):
        Rect.__init__(self, x, y, x2, y2)
        self.draw()

    def draw(self):
        if (self.surface is None):
            self.surface = Rect.create_surface(self)
        config.CANVAS.itemconfig(self.surface, outline='blue', fill='blue', tags=('mur'))


class Bonus(Rect):
    def __init__(self, x, y, bonus_contenu, dy=config.BONUS_SPEED):
        Rect.__init__(self, x, y, 20, 20)
        self.bonus_contenu = bonus_contenu
        self.dx = 0
        self.dy = dy
        self.draw()

    def __del__(self):
        try:
            for s in self.surface:
                config.CANVAS.delete(s)
        except:
                pass

    def move(self):
        self.x += self.dx
        self.y += self.dy
        for s in self.surface:
            config.CANVAS.move(s, self.dx, self.dy)

    def draw(self):
        if self.surface is None:
            self.surface = list()
            self.surface.append(Rect.create_surface(self))
        # indéfini
        config.CANVAS.itemconfig(self.surface[0], outline='grey70', fill='purple')

        if (self.bonus_contenu in config.BONUS):
            config.CANVAS.itemconfig(self.surface[0], outline='dark green', fill='green3')
            if self.bonus_contenu == "barre_agrandie":
                self.surface.append(
                    config.CANVAS.create_polygon(
                        [self.x+self.w/2-1, self.y+4,
                         self.x+3, self.y+self.h/2,
                         self.x+self.w/2-1, self.y+self.h-4],
                        outline='yellow4',
                        fill='yellow2', width=1)
                    )
                self.surface.append(
                    config.CANVAS.create_polygon(
                        [self.x+self.w/2+1, self.y+4,
                         self.x+self.w-3, self.y+self.h/2,
                         self.x+self.w/2+1, self.y+self.h-4],
                        outline='yellow4',
                        fill='yellow2', width=1)
                    )
            if self.bonus_contenu == "ajout_balle":
                self.surface.append(
                    config.CANVAS.create_polygon(
                        [
                         self.x+4, self.y+self.h/2-2,
                         self.x+self.w/2-2, self.y+self.h/2-2,
                         self.x+self.w/2-2, self.y+4,
                         self.x+self.w/2+2, self.y+4,
                         self.x+self.w/2+2, self.y+self.h/2-2,
                         self.x+self.w-4, self.y+self.h/2-2,
                         self.x+self.w-4, self.y+self.h/2+2,
                         self.x+self.w/2+2, self.y+self.h/2+2,
                         self.x+self.w/2+2, self.y+self.h-4,
                         self.x+self.w/2-2, self.y+self.h-4,
                         self.x+self.w/2-2, self.y+self.h/2+2,
                         self.x+4, self.y+self.h/2+2,
                         ],
                        outline='yellow4',
                        fill='yellow2', width=1)
                    )
            if self.bonus_contenu == "balle_feu":
                self.surface.append(
                    config.CANVAS.create_rectangle(
                        self.x+5, self.y+5,
                        self.x+self.w-5, self.y+self.h-5,
                        outline='yellow4', fill='red2', width=1)
                    )
        # fin bonus
        elif self.bonus_contenu in config.MALUS:
            config.CANVAS.itemconfig(self.surface[0], outline='dark red', fill='red3')
            if self.bonus_contenu == 'barre_retrecie':
                self.surface.append(
                    config.CANVAS.create_polygon(
                        [self.x+3, self.y+4,
                         self.x+self.w/2-1, self.y+self.h/2,
                         self.x+3, self.y+self.h-4],
                        outline='yellow4',
                        fill='yellow2', width=1)
                    )
                self.surface.append(
                    config.CANVAS.create_polygon(
                        [self.x+self.w-3, self.y+4,
                         self.x+self.w/2+1, self.y+self.h/2,
                         self.x+self.w-3, self.y+self.h-4],
                        outline='yellow4',
                        fill='yellow2', width=1)
                    )
                pass

if __name__ == '__main__':
    from tkinter import *
    root = Tk()
    root.title("Arkanoid")
    config.CANVAS = Canvas(root, width=400, height=300, bg="grey10")
    config.CANVAS.pack()

    briques = list()
    briques.append(Brique(5, 5, 3))
    for b in briques:
        b.draw()
        briques.remove(b)

    x = 5
    bl = list()
    for b in config.BONUS:
        bl.append(Bonus(x, 55, b))
        x += 25

    for b in bl:
        b.draw()

    x = 5
    ml = list()
    for m in config.MALUS:
        ml.append(Bonus(x, 85, m))
        x += 25

    for m in ml:
        m.draw()
    '''
    for m in ml:
        for s in m.surface:
            config.CANVAS.delete(s)
    '''
    config.CANVAS.mainloop()
