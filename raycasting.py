import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game  # hivatkozás a teljes játékobjektumra, hogy elérje pl. a játékos pozícióját, képernyőt, térképet
        self.raycasting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_object_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.raycasting_result):
            depth ,proj_height , texture, offset = values
            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),0,SCALE,TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column,(SCALE,proj_height))
                wall_pos = (ray * SCALE,HALF_HEIGHT -proj_height //2)
                self.objects_to_render.append((depth,wall_column,wall_pos))
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE),HALF_TEXTURE_SIZE-texture_height//2,
                    SCALE,texture_height
                )
                wall_column = pg.transform.scale(wall_column,(SCALE,HEIGHT))
                wall_pos = (ray*SCALE,0)
            self.objects_to_render.append((depth,wall_column,wall_pos))


    def ray_cast(self):
        self.raycasting_result = []
        ox, oy = self.game.player.pos  # a játékos pozíciója (ox, oy)
        x_map, y_map = self.game.player.map_pos  # a játékos térképpozíciója (egész csempék szerint)
        texture_vertical,texture_horizontal = 1,1
        ray_angle = self.game.player.angle - Half_FOV + 0.0001  # a sugár induló szöge, balról jobbra kezdve a látótérben

        for ray in range(NUM_RAYS):  # végigmegyünk az összes sugáron (pixeles oszlopokon)
            sin_a = math.sin(ray_angle)  # a szög szinusza
            cos_a = math.cos(ray_angle)  # a szög koszinusza

            # Vízszintes metszéspont keresése
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)  # a következő vízszintes csempe iránya
            depth_horizontal = (y_hor - oy) / sin_a  # a vízszintes találat távolsága
            x_hor = ox + depth_horizontal * cos_a  # vízszintes találat x koordinátája
            delta_depth = dy / sin_a  # lépésméret a következő vízszintes vonalig
            dx = delta_depth * cos_a  # x lépés az adott irányban

            for i in range(MAX_DEPTH):  # ciklus a vízszintes sugarakhoz
                tile_horizontal = int(x_hor), int(y_hor)  # jelenlegi csempe koordináta
                if tile_horizontal in self.game.map.world_map:  # ha falat talál
                    texture_horizontal = self.game.map.world_map[tile_horizontal]
                    break
                x_hor += dx  # továbblépés
                y_hor += dy
                depth_horizontal += delta_depth  # növeljük a sugarat

            # Függőleges metszéspont keresése
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)  # következő függőleges csempe iránya
            depth_vertical = (x_vert - ox) / cos_a  # távolság a függőleges találatig
            y_vert = oy + depth_vertical * sin_a  # y pozíció a falig
            delta_depth = dx / cos_a  # lépésméret a következő függőleges vonalig
            dy = delta_depth * sin_a  # y lépés

            for i in range(MAX_DEPTH):  # ciklus a függőleges sugarakhoz
                tile_vert = int(x_vert), int(y_vert)  # aktuális csempe koordináta
                if tile_vert in self.game.map.world_map:  # ha falat talál
                    texture_vertical =self.game.map.world_map[tile_vert]
                    break
                x_vert += dx  # továbblépés
                y_vert += dy
                depth_vertical += delta_depth

            # A kettő közül a kisebb távolságot vesszük (amelyik előbb falat talál)
            # depth,texture offset
            if depth_vertical < depth_horizontal:
                depth,texture = depth_vertical,texture_vertical
                y_vert %=1
                offset = y_vert if cos_a >0 else(1-y_vert)
            else:
                depth,texture = depth_horizontal,texture_horizontal
                x_hor %= 1
                offset = (1-x_hor) if sin_a > 0 else x_hor

            #eltavolitsuk a kozelitesnel a tul nagy fal effektek
            depth *= math.cos(self.game.player.angle-ray_angle)
            # Fal vetítése (projection) — minél közelebb van a fal, annál magasabb
            proj_height = SCREEN_DIST / (depth + 0.0001)  # 3D magasság kiszámítása

            #ray casting result
            self.raycasting_result.append((depth,proj_height,texture,offset))

            ray_angle += DELTA_ANGLE  # továbbhaladás a következő sugárra (következő képernyőoszlop)

    def update(self):
        self.ray_cast()  # minden képkockában újrarendereli a falakat
        self.get_object_to_render()

