from settings import *
import pygame as pg
import math


class Player:
    def __init__(self,game):
        self.game=game
        self.x,self.y= PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = PLAYER_MAX_HEALTH
        self.rel = 0

    def check_game_over(self):
        if self.health <1:
           self.game.object_renderer.game_over()
           pg.display.flip()
           pg.time.delay(1500)
           self.game.new_game()
    def get_damage(self,damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.check_game_over()

    def single_fire_event(self,event):
        if event.type == pg.MOUSEBUTTONDOWN:
           if event.button == 1 and not self.shot and not self.game.weapon.reloading:
               self.game.sound.shotgun.play()
               self.shot = True
               self.game.weapon.reloading = True


    def movement(self):
        dx, dy = 0, 0
        '''
        Ha pg.k_W => dx=SPEED*cos(a),dy=SPEED*sin(a)
        Ha pg.k_S => dx=-SPEED*cos(a),dy=-SPEED*sin(a)
        Ha pg.k_D => dx=-SPEED*sin(a),dy=+SPEED*cos(a)
        Ha pg.k_A => dx=SPEED*sin(a), dy=-SPEED*cos(a)
        '''
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)

        speed= PLAYER_SPEED *self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        keys=pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy +=speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        self.check_wall_collision(dx,dy)
        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time
        self.angle %= math.tau #math.tau  = 2π

    def check_walls(self,x,y):
        return (x,y) not in self.game.map.world_map
    def check_wall_collision(self,dx,dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_walls(int(self.x+dx),int(self.y)):
            self.x += dx
        if self.check_walls(int(self.x), int(self.y+dy)):
            self.y += dy

    def draw(self):
        #pg.draw.line(self.game.screen,(255, 0, 0),(self.x*100,self.y*100), #felület, szín, kezdőpont,
        #(self.x*100+WIDTH*math.cos(self.angle), #végpont,
        # self.y*100+WIDTH*math.sin(self.angle)),
        #             2) #vastagsag
        pg.draw.circle(self.game.screen,'#25bfae',(self.x *100,self.y*100),15) #(felület, szín, középpont, sugár)

    def mouse_control(self):
        mx,my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx> MOUSE_BORDER_LEFT:
            pg.mouse.set_pos(HALF_WIDTH,HALF_HEIGHT)
            self.rel = pg.mouse.get_rel()[0]
            self.rel = max(-MOUSE_MAX_REL,min(MOUSE_MAX_REL,self.rel))
            self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time
    def update(self):
        self.movement()
        self.mouse_control()
    @property
    def pos(self):
        return self.x,self.y
    @property
    def map_pos(self):
        return int(self.x),int(self.y)

