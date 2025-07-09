import pygame as pg

class Sound:
    def __init__(self,game):
        self.game = game
        pg.mixer.init()
        self.path = 'C:/Users/hunor/Desktop/3D modellezes Project/3D game/Fegyverek/fegyverhang/'
        self.shotgun = pg.mixer.Sound(self.path + 'resources_sound_shotgun.wav')
        self.shotgun.set_volume(0.3)
        self.npc_pain = pg.mixer.Sound('C:/Users/hunor/Desktop/3D modellezes Project/3D game/NPC/NPC hangok/resources_sound_npc_pain.wav')
        self.npc_shot = pg.mixer.Sound('C:/Users/hunor/Desktop/3D modellezes Project/3D game/NPC/NPC hangok/resources_sound_npc_attack.wav')
        self.npc_death = pg.mixer.Sound('C:/Users/hunor/Desktop/3D modellezes Project/3D game/NPC/NPC hangok/resources_sound_npc_death.wav')
        self.player_pain = pg.mixer.Sound('C:/Users/hunor/Desktop/3D modellezes Project/3D game/NPC/NPC hangok/resources_sound_player_pain.wav')
        self.theme = pg.mixer.music.load('C:/Users/hunor/Desktop/3D modellezes Project/3D game/NPC/NPC hangok/resources_sound_theme.mp3')
        self.npc_pain.set_volume(0.2)
        self.npc_shot.set_volume(0.2)
        self.npc_death.set_volume(0.2)
