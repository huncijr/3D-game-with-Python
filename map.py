import pygame as pg
_ = False

mini_map = \
[
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 2],
            [2, _, 3, 3, 3, _, _, _, _, _, _, 4, 4, _, _, 2],
            [5, _, 3, _, _, _,_, _, _, _, _, 4, 4, _ , _, 2],
            [5, _, 3,_, _, _, _, _,  2, _, _, _, _, _, _, 2],
            [5, _, _, _, _, _, _, _, 2, _, _, _, _, _, _, 2],
            [2, 5, _, _, _, _, _, _, 2, 2, 2, 2, _, _, _, 2],
            [2, 5, _, _, 1, 1, _, _, _, _, 2, 2, 2, _, _, 2],
            [2, _, _, _, _, _, _, _, _, _, _, _, _,_, _, 2],
            [2, _, _, _, _, _, _, _, 4, 4, _, _, _, _, _, 2],
            [2, _, _, 2, _, _, _, _, _, _, _, 5, 5, 5, _, 2],
            [2, _, 2, _, _, 6 ,6, _, _, _, _, _, 5, _ , _,2],
            [2, _, 2, _, _, 6, 6, _, _, _, _, _, 5, _, _, 2],
            [2, _, _, 2, _, _, _, _, _, _, 4, _, _, _, _, 2],
            [5, 5, _, _, _, _, _, _, 4, 4, 4, _, _, _, _, 2],
            [2, 5, _, _, 1, 1, _, _, _, _, _, _, _, _, _, 2],
            [2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
]
class Map:
    def __init__(self,game):
        self.game = game
        self.mini_map = mini_map
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map): #j a sor indexe (Y koordináta),row=a sorok
            for i,value in enumerate(row): #i az oszlop indexe (X koordináta),
               if value: #value az aktuális érték (1 vagy _).
                   self.world_map[(i,j)] = value
    def draw(self):
        [pg.draw.rect(self.game.screen,'red', (pos[0] * 100, pos[1] * 100, 100, 100), 2)  #lerajzol egy 100x100-as szurke négyzetet a képernyőn a (200, 300) pontnál, tehát a 2. oszlop, 3. sor helyére, ha a cellaméret 100 pixel.
         #x,y,szelleseg,magassag
         for pos in self.world_map]