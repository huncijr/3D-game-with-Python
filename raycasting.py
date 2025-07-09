import pygame as pg
import math
from settings import *

class RayCasting:
    def __init__(self, game):
        self.game = game  
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
        ox, oy = self.game.player.pos  
        x_map, y_map = self.game.player.map_pos  
        texture_vertical,texture_horizontal = 1,1
        ray_angle = self.game.player.angle - Half_FOV + 0.0001  

        for ray in range(NUM_RAYS): 
            sin_a = math.sin(ray_angle)  
            cos_a = math.cos(ray_angle)  

            # Vízszintes metszéspont keresése
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)  # a következő vízszintes csempe iránya
            depth_horizontal = (y_hor - oy) / sin_a  
            x_hor = ox + depth_horizontal * cos_a  
            delta_depth = dy / sin_a 
            dx = delta_depth * cos_a  

            for i in range(MAX_DEPTH): 
                tile_horizontal = int(x_hor), int(y_hor)  # jelenlegi csempe koordináta
                if tile_horizontal in self.game.map.world_map:  # ha falat talál
                    texture_horizontal = self.game.map.world_map[tile_horizontal]
                    break
                x_hor += dx  
                y_hor += dy
                depth_horizontal += delta_depth  

            
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

          
            # depth,texture offset
            if depth_vertical < depth_horizontal:
                depth,texture = depth_vertical,texture_vertical
                y_vert %=1
                offset = y_vert if cos_a >0 else(1-y_vert)
            else:
                depth,texture = depth_horizontal,texture_horizontal
                x_hor %= 1
                offset = (1-x_hor) if sin_a > 0 else x_hor

            
            depth *= math.cos(self.game.player.angle-ray_angle)
           
            proj_height = SCREEN_DIST / (depth + 0.0001)  # 3D magasság kiszámítása

            #ray casting result
            self.raycasting_result.append((depth,proj_height,texture,offset))

            ray_angle += DELTA_ANGLE  # továbbhaladás a következő sugárra (következő képernyőoszlop)

    def update(self):
        self.ray_cast()  
        self.get_object_to_render()

