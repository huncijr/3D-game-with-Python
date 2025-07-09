import os                          # fájlkezeléshez
from collections import deque     # képek sorban való forgatásához használt dupla végű sor
import pygame as pg
from settings import *
import math


#Egy sprite egy grafikai objektum (kép), amit a képernyőn mozgatni, forgatni vagy animálni lehet.

class SpriteObject:
    def __init__(self,game,path="C:/Users/hunor/Desktop/3D modellezes Project/3D game/Spriteok/enemy.png",pos=(10.5,3.5),scale=1,shift=0):
        self.game = game
        self.player = game.player
        self.x,self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH= self.image.get_width() // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()# szélesség-magasság arány
        self.dx,self.dy,self.theta,self.screen_x,self.dist,self.norm_dist=0,0,0,0,1,1  # alapértelmezett értékek
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift                              # függőleges eltolás a vetítésnél

    def get_sprite_projection(self):  # sprite vetítése a 3D-ből 2D képernyőre
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE       # perspektivikus magasság kiszámítása
        proj_width,proj_height = proj * self.IMAGE_RATIO,proj         # szélesség magasság arány alapján
        image = pg.transform.scale(self.image,(proj_width,proj_height))  # kép átméretezése
        self.sprite_half_width = proj_width //2                       # fél szélesség a vízszintes pozícionáláshoz
        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT         # függőleges eltolás kiszámítása
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height //2 - height_shift  # képernyő pozíció (x,y)
        self.game.raycasting.objects_to_render.append((self.norm_dist,image,pos))  # hozzáadás a kirajzolási listához

    def get_sprite(self):  # sprite helyzetének és vetítésének kiszámítása
        dx = self.x - self.player.x                                  # sprite és játékos távolság x-ben
        dy = self.y - self.player.y                                  # sprite és játékos távolság y-ban
        self.dx , self.dy = dx, dy                                    # tárolás
        self.theta = math.atan2(dy,dx)                                # irányszög a sprite és játékos között

        delta = self.theta - self.player.angle                        # különbség a játékos nézési irányával
        if(dx > 0 and self.player.angle > math.pi) or (dx< 0 and dy<0):  # ha átugorja a 0/2pi határt
            delta += math.tau                                         # 2*pi hozzáadása

        delta_rays = delta / DELTA_ANGLE                              # hány sugárral van eltolva
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE          # képernyőn hova esik a sprite vízszintesen

        self.dist = math.hypot(dx,dy)                                 # sprite távolsága Pitagorasz-tétellel
        self.norm_dist = self.dist * math.cos(delta)                  # vetített távolság (kamera irányában)
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH+self.IMAGE_HALF_WIDTH) and self.norm_dist>0.5:  # ha képernyőn belül van és nincs túl közel
            self.get_sprite_projection()                              # megjelenítjük

    def update(self):             # frissíti a sprite állapotát minden frame-ben
        self.get_sprite()         # kiszámolja és vetíti

class AnimatedSprite(SpriteObject):  # sprite, ami animált (váltogatja a képeket)
    def __init__(self, game, path='C:/Users/hunor/Desktop/3D modellezes Project/3D game/Animalt_Spriteok/zold_sprite/tuzsprite1.png',
                 pos=(11.5, 3.5), scale=1, shift=0, animation_time=120):
        super().__init__(game, path, pos, scale, shift)               # meghívjuk az ősosztály konstruktorát
        self.animation_time = animation_time
        self.path = path.rsplit('/', 1)[0]                # csak a könyvtárat vesszük ki az elérési útból
        self.images = self.get_images(self.path)                      # képek betöltése deque-be
        self.animation_time_prev = pg.time.get_ticks()                # időbélyeg a legutóbbi váltáskor
        self.animation_trigger = False                                # trigger, hogy váltani kell-e képet

    def update(self):
        super().update()              # sprite pozíció és vetítés
        self.check_animation_time()   # megnézzük, lejárt-e az idő egy új frame-hez
        self.animate(self.images)     # ha igen, váltjuk a képet

    def animate(self, images):
        if self.animation_trigger:    # ha lejárt az idő
            images.rotate(-1)         # első kép hátra megy, következő előre
            self.image = images[0]    # új kép lesz az aktuális sprite

    def check_animation_time(self):   # időzítés kezelése
        self.animation_trigger = False                                # alapból nem váltunk képet
        time_now = pg.time.get_ticks()                                # jelenlegi idő lekérése
        if time_now - self.animation_time_prev > self.animation_time: # ha letelt az animációs idő
            self.animation_time_prev = time_now                       # új idő mentése
            self.animation_trigger = True                             # képet kell váltani

    def get_images(self, path):       # képek betöltése egy mappából
        images = deque()              # dupla végű sor a forgatáshoz
        for file_name in os.listdir(path):
            if os.path.isfile(os.path.join(path, file_name)):        # csak a fájlokat nézi (nem mappák)
                img = pg.image.load(path + '/' + file_name).convert_alpha() # kép betöltése áttetszőséggel
                images.append(img)                                    # hozzáadás a listához
        return images              # visszatér a betöltött képekkel
