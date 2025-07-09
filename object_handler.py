from sprite_object import *
from NPC import *

class ObjectHandler:
    def __init__(self,game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = '3D game/NPC'
        self.static_sprite_path =  '3D game/Spriteok/'
        self.anim_sprite_path = '3D game/Animalt_Spriteok/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_position = {}
        #sprite map
        add_sprite(SpriteObject(game))
        add_sprite(AnimatedSprite(game))

        add_sprite(SpriteObject(game))  
        add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))  
        add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))  

        add_sprite(AnimatedSprite(game, pos=(5.5, 5.5)))  
        add_sprite(AnimatedSprite(game, pos=(11.5, 13.5)))  
        add_sprite(AnimatedSprite(game, pos=(13.5, 3.5)))
        add_sprite(AnimatedSprite(game, pos=(14.5, 10.5)))  
        add_sprite(AnimatedSprite(game, pos=(10.5, 1.5)))  
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'husos_cucc/hus1.png', pos=(2.5, 10.5)))  # külön sprite
        add_sprite(AnimatedSprite(game, path=self.anim_sprite_path + 'husos_cucc/hus1.png', pos=(6.5, 13.5)))  # külön sprite

        #add_npc(NPC(game))
        #add_npc(NPC(game,pos=(10,7)))
        add_npc(NPC(game,pos=(2,8)))
        add_npc(NPC(game, pos=(12, 8)))
        add_npc(NPC(game,pos=(8,15)))
        add_npc(NPC(game, pos=(10, 11)))
        add_npc(CacoDemonNPC(game, pos=(14, 3)))
        add_npc(CacoDemonNPC(game, pos=(12, 14)))
        add_npc(CacoDemonNPC(game, pos=(13, 13)))
        add_npc(CacoDemonNPC(game, pos=(9, 10)))
        add_npc(CyberDemonNPC(game, pos=(13,15)))
        add_npc(CyberDemonNPC(game, pos=(2, 14)))
        #add_npc(SoldierNPC(game, pos=(11.0, 19.0)))
        #add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        #add_npc(SoldierNPC(game, pos=(13.5, 6.5)))
        #add_npc(SoldierNPC(game, pos=(2.0, 20.0)))
        # add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        # add_npc(CacoDemonNPC(game, pos=(12.5, 4.5)))
        # add_npc(CacoDemonNPC(game, pos=(5.5, 16.5)))


    def update(self):
        self.npc_position = {npc.map_pos for npc in self.npc_list if npc.alive}
        for sprite in self.sprite_list:
            sprite.update()
        for npc in self.npc_list:
            npc.update()

    def check_win(self):
        if not len(self.npc_positions):
            self.game.object_renderer.win()
            pg.display.flip()
            pg.time.delay(1500)
            self.game.new_game()
    def add_npc(self,npc):
        self.npc_list.append(npc)


    def add_sprite(self,sprite):
        self.sprite_list.append(sprite)
