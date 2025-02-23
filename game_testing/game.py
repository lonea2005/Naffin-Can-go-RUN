#FFEDC1
import pygame
import sys
import os
import random
import math
from script.entity import Player, Enemy, Beam, Box, Scrap, Tutorial_trigger, Cutscene_trigger, Spike, Knife, Hook_start, Hook_stop  ,Camera_trigger
from script.utils import load_image,load_white_image
from script.utils import load_tile,load_trans_tile
from script.utils import load_fix_tile
from script.utils import load_images
from script.utils import load_trans_images,load_trans_image,load_trans_scaled_images,load_scaled_images,load_trans_scaled_image
from script.utils import load_sfx
from script.utils import Animation
from script.tilemap import Tilemap, small_tile
from script.particle import Particle
from script.spark import Spark, Flame, Ice_Flame, Gold_Flame, Dark_Blue_Flame,Flexible_Spark    

#constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2
HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
FPS = 60

class main_game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Devil's Dash")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)
        #放大兩倍
        self.display = pygame.Surface((HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT), pygame.SRCALPHA)
        self.display_for_outline = pygame.Surface((HALF_SCREEN_WIDTH, HALF_SCREEN_HEIGHT))
        self.display_brightness = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)
        self.temp_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT),pygame.SRCALPHA)

        self.clock = pygame.time.Clock()
        
        self.title_select_cd = 0
        self.setting_select_cd = 0
        self.craft_select_cd = 0

        self.title_select = [False,False,False]
        self.setting_select = [[True,False],[False,False],[False,False],[False,False]]
        self.setting_index = [1,1]
        self.text_counter = 0

        self.craft_select = [[True,False,False],[False,False,False],[False,False,False]]
        self.craft_index = [1,1]
        self.can_craft = [False,False,False,False,False,False]

        self.cpos_list = [[[673,600],[688,420],[658,470],[658,420],[550,210]],
                            [[700,600],[588,320],[558,470]],
                            [[700,600],[588,200]],
                            [[270,350],[620,300],[695,340],[658,200],[700,600]],
                            [[270,500]]
                        ]
        self.crad_list= [[100,100,120,100,100],
                            [200,200,200],
                            [200,200],
                            [100,200,100,200,200],
                            [150]
                        ]
        self.tpos_list = [[[543,400],[518,220],[458,270],[458,220],[750,210]],
                          [[543,300],[228,570],[358,200]],
                          [[543,300],[335,470]],
                            [[420,300],[405,570],[335,470],[335,470],[520,320]],
                            [[500,300]],
                        ]
        self.tutorial_text_list = [["Press UP to jump","Hold UP to jump higher","Touch scraps to collect them","Jump to pass the platform","Press DOWN to fast fall"],
                                   ["Press SPACE to dash","Press SPACE to dash, dashes has 1 sec cool down","Press SPACE to dash again"],
                                   ["Press Z to attack the box","Fast fall to break the box"],
                                   ["Press A to hook onto the gear","Press Z to attack the box","Press A to hook onto the gear","Hook again to change direction","Fast fall to leave earily"],
                                   ["Press X to throw the Fork, 3 sec cool down"]
                        ]

        self.assets = {
            "font": pygame.font.Font("game_testing/data/font/LXGWWenKaiMonoTC-Bold.ttf", 36),
            "font_setting": pygame.font.Font("game_testing/data/font/LXGWWenKaiMonoTC-Bold.ttf", 50),
            "pixel_font": pygame.font.Font("game_testing/data/font/pixel.otf", 70),
            "big_pixel_font": pygame.font.Font("game_testing/data/font/pixel.otf", 200),
            "small_font": pygame.font.Font("game_testing/data/font/LXGWWenKaiMonoTC-Bold.ttf", 12),
            "title": load_trans_image("title.png"),
            "title_screen": load_trans_image("標題畫面.jpg"),
            "title_start": load_trans_image("buttons/start_button.png"),
            "title_start_selected": load_trans_image("buttons/chosen_start_button.png"),
            "title_setting": load_trans_image("buttons/setting_button.png"),
            "title_setting_selected": load_trans_image("buttons/chosen_setting_button.png"),
            "title_quit":load_trans_image("buttons/quit_unchoose.png"),
            "title_quit_selected":load_trans_image("buttons/quit_choose.png"),
            "tri_right": load_trans_image("buttons/tri_1.png"),
            "tri_right_selected": load_trans_image("buttons/tri_2.png"),
            "tri_left": pygame.transform.flip(load_trans_image("buttons/tri_1.png"),True,False),
            "tri_left_selected": pygame.transform.flip(load_trans_image("buttons/tri_2.png"),True,False),
            "setting_screen":load_trans_image("setting_board.png"),

            "craft_screen":load_trans_image("craft_board.png"),
            "craftable":load_trans_scaled_image("buttons/can_select.png",0.2),
            "craftable_selected":load_trans_scaled_image("buttons/can_select_s.png",0.5),
            "uncraftable":load_trans_scaled_image("buttons/can_not_select.png",0.2),
            "uncraftable_selected":load_trans_scaled_image("buttons/can_not_select_s.png",0.5),

            "craft_back":load_trans_scaled_image("buttons/item_back.png",2),
            "crafted_back":load_trans_scaled_image("buttons/item_crafted.png",2),
            "craft_back_locked":load_trans_scaled_image("buttons/item_locked.png",2),
            "extra_can":load_trans_scaled_image("buttons/extra_can.png",0.1),
            "sword":pygame.transform.rotate(load_trans_scaled_image("sword.png",0.4),90),
            "dash":load_trans_scaled_image("fi.png",0.37), 
            "hook":load_trans_scaled_image("hook.png",6), 
            "scrap" : pygame.transform.scale(load_trans_image("entities/scrap/scrap_1.png"),(130,160)), 

            "button_background": load_trans_image("buttons/bg.png"),
            "text_box": load_image("text_box.png"),
            "head_1": pygame.transform.flip(load_trans_scaled_image("head/head.png",0.15),True,False),
            "head_2": load_trans_image("head/hong_head.png"),
            "head_1_shadow": load_trans_image("head/koakuma_shadow.png"),
            "head_2_shadow": load_trans_image("head/hong_shadow.png"),
            "music": load_trans_image("music.png"),
            "sun": load_trans_image("sun.png"),
            "decor" : load_tile("tiles/decor"),
            "stone" : load_tile("tiles/stone"),
            "grass" : load_tile("tiles/grass"),
            "large_decor" : load_trans_tile("tiles/large_decor"),
            "block" : load_fix_tile("tiles/block"),
            "player": load_image("entities/player.png"),
            "background_2": load_trans_scaled_image("back2.png",1.17),
            "background": load_trans_scaled_image("back.png",1.17),
            "enemy/idle" : Animation(load_trans_images("entities/enemy/idle"),duration=10,loop=True),
            "enemy/run" : Animation(load_trans_images("entities/enemy/run"),duration=10,loop=True),
            "enemy/jump" : Animation(load_trans_images("entities/enemy/jump"),duration=5,loop=True),
            "enemy/dash" : Animation(load_trans_images("entities/enemy/dash"),duration=4,loop=False),

            "beam/idle" : Animation(load_trans_images("entities/beam"),duration=5,loop=True),
            "scrap/idle" : Animation(load_scaled_images("entities/scrap",0.037),duration=5,loop=True),
            "box/idle" : Animation(load_scaled_images("entities/box",2),duration=5,loop=True),
            "spike/idle" : Animation(load_images("entities/spike"),duration=5,loop=True),
            "knife/idle" : Animation(load_images("entities/knife"),duration=5,loop=True),
            "trigger/idle": Animation(load_trans_images("entities/trigger"),duration=5,loop=True),
            "cut_trigger/idle" : Animation(load_trans_images("entities/trigger"),duration=5,loop=True),
            "camera_trigger/idle" : Animation(load_trans_images("entities/trigger"),duration=5,loop=True),
            "hook_start/idle": Animation(load_images("entities/hook_start"),duration=5,loop=True),
            "hook_stop/idle": Animation(load_images("entities/hook_stop"),duration=5,loop=True),

            "player/idle" : Animation(load_trans_images("entities/player/idle"),duration=10,loop=True),
            "player/run" : Animation(load_trans_images("entities/player/run"),duration=10,loop=True),
            "player/jump" : Animation(load_trans_images("entities/player/jump"),duration=5,loop=True),
            "player/attack" : Animation(load_trans_images("entities/player/attack"),duration=4,loop=False),
            "particle/leaf" : Animation(load_images("particles/leaf"),duration=20,loop=False),
            "particle/fire" : Animation(load_images("particles/fire"),duration=10,loop=False),
            "particle/particle" : Animation(load_images("particles/particle"),duration=6,loop=False),
            "particle/slash" : Animation(load_trans_scaled_images("entities/slash",0.15),duration=4,loop=False),
            "particle/hp" : Animation(load_images("particles/hp"),duration=10,loop=False),
            "projectile" : pygame.transform.flip(load_trans_image("knife.png"),True,False),
            "harpoon" : load_trans_scaled_image("harpoon.png",0.1),
            #"projectile" : pygame.transform.rotate(load_image("entities/fireball/0.png"),90),
            "fireball" : Animation(load_images("entities/fireball"),duration=10,loop=True),
            "projectile_1": load_image("projectile.png"),
            "projectile_2": load_image("projectile_orange.png"),
            "projectile_3": load_image("projectile_yellow.png"),
            "projectile_4": load_image("projectile_green.png"), 
            "projectile_5": load_image("projectile_aqua.png"),  
            "projectile_6": load_image("projectile_blue.png"),
            "projectile_7": load_image("projectile_purple.png"),
            "HP" : load_trans_image("HP.png"),
            "star" : load_trans_image("star.png"),
            #"Boss_full" : load_trans_image("max_HP_bar.png"),
            "Boss_full" : load_trans_image("new_trans_full_blood.png"),
            #"Boss_empty" : load_trans_image("empty_HP_bar.png"),
            "Boss_empty" : load_trans_image("new_trans_empty_blood.png"),
            "Boss_low" : load_trans_image("new_trans_low_warning.png"),
            #"energy_max" : load_trans_image("max_SP_bar.png"),
            "energy_max" : load_trans_image("new_trans_energy_hint.png"),
            #"energy_empty" : load_trans_image("empty_SP_bar.png"),
            "energy_empty" : load_trans_image("new_trans_empty_energy.png"),
            "retry" : load_trans_image("buttons/retry_unchoose.png"),  
            "pressed_retry" : load_trans_image("buttons/retry_choose.png"),
            "enemy_portrait_1" : load_trans_image("紅美鈴_大招立繪.png"),
            "continue" : load_trans_image("buttons/continue_1.png"),
            "pressed_continue" : load_trans_image("buttons/continue_2.png"),
            "menu" : load_trans_image("buttons/menu_1.png"),
            "pressed_menu" : load_trans_image("buttons/menu_2.png"),

        }

        self.sfx = {
            "jump" : load_sfx("jump.wav"),
            "dash" : load_sfx("dash.wav"),
            "shoot" : load_sfx("shoot.wav"),
            "hit" : load_sfx("hit.wav"),
            "got_hit" : load_sfx("player_take_damage.wav"),
            "ambience" : load_sfx("ambience.wav"),
            "swing" : load_sfx("swing.wav"),
            "coin" : load_sfx("swing.wav"),
        }   
        self.sfx["ambience"].set_volume(0.2)
        self.sfx["shoot"].set_volume(0.5)
        self.sfx["jump"].set_volume(0.7)
        self.sfx["dash"].set_volume(0.7)
        self.sfx["swing"].set_volume(0.7)
        self.sfx["coin"].set_volume(0.7)
        self.sfx["hit"].set_volume(0.8) 
        self.sfx["got_hit"].set_volume(1)

        self.bgm_factor = 0
        self.sfx_factor = 5
        self.brightness = 3


        self.level = -1

        self.scrap = 0
        self.tools = []
        self.checkpoint = 0
        self.HP_can = 0

    def load_level(self,new_level=True):
        self.enable_y_camera = False
        self.pause = False
        self.tutorial = 0
        self.tutorial_pause = False
        self.level_end = False
        self.pause_select = 0
        self.pause_select_cd = 0
        self.movements = [False,False]

        self.player = Player(self, (100,100), (8,15) , HP = self.HP_can + 1)

        self.tilemap = Tilemap(self)

        self.projectiles = []
        self.special_projectiles = [] #object [pos,direction,speed,timer,img_name]
        self.particles = []
        self.sparks = []  

        self.camera = [0,0] #camera position = offset of everything
        self.min_max_camera = [0,2700] #min and max camera x position
        self.screen_shake_timer = 0
        self.screen_shake_offset = [0,0]
        self.dead = 0 #dead animation
        self.in_cutscene = False
        self.cutscene_timer = 0

        self.tilemap.load("game_testing/"+str(self.level)+".pickle")

        self.fire_spawners = []
        self.hook_spawners = []

        for fire in self.tilemap.extract([('large_decor',8)],keep=True):
            self.fire_spawners.append(pygame.Rect(4+fire.pos[0], 4+fire.pos[1], 23, 13))

        self.enemy_spawners = []
        for spawner in self.tilemap.extract([('spawners',0),('spawners',1),('spawners',2),('spawners',3),('spawners',4),('spawners',11),
                                             ('spawners',5),('spawners',6),('spawners',7),('spawners',8),('spawners',9),('spawners',10)],keep=False):
            if spawner.variant == 0:
                self.player.position = spawner.pos #player start position
            elif spawner.variant == 1:
                self.enemy_spawners.append(Enemy(self,spawner.pos,(8,15),phase=1))
            elif spawner.variant == 2:
                self.enemy_spawners.append(Beam(self,spawner.pos,(20,144),duration=-1))
            elif spawner.variant == 3:
                self.enemy_spawners.append(Box(self,(spawner.pos[0]+2,spawner.pos[1]+2),(26,29),duration=-1))
            elif spawner.variant == 4:
                self.enemy_spawners.append(Scrap(self,(spawner.pos[0]-8,spawner.pos[1]),(12,20),duration=-1))
            elif spawner.variant == 5:
                self.enemy_spawners.append(Tutorial_trigger(self,spawner.pos,(20,144),duration=-1))
            elif spawner.variant == 6:
                self.enemy_spawners.append(Cutscene_trigger(self,spawner.pos,(20,144),duration=-1))
            elif spawner.variant == 7:
                self.enemy_spawners.append(Spike(self,spawner.pos,(16,16),duration=-1))
            elif spawner.variant == 8:
                self.enemy_spawners.append(Knife(self,spawner.pos,(32,16),duration=-1))
            elif spawner.variant == 9:
                self.hook_spawners.append(Hook_start(self,spawner.pos,(16,16),duration=-1))
            elif spawner.variant == 10:
                self.hook_spawners.append(Hook_stop(self,spawner.pos,(16,16),duration=-1))
            elif spawner.variant == 11:
                self.enemy_spawners.append(Camera_trigger(self,spawner.pos,(20,500),duration=-1))   

        sorted_objects = sorted(self.hook_spawners  , key=lambda obj: obj.position[0])
        self.hook_spawners = sorted_objects

        if self.level == 0:
            self.transition = -30
        elif self.level == 1:
            self.transition = -50
        elif self.level == -1:
            self.transition = -50
        else:
            self.transition = -50
            self.min_max_camera = [0,30000]

        self.win = 0
        self.phase_3_start = False
        if new_level:
            self.intro = True

        if self.level == -1:
            if new_level:
                pygame.mixer.music.load("game_testing/data/sfx/music_0.wav")
                pygame.mixer.music.set_volume(self.bgm_factor/5*0.2)
                pygame.mixer.music.play(-1)
        if self.level == -1:
            if new_level:
                self.in_cutscene = True
                self.text_list = ["Finally...the day has come.","Today, me, Naffin the Can, will earn FREEDOM myself","Time to escape!"]
                self.order_list = [True,True,True]
                '''
                pygame.mixer.music.load("game_testing/data/sfx/music_1.wav")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                '''
        if self.level == 0:
            self.min_max_camera = [-1000,5000]
            self.camera = [-900,0]
            if new_level:
                self.intro = False
                '''
                pygame.mixer.music.load("game_testing/data/sfx/music_1.wav")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                '''
            
        elif self.level == 1:
            self.min_max_camera = [0,5000]
            self.intro = False

        elif self.level == 2:
            self.min_max_camera = [0,5000]
            self.intro = False

        elif self.level == 3:
            self.min_max_camera = [0,5000]
            self.in_cutscene = True
            self.text_list = ["Freedom is near, I can smell it.","This should be the final challange!"]
            self.order_list = [True,True]
            self.intro = True
                

    def run_game(self):
        
        while True:
            while self.pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            self.pause = False
                            pygame.mixer.music.set_volume(self.bgm_factor/5*0.2)
                        if event.key == pygame.K_UP and self.pause_select_cd == 0:
                            self.pause_select = max(0,self.pause_select-1)
                            self.pause_select_cd = 10
                        if event.key == pygame.K_DOWN and self.pause_select_cd == 0:
                            self.pause_select = min(2,self.pause_select+1)
                            self.pause_select_cd = 10
                        if event.key == pygame.K_SPACE:
                            if self.pause_select == 0:
                                self.pause = False
                                pygame.mixer.music.set_volume(self.bgm_factor/5*0.2)
                            elif self.pause_select == 1:
                                self.pause = False
                                pygame.mixer.music.set_volume(self.bgm_factor/5*0.2)
                                self.dead = 10
                            elif self.pause_select == 2:
                                pygame.mixer.music.stop()
                                return
                    
                self.pause_select_cd = max(0,self.pause_select_cd-1)
                
                self.screen.blit(self.temp_screen, (0,0))

                self.screen.blit(self.assets['continue'], (SCREEN_WIDTH//2 - self.assets['continue'].get_width()//2, SCREEN_HEIGHT//2-150 - self.assets['continue'].get_height()//2))
                self.screen.blit(self.assets['retry'], (SCREEN_WIDTH//2 - self.assets['retry'].get_width()//2, SCREEN_HEIGHT//2 - self.assets['retry'].get_height()//2))
                self.screen.blit(self.assets['menu'], (SCREEN_WIDTH//2 - self.assets['menu'].get_width()//2, SCREEN_HEIGHT//2+150 - self.assets['menu'].get_height()//2))
                if self.pause_select == 0:
                    img = self.assets['pressed_continue']
                    self.screen.blit(img, (SCREEN_WIDTH//2 - img.get_width()//2, SCREEN_HEIGHT//2-150 - img.get_height()//2))
                elif self.pause_select == 1:
                    img = self.assets['pressed_retry']
                    self.screen.blit(img, (SCREEN_WIDTH//2 - img.get_width()//2, SCREEN_HEIGHT//2 - img.get_height()//2))
                elif self.pause_select == 2:
                    img = self.assets['pressed_menu']
                    self.screen.blit(img, (SCREEN_WIDTH//2 - img.get_width()//2, SCREEN_HEIGHT//2+150 - img.get_height()//2))
                self.screen.blit(self.display_brightness, (0, 0))
                pygame.display.update()
                self.clock.tick(FPS)

            while self.tutorial_pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if self.level == -1:
                            if event.key == pygame.K_UP and self.tutorial <= 3:
                                self.tutorial_pause = False
                                if self.tutorial == 0 or self.tutorial == 2:
                                    self.player.tutorial_jump() 
                                else:
                                    self.player.jump()
                                self.tutorial += 1
                            if event.key == pygame.K_DOWN and self.tutorial == 4:
                                self.tutorial_pause = False
                                self.player.fast_fall()
                                self.tutorial += 1
                        elif self.level == 0:   
                            if event.key == pygame.K_SPACE:
                                self.tutorial_pause = False
                                self.player.dash()
                                self.tutorial += 1
                            elif "dash" not in self.tools:
                                self.tutorial_pause = False
                                self.tutorial += 1
                        elif self.level == 1:   
                            if event.key == pygame.K_z and self.tutorial == 0:
                                self.tutorial_pause = False
                                self.player.attack()
                                self.tutorial += 1
                            if event.key == pygame.K_DOWN and self.tutorial == 1:
                                self.tutorial_pause = False
                                self.player.fast_fall()
                                self.tutorial += 1
                            elif "sword" not in self.tools:
                                self.tutorial_pause = False
                                self.tutorial += 1
                        elif self.level == 2: 
                            if "hook" not in self.tools:
                                self.tutorial_pause = False
                                self.tutorial += 1  
                            if event.key == pygame.K_z and self.tutorial == 1:
                                self.tutorial_pause = False
                                self.player.attack()
                                self.tutorial += 1
                            if event.key == pygame.K_DOWN and self.tutorial == 4:
                                self.tutorial_pause = False
                                self.player.fast_fall()
                                self.tutorial += 1
                            if event.key == pygame.K_a and self.tutorial in [0,2,3]:
                                self.tutorial_pause = False
                                self.player.hook()
                                self.tutorial += 1
                        elif self.level == 3: 
                            if "harpoon" not in self.tools:
                                self.tutorial_pause = False
                                self.tutorial += 1  
                            if event.key == pygame.K_x:
                                self.tutorial_pause = False
                                self.player.harpoon()
                                self.tutorial += 1
                self.screen.blit(self.temp_screen, (0,0))
                pygame.display.update()
                self.clock.tick(FPS)


            self.display.fill((0,0,0,0))
            if self.level <=0:
                self.display_for_outline.blit(pygame.transform.scale(self.assets['background'],(self.assets['background'].get_width()/2,self.assets['background'].get_height()/2)), (0,0))
            else:
                self.display_for_outline.blit(pygame.transform.scale(self.assets['background_2'],(self.assets['background_2'].get_width()/2,self.assets['background_2'].get_height()/2)), (0,0))
            #blit a half transparent black screen on top of the background
            decrease_light = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            decrease_light.fill((0, 0, 0, 64))  # RGBA: (0, 0, 0, 128) for half transparency
            self.display_for_outline.blit(decrease_light, (0, 0))

            if self.transition < 0:
                self.transition += 1
            if self.win>0 and not self.in_cutscene:
                self.win += 1
                pygame.mixer.music.set_volume(self.bgm_factor/5*0.2*(90-self.win)/90)
                if self.win > 90:
                    self.transition += 1
                    if self.transition > 30:
                        self.level += 1
                        if self.level == 0:
                            self.tools.append("dash_material")
                        elif self.level == 1:
                            self.tools.append("knife_material")
                        elif self.level == 2:
                            self.tools.append("hook_material")
                        elif self.level == 3:
                            self.tools.append("harpoon_material")
                        elif self.level == 4:
                            #fill black screen and "thanks for playing in the middle"
                            self.screen.fill((0,0,0))
                            text = self.assets['font'].render("Thanks for playing!", True, (255, 255, 255))
                            self.screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, SCREEN_HEIGHT//2 - text.get_height()//2))
                            while True:
                                for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                        pygame.quit()
                                        sys.exit()
                                pygame.display.update()
                                self.clock.tick(FPS)
                        self.craft_menu()
                        self.load_level()


            if self.dead > 0:
                self.dead += 1
                if self.dead >=10:
                    self.transition = min(30,self.transition+1)
                if self.dead > 40:
                    if self.level > -1:
                        self.craft_menu()

                    self.load_level(False)

            self.camera[0] += (self.player.rect().centerx - self.display.get_width()/4 -self.camera[0])/20 #camera follow player x
            if self.enable_y_camera:    
                self.camera[1] += (self.player.rect().centery - self.display.get_height()/4 -self.camera[1])/20
            else:
                self.camera[1] += (-16+self.display.get_height()/32 -self.camera[1])/20
            self.camera[0] = max(self.min_max_camera[0],self.camera[0])
            self.camera[0] = min(self.min_max_camera[1],self.camera[0])
            self.render_camera = [int(self.camera[0])+50, int(self.camera[1])]

            self.tilemap.render(self.display,offset=self.render_camera) #render background

            if self.in_cutscene == False and self.cutscene_timer == 0:
                #tutorial end
                #if self.player.position[0] > 2880 and self.level == -1 and self.win == 0:
                #    self.win = 1
                for spawner in self.fire_spawners:
                    if random.random() * 4999 < spawner.width* spawner.height:
                        pos = (spawner.x + random.random()*spawner.width, spawner.y + random.random()*spawner.height-8)
                        self.particles.append(Particle(self,'fire',pos,velocity=[-0.2,0.3],frame=random.randint(0,20)))
                
                for hook in self.hook_spawners.copy():
                    kill=hook.update((0,0),self.tilemap)
                    hook.render(self.display,offset=self.render_camera)
                    if hook.type == "hook_start" and hook.rect().colliderect(self.player.rect()) and self.player.on_hook:
                        self.player.hook_move((hook.position[0]+8,hook.position[1]+8))
                        self.hook_spawners.remove(hook)
                    elif hook.type == "hook_stop" and hook.rect().colliderect(self.player.rect()) and self.player.on_hook:
                        self.player.hook_stop()
                        self.hook_spawners.remove(hook)
                    elif kill:
                        self.hook_spawners.remove(hook)

                for enemy in self.enemy_spawners.copy():
                    kill = enemy.update((0,0),self.tilemap)
                    if enemy.render_type == "obstacle":
                        enemy.render(self.display,offset=self.render_camera)
                    if kill and enemy.type == "trigger":
                        self.enemy_spawners.remove(enemy)
                        if self.level == -1:
                            self.tutorial_pause = True
                        elif self.level == 0 and "dash" in self.tools:
                            self.tutorial_pause = True
                        elif self.level == 1 and "sword" in self.tools:
                            self.tutorial_pause = True
                        elif self.level == 2 and "hook" in self.tools:
                            self.tutorial_pause = True
                        elif self.level == 3 and "harpoon" in self.tools:
                            self.tutorial_pause = True
                    elif kill and enemy.type == "cut_trigger":
                        self.enemy_spawners.remove(enemy)
                        self.level_end = True
                        self.end_cutscene()
                    elif kill and enemy.type == "camera_trigger":
                        self.enemy_spawners.remove(enemy)
                        self.enable_y_camera = not self.enable_y_camera
                    elif kill and enemy.type == "boss":
                        self.projectiles=[] 
                        self.special_projectiles=[]
                        phase = enemy.phase
                        self.enemy_spawners.remove(enemy)
                        for i in range(4):
                            self.sparks.append(Flame((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 3+random.random()))
                            self.sparks.append(Flexible_Spark((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 3+random.random(),(255,127,0)))
                            self.sparks.append(Gold_Flame((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 2+random.random()))
                            self.sparks.append(Flexible_Spark((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 1+random.random(),(0,255,0)))
                            self.sparks.append(Ice_Flame((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 5+random.random()))
                            self.sparks.append(Flexible_Spark((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 4+random.random(),(148,0,211)))
                        if phase == 1:
                            self.enemy_spawners.append(Enemy(self,[287,145],(8,15),phase=2,action_queue=[100,"jump()",40,"frozen_in_air()",10,"air_8_shoot(1)",30,"air_8_shoot(2)",30,"air_8_shoot(1)",30,"prepare_attack()",["attack_preview()",30],5,["dash_to()",1]]))
                        elif phase == 2:
                            self.enemy_spawners.append(Enemy(self,[287,90],(8,15),phase=3,action_queue=[60,"cut_in()",60,"prepare_attack(1)",60,["spell_card()",80],90,"air_dash()",40,"frozen_in_air()",10,["spell_card()",80],90,["spread()",15],90,"prepare_attack()",["attack_preview()",30],5,["dash_to()",1]]))                
                        elif phase == 3:
                            self.win = 1
                    elif kill and enemy.type == "scrap":
                        self.enemy_spawners.remove(enemy)
                        for i in range(4):
                            self.sparks.append(Gold_Flame((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 2+random.random()))
                    elif kill:
                        self.enemy_spawners.remove(enemy)

                if not self.dead:
                    self.player.update((self.movements[1] - self.movements[0],0),self.tilemap) #update player
                    #self.player.render(self.display,offset=self.render_camera) #render player

                #[[x,y],direction,timer]
                for projectile in self.projectiles.copy():
                    if projectile[3] == "harpoon":
                        projectile[0][0] += projectile[1]
                        projectile[2] += 1
                        img = self.assets['harpoon']
                        img = pygame.transform.scale(img,(img.get_width()*0.4,img.get_height()*0.4))
                        if projectile[1] > 0:
                            self.display.blit(img,(projectile[0][0]-img.get_width()/2 -self.render_camera[0],projectile[0][1]-img.get_height()/2-self.render_camera[1]))
                        else:
                            self.display.blit(pygame.transform.flip(img, True, False),(projectile[0][0]-img.get_width()/2 -self.render_camera[0],projectile[0][1]-img.get_height()/2-self.render_camera[1]))
                        if projectile[2] > 90:
                            try:
                                self.projectiles.remove(projectile)
                            except:
                                pass
                        for enemy in self.enemy_spawners:
                            if enemy.rect().colliderect(pygame.Rect(projectile[0][0]-16,projectile[0][1]-16,32,32)) and enemy.type == "box":
                                enemy.HP -= 1
                                self.sfx['hit'].play()
                                for i in range(10):
                                    angle = random.random()*math.pi*2
                                    speed = random.random() *5
                                    self.sparks.append(Gold_Flame(enemy.rect().center,angle,2+random.random()))  
                                    self.particles.append(Particle(self,'particle',enemy.rect().center,[math.cos(angle+math.pi)*speed*0.5,math.sin(angle+math.pi)*speed*0.5],frame=random.randint(0,7)))  
                                self.sparks.append(Gold_Flame(enemy.rect().center, 0, 5+random.random()))
                    else:
                        projectile[0][0] += projectile[1]
                        projectile[2] += 1
                        img = self.assets['projectile']
                        #img = pygame.transform.scale(img,(img.get_width()//8,img.get_height()//8))
                        if projectile[1] > 0:
                            self.display.blit(img,(projectile[0][0]-img.get_width()/2 -self.render_camera[0],projectile[0][1]-img.get_height()/2-self.render_camera[1]))
                        else:
                            self.display.blit(pygame.transform.flip(img, True, False),(projectile[0][0]-img.get_width()/2 -self.render_camera[0],projectile[0][1]-img.get_height()/2-self.render_camera[1]))
                        '''
                        if self.tilemap.solid_check(projectile[0]):
                            try:
                                self.projectiles.remove(projectile) 
                            except:
                                pass
                            for i in range(4):
                                self.sparks.append(Spark(projectile[0],random.random()*math.pi*2,2+random.random()))
                        '''
                        if projectile[2] > 360:
                            try:
                                self.projectiles.remove(projectile)
                            except:
                                pass
                        else:
                            if self.player.rect().collidepoint(projectile[0]) or self.player.rect().collidepoint([projectile[0][0],projectile[0][1]+8]) or self.player.rect().collidepoint([projectile[0][0],projectile[0][1]+16]):
                                try:
                                    self.projectiles.remove(projectile)
                                except:
                                    pass
                                self.player.take_damage(1,(list(self.player.rect().center).copy()[0]-projectile[0][0],0))
                for special_projectile in self.special_projectiles.copy():
                    special_projectile.update()
                    
                    img = self.assets[special_projectile.img_name]
                    #rotate image according to its direction which is a vector
                    angle = math.atan2(special_projectile.direction[1],special_projectile.direction[0]) * 180 / math.pi
                    #img = pygame.transform.rotate(img,-1*angle)
                    self.display.blit(img,(special_projectile.pos[0]-img.get_width()/2 -self.render_camera[0],special_projectile.pos[1]-img.get_height()/2-self.render_camera[1]))
                    if self.tilemap.solid_check(special_projectile.pos):
                        if special_projectile.reverse():
                            try:
                                self.special_projectiles.remove(special_projectile)
                            except:
                                pass
                        for i in range(4):
                            #match the spark's color with the projectile
                            if special_projectile.img_name == 'projectile_1':
                                self.sparks.append(Flame(special_projectile.pos,random.random()*math.pi*2,2+random.random()))
                            elif special_projectile.img_name == 'projectile_2':
                                self.sparks.append(Flexible_Spark(special_projectile.pos,random.random()*math.pi*2,2+random.random(),(255,127,0)))
                            elif special_projectile.img_name == 'projectile_3':
                                self.sparks.append(Gold_Flame(special_projectile.pos,random.random()*math.pi*2,2+random.random()))
                            elif special_projectile.img_name == 'projectile_4':
                                self.sparks.append(Flexible_Spark(special_projectile.pos,random.random()*math.pi*2,2+random.random(),(0,255,0)))
                            elif special_projectile.img_name == 'projectile_5':
                                self.sparks.append(Ice_Flame(special_projectile.pos,random.random()*math.pi*2,2+random.random()))
                            elif special_projectile.img_name == 'projectile_6':
                                self.sparks.append(Flexible_Spark(special_projectile.pos,random.random()*math.pi*2,2+random.random(),(148,0,211)))
                            elif special_projectile.img_name == 'projectile_7':
                                self.sparks.append(Flexible_Spark(special_projectile.pos,random.random()*math.pi*2,2+random.random(),(255,0,255)))
                            else:
                                self.sparks.append(Spark(special_projectile.pos,random.random()*math.pi*2,2+random.random()))   
                    elif special_projectile.timer > 360:
                        try:
                            self.special_projectiles.remove(special_projectile) 
                        except:
                            pass    
                    elif abs(self.player.dashing) < 50: 
                        if self.player.rect().collidepoint(special_projectile.pos):
                            try:
                                self.special_projectiles.remove(special_projectile)
                            except:
                                pass
                            self.player.take_damage(1,(list(self.player.rect().center).copy()[0]-special_projectile.pos[0],0))

                for spark in self.sparks.copy():
                    kill = spark.update()
                    spark.render(self.display,offset=self.render_camera)
                    if kill:
                        self.sparks.remove(spark)   

                display_mask = pygame.mask.from_surface(self.display)
                display_sillouette = display_mask.to_surface(setcolor=(0,0,0,180),unsetcolor=(0,0,0,0))
                #outline stuff but I dont like it
                #for offset in [[-1,0],[1,0],[0,1],[0,-1]]:
                #    self.display_for_outline.blit(display_sillouette,offset)
                
                for particle in self.particles.copy():
                    kill = particle.update()
                    if particle.p_type == 'fire':
                        particle.pos[0] += math.sin(particle.animation.frame*0.035)*0.3
                    particle.render(self.display,offset=self.render_camera)
                    if kill:
                        self.particles.remove(particle)
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            self.movements[0] = True
                        if event.key == pygame.K_RIGHT:
                            self.movements[1] = True
                        if event.key == pygame.K_j or event.key == pygame.K_UP:
                            if not self.player.on_hook:
                                self.player.jump()
                        if event.key == pygame.K_x:
                            if not self.player.on_hook and "harpoon" in self.tools:
                                self.player.harpoon()
                        if event.key == pygame.K_k or event.key == pygame.K_DOWN:
                            self.player.fast_fall()
                        if event.key == pygame.K_SPACE:
                            if not self.player.on_hook and "dash" in self.tools:
                                self.player.dash()
                        if event.key == pygame.K_a:
                            if "hook" in self.tools:
                                self.player.hook()
                        if event.key == pygame.K_z: 
                            if "sword" in self.tools:
                                self.player.attack()
                        if event.key == pygame.K_p:
                            self.pause = True
                            #self.tutorial_pause = True
                            self.movements = [False,False]  
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_LEFT:
                            self.movements[0] = False
                        if event.key == pygame.K_RIGHT:
                            self.movements[1] = False
                        if event.key == pygame.K_j  or event.key == pygame.K_UP:
                            self.player.stop_jump()

                #player keeps move right
                if self.player.harpoon_counter < 1920 and not self.level_end and not self.player.on_hook:
                    self.movements[1] = True
                elif self.player.on_hook:   
                    self.movements[1] = False   
    

                self.screen_shake_timer = max(0,self.screen_shake_timer-1)
                self.screen_shake_offset = [random.randint(-self.screen_shake_timer,self.screen_shake_timer),random.randint(-self.screen_shake_timer,self.screen_shake_timer)]  
            
            if not self.in_cutscene:
                for i in range(self.player.HP):
                    self.display_for_outline.blit(self.assets['HP'],(i*18,10))
                self.display_for_outline.blit(pygame.transform.scale(self.assets['scrap'],(25,25)),(0,30))

                
                
            
            self.display_for_outline.blit(self.display, (0,0))
            
            self.screen.blit(pygame.transform.scale(self.display_for_outline, (2*SCREEN_WIDTH, 2*SCREEN_HEIGHT)), self.screen_shake_offset) 
            
            #blit self.display_entity to screen without scaling
            #if not self.dead and abs(self.player.dashing) < 50:
            if not self.dead:
                self.player.render_new(self.screen,offset=self.render_camera) #render player
                if not self.in_cutscene:
                    scrap_text = " x " + str(self.scrap)
                    text_font = self.assets["font"].render(scrap_text, True, (255,255,255))
                    self.screen.blit(text_font, (70,145))

            if not self.in_cutscene:
                
                for enemy in self.enemy_spawners:
                    if enemy.render_type != "obstacle":
                        enemy.render_new(self.screen,offset=self.render_camera)
                    
                    if enemy.type == 'boss':
                        for i in range(4-enemy.phase):
                            img = self.assets['star']
                            img = pygame.transform.scale(img,(img.get_width()*4,img.get_height()*4))
                            self.screen.blit(img,(1150-i*80,90))
                        if enemy.phase != 3 and enemy.HP < enemy.max_HP:
                            ratio = enemy.HP/enemy.max_HP
                            pygame.draw.rect(self.screen,(255,0,0),(847+376*(1-ratio),171,376*ratio,20))
                            if ratio < 0.4:
                                img = self.assets['Boss_low']
                            else:
                                img = self.assets['Boss_empty']
                            img = pygame.transform.scale(img,(58*8,12*8))
                            self.screen.blit(pygame.transform.flip(img,True,True),(800,130))
                        elif enemy.phase == 3 and enemy.timer_HP < enemy.max_HP:
                            ratio = enemy.timer_HP/enemy.max_HP
                            #orange
                            pygame.draw.rect(self.screen,(255,127,0),(847+376*(1-ratio),171,376*ratio,20))
                            if ratio < 0.4:
                                img = self.assets['Boss_low']
                            else:
                                img = self.assets['Boss_empty']
                            img = pygame.transform.scale(img,(58*8,12*8))
                            self.screen.blit(pygame.transform.flip(img,True,True),(800,130))
                        else:
                            img = self.assets['Boss_full']
                            img = pygame.transform.scale(img,(58*8,12*8))
                            self.screen.blit(pygame.transform.flip(img,True,True),(800,130))
                
            if self.cutscene_timer > 0:    
                self.cutscene_timer -= 1
                decrease_light = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                decrease_light.fill((0, 0, 0, 150))  # RGBA: (0, 0, 0, 128) for half transparency
                self.screen.blit(decrease_light, (0, 0))
                if self.cutscene_timer >= 100:
                    #if self.cutscene_timer > 100
                    self.cutscene_timer -= 0
                    x = 960 + (740-960) * (self.cutscene_timer - 120)/ (100-120)-HALF_SCREEN_WIDTH
                    y = 0 + (405-0) * (self.cutscene_timer - 120)/ (100-120)-HALF_SCREEN_HEIGHT
                    self.screen.blit(pygame.transform.scale(self.assets["enemy_portrait_1"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(x,y))
                    #self.screen.blit(pygame.transform.scale(self.assets["enemy_portrait_1"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(self.cutscene_timer*16-1120-HALF_SCREEN_WIDTH,self.cutscene_timer*-48+5760-HALF_SCREEN_HEIGHT))
                elif self.cutscene_timer >= 20:
                    x = 740 + (540-740) * (self.cutscene_timer - 100)/ (20-100)-HALF_SCREEN_WIDTH
                    y = 405 + (555-405) * (self.cutscene_timer - 100)/ (20-100)-HALF_SCREEN_HEIGHT
                    self.screen.blit(pygame.transform.scale(self.assets["enemy_portrait_1"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(x,y))
                    #self.screen.blit(pygame.transform.scale(self.assets["enemy_portrait_1"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(0,0))
                else:
                    self.cutscene_timer -= 1
                    x = 540 + 2*(320-540) * (self.cutscene_timer - 20)/ (0-20)-HALF_SCREEN_WIDTH
                    y = 555 + 2*(960-555) * (self.cutscene_timer - 20)/ (0-20)-HALF_SCREEN_HEIGHT
                    self.screen.blit(pygame.transform.scale(self.assets["enemy_portrait_1"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(x,y))
                    #self.screen.blit(pygame.transform.scale(self.assets["enemy_portrait_1"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(self.cutscene_timer*16+480-HALF_SCREEN_WIDTH,self.cutscene_timer*-48+960-HALF_SCREEN_HEIGHT))
                if self.cutscene_timer == 0:
                    self.in_cutscene = False
                    self.phase_3_start = True

            if self.transition:
                tran_surf=pygame.Surface(self.display.get_size())
                pygame.draw.circle(tran_surf,(255,255,255),(self.display.get_width()//4,self.display.get_height()//4),(30-abs(self.transition))*8)
                tran_surf.set_colorkey((255,255,255))
                self.display.blit(tran_surf,(0,0))
                self.screen.blit(pygame.transform.scale(self.display, (2*SCREEN_WIDTH, 2*SCREEN_HEIGHT)), (0,0)) 


            if self.pause:
                #pause screen: blit a half transparent black screen
                pause_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pause_screen.fill((0, 0, 0, 128))  # RGBA: (0, 0, 0, 128) for half transparency
                self.screen.blit(pause_screen, (0, 0))
                self.pause_select = 0
                self.temp_screen = self.screen.copy()
                pygame.mixer.music.set_volume(self.bgm_factor/5*0.1)

            if self.tutorial_pause:
                #pause screen: blit a half transparent black screen
                pause_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                pause_text = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                pause_screen.fill((0, 0, 0, 128))  # RGBA: (0, 0, 0, 128) for half transparency
                pause_text.fill((255,255,255))
                pause_text.set_colorkey((255,255,255))
                circle_pos = self.cpos_list[self.level+1][self.tutorial]
                circle_radius = self.crad_list[self.level+1][self.tutorial]
                pygame.draw.circle(pause_screen,(255,255,255),circle_pos,circle_radius)
                pause_screen.set_colorkey((255,255,255))
                self.screen.blit(pygame.transform.scale(self.display, (2*SCREEN_WIDTH, 2*SCREEN_HEIGHT)), (0,0)) 
                self.screen.blit(pause_screen, (0, 0))
                text_pos = self.tpos_list[self.level+1][self.tutorial]
                text = self.tutorial_text_list[self.level+1][self.tutorial]
                text_font = self.assets["font"].render(text, True, (0,200,255))
                self.screen.blit(text_font, text_pos)
                self.temp_screen = self.screen.copy()

            if self.in_cutscene == True and not self.transition: 
                speed = 3
                #blit the text box at the buttom of the screen
                if not self.order_list[0]:
                    self.screen.fill((0,0,0))
                self.screen.blit(pygame.transform.scale(self.assets["text_box"], (SCREEN_WIDTH, SCREEN_HEIGHT//4)),(0,3*SCREEN_HEIGHT//4))
                #blit headd_1 at the left of the text box while scale it up to 2x
                if not self.order_list[0]:
                    pass

                else:
                    img= self.assets["head_1"].copy()
                    self.screen.blit(pygame.transform.scale(pygame.transform.flip(img,True,False),(self.assets["head_1"].get_width()*1.8,self.assets["head_1"].get_height()*1.8-3)),(10,3*SCREEN_HEIGHT//4+7))
                #blit the text using font in the assets
                if self.text_list:
                    text = self.text_list[0]
                    if self.text_counter < len(text)*speed:
                        self.text_counter += 1
                    elif self.text_counter >= speed*len(text):
                        pass
                    snip = text[0:self.text_counter//speed]
                    text_font = self.assets["font"].render(snip, True, (255,255,255))
                    self.screen.blit(text_font, (SCREEN_WIDTH//4, 3*SCREEN_HEIGHT//4 + SCREEN_HEIGHT//8 - text_font.get_height()//2))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.text_list.pop(0)
                            self.order_list.pop(0)
                            self.text_counter = 0
                            if not self.text_list:
                                self.in_cutscene = False
                                if not self.intro :
                                    self.win = 1
                                self.intro = False

            self.screen.blit(self.display_brightness, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

    def first_phase_cutscene(self):
        self.in_cutscene = True
        self.text_list = ["原來是小惡魔啊，還以為是入侵者呢（呵欠","......zzz...zzz","竟然睡回去了......","算了，趕快進屋吧"]
        self.order_list = [False,False,True,True]

    def end_cutscene(self):
        self.movements = [False,False]
        if self.level == -1:
            self.tutorial_cutscene()
        elif self.level == 0:
            self.in_cutscene = True
            self.text_list = ["A broken knife?","Looks like it could break those boxes","*Obtain broken knife*"]
            self.order_list = [True,True,True]
        elif self.level == 1:
            self.in_cutscene = True
            self.text_list = ["A can-size grappling hook?","This place is weird","*Obtain grappling hook*"]
            self.order_list = [True,True,True]
        elif self.level == 2:
            self.in_cutscene = True
            self.text_list = ["Hmm...","I already got the knife","Maybe I should take the fork as well","*Obtain fork*"]
            self.order_list = [True,True,True,True]
        elif self.level == 3:
            self.in_cutscene = True
            self.text_list = ["The door is right there!","There's notning can stop me now!","Freedom!","......","*crack*","......"]
            self.order_list = [True,True,True,False,False,False]

    def tutorial_cutscene(self):
        self.in_cutscene = True
        self.text_list = ["Hmm... a lighter?","This might help me with the escape","*Obtain Lighter*","*Unlocked Craft Menu*"]
        self.order_list = [True,True,True,True]

    def run_main_menu(self):
        pygame.mixer.music.load("game_testing/data/sfx/Raise_the_Flag_of_Cheating.wav")
        pygame.mixer.music.set_volume(self.bgm_factor/5*0.3)
        pygame.mixer.music.play(-1)
        while True:
            #blit the title screen and scale it to the screen size
            self.screen.blit(pygame.transform.scale(self.assets["background"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(0,0))
            self.screen.fill((0,0,0))
            #blit "Naffin-Can /n go RUN" at the middle of the screen using font, with "Can" being gray and "RUN" being red
            #color for blue?

            text_font = self.assets["big_pixel_font"].render("Naff", True, (0,0,255))
            self.screen.blit(text_font, (SCREEN_WIDTH//4-150, SCREEN_HEIGHT//4))
            text_font = self.assets["big_pixel_font"].render("fin", True, (0,255,0))
            self.screen.blit(text_font, (SCREEN_WIDTH//4+200, SCREEN_HEIGHT//4))
            text_font = self.assets["big_pixel_font"].render("-", True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH//4+450, SCREEN_HEIGHT//4))
            text_font = self.assets["big_pixel_font"].render("Can", True, (100,100,100))
            self.screen.blit(text_font, (SCREEN_WIDTH//4 + 570, SCREEN_HEIGHT//4))
            text_font = self.assets["big_pixel_font"].render("go", True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH//4 + 50, SCREEN_HEIGHT//4+200))
            text_font = self.assets["big_pixel_font"].render("RUN!", True, (255,0,0))
            self.screen.blit(text_font, (SCREEN_WIDTH//4 + 300, SCREEN_HEIGHT//4+200))

            #blit "Press space to start" at the bottom of the screen using font
            text_font = self.assets["font"].render("Press space to start", True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH//4 + 120, SCREEN_HEIGHT//4+500))
            
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for i in range(60):
                            decrease_light = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                            decrease_light.fill((0, 0, 0, 10))  # RGBA: (0, 0, 0, 128) for half transparency
                            self.screen.blit(decrease_light, (0, 0))
                            pygame.mixer.music.set_volume(self.bgm_factor/5*0.3*i/60)
                            self.clock.tick(60)
                            self.screen.blit(self.display_brightness, (0, 0))
                            pygame.display.flip()
                        self.level = -1
                        self.load_level()
                        self.run_game()
                        pygame.mixer.music.load("game_testing/data/sfx/Raise_the_Flag_of_Cheating.wav")
                        pygame.mixer.music.set_volume(self.bgm_factor/5*0.3)
                        pygame.mixer.music.play(-1)
                    if event.key == pygame.K_e:
                        self.craft_menu()
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0 and self.title_select[0]:  
                        for i in range(100):
                            decrease_light = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA).copy()
                            decrease_light.fill((0, 0, 0, 5))  # RGBA: (0, 0, 0, 128) for half transparency
                            self.screen.blit(decrease_light, (0, 0))
                            pygame.mixer.music.set_volume(self.bgm_factor/5*0.3*(60-i)/60)
                            self.clock.tick(60)
                            if not i:
                                self.screen.blit(self.display_brightness, (0, 0))
                            pygame.display.flip()
                        self.load_level()
                        self.run_game()
                        pygame.mixer.music.load("game_testing/data/sfx/Raise_the_Flag_of_Cheating.wav")
                        pygame.mixer.music.set_volume(self.bgm_factor/5*0.3)
                        pygame.mixer.music.play(-1)
                    elif event.button == 0 and self.title_select[2]:
                        self.run_setting()
                    elif event.button == 0 and self.title_select[1]:
                        pygame.quit()
                if event.type == pygame.JOYAXISMOTION:
                    #THERE IS A BUG WITH COUNTING ISSUE WHICH RESULT IN THE ORDER BEING 1 3 2, DO NOT TRY TO FIX IT
                    if event.axis == 1:
                        if event.value < -0.5 and self.title_select_cd == 0:
                            if self.title_select[0]:
                                self.title_select[0] = False
                                self.title_select[1] = True
                            elif self.title_select[1]:
                                self.title_select[1] = False
                                self.title_select[2] = True
                            else:
                                self.title_select[2] = False
                                self.title_select[0] = True
                            self.title_select_cd = 10
                        elif event.value > 0.5 and self.title_select_cd == 0:
                            if self.title_select[0]:
                                self.title_select[0] = False
                                self.title_select[2] = True
                            elif self.title_select[2]:
                                self.title_select[2] = False
                                self.title_select[1] = True
                            else:
                                self.title_select[1] = False
                                self.title_select[0] = True
                            self.title_select_cd = 10
            self.title_select_cd = max(0,self.title_select_cd-1)
            self.screen.blit(self.display_brightness, (0, 0))
            pygame.display.flip()
    def run_setting(self):
        self.setting_select = [[True,False],[False,False],[False,False],[False,False]]
        self.setting_index = [1,1]
        decrease_light = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        decrease_light.fill((0, 0, 0, 128))  # RGBA: (0, 0, 0, 128) for half transparency
        self.screen.blit(decrease_light, (0, 0))

        self.temp_screen = self.screen.copy()

        while True:
            self.setting_select_cd = max(0,self.setting_select_cd-1)
            self.screen.blit(self.temp_screen, (0,0))
            #blit setting_bg in the middle of the screen
            #self.screen.blit(pygame.transform.scale(self.assets["setting_screen"], (2*SCREEN_WIDTH/3, 2*SCREEN_HEIGHT/3)),(SCREEN_WIDTH/6, SCREEN_HEIGHT/6))
            self.screen.blit(pygame.transform.scale(self.assets["setting_screen"], (7*SCREEN_WIDTH/8, 12*SCREEN_HEIGHT/8)),(SCREEN_WIDTH/16-40, SCREEN_HEIGHT/16-300))
            
            
            text_font = self.assets["font_setting"].render("BGM音量", True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH/3-120, SCREEN_HEIGHT/6+100))
            self.screen.blit(pygame.transform.scale(self.assets["music"], (50,50)),(SCREEN_WIDTH/3+90, SCREEN_HEIGHT/6+105))
            text = str(self.bgm_factor)
            text_font = self.assets["font_setting"].render(text, True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH/3+335, SCREEN_HEIGHT/6+95))

            text_font = self.assets["font_setting"].render("SFX音量", True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH/3-120, SCREEN_HEIGHT/6+250))
            self.screen.blit(pygame.transform.scale(self.assets["music"], (50,50)),(SCREEN_WIDTH/3+90, SCREEN_HEIGHT/6+255))
            text = str(self.sfx_factor)
            text_font = self.assets["font_setting"].render(text, True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH/3+335, SCREEN_HEIGHT/6+250))

            text_font = self.assets["font_setting"].render("畫面亮度", True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH/3-130, SCREEN_HEIGHT/6+400))
            self.screen.blit(pygame.transform.scale(self.assets["sun"], (50,50)),(SCREEN_WIDTH/3+95, SCREEN_HEIGHT/6+405))
            text = str(self.brightness)
            text_font = self.assets["font_setting"].render(text, True, (255,255,255))
            self.screen.blit(text_font, (SCREEN_WIDTH/3+335, SCREEN_HEIGHT/6+400))

            if self.setting_select[0][0]:
                self.screen.blit(pygame.transform.scale(self.assets["tri_left_selected"], (50,50)),(SCREEN_WIDTH/3+200, SCREEN_HEIGHT/6+100))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["tri_left"], (50,50)),(SCREEN_WIDTH/3+200, SCREEN_HEIGHT/6+100))
            if self.setting_select[0][1]:
                self.screen.blit(pygame.transform.scale(self.assets["tri_right_selected"], (50,50)),(SCREEN_WIDTH/3+450, SCREEN_HEIGHT/6+100))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["tri_right"], (50,50)),(SCREEN_WIDTH/3+450, SCREEN_HEIGHT/6+100))
            if self.setting_select[1][0]:
                self.screen.blit(pygame.transform.scale(self.assets["tri_left_selected"], (50,50)),(SCREEN_WIDTH/3+200, SCREEN_HEIGHT/6+250))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["tri_left"], (50,50)),(SCREEN_WIDTH/3+200, SCREEN_HEIGHT/6+250))
            if self.setting_select[1][1]:
                self.screen.blit(pygame.transform.scale(self.assets["tri_right_selected"], (50,50)),(SCREEN_WIDTH/3+450, SCREEN_HEIGHT/6+250))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["tri_right"], (50,50)),(SCREEN_WIDTH/3+450, SCREEN_HEIGHT/6+250))
            if self.setting_select[2][0]:
                self.screen.blit(pygame.transform.scale(self.assets["tri_left_selected"], (50,50)),(SCREEN_WIDTH/3+200, SCREEN_HEIGHT/6+400))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["tri_left"], (50,50)),(SCREEN_WIDTH/3+200, SCREEN_HEIGHT/6+400))
            if self.setting_select[2][1]:
                self.screen.blit(pygame.transform.scale(self.assets["tri_right_selected"], (50,50)),(SCREEN_WIDTH/3+450, SCREEN_HEIGHT/6+400))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["tri_right"], (50,50)),(SCREEN_WIDTH/3+450, SCREEN_HEIGHT/6+400))
            if self.setting_select[3][0] or self.setting_select[3][1]:
                self.screen.blit(self.assets["pressed_menu"],(SCREEN_WIDTH/2-200, 4*SCREEN_HEIGHT/6-100))
            else:
                self.screen.blit(self.assets["menu"],(SCREEN_WIDTH/2-200, 4*SCREEN_HEIGHT/6-100))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return
                    if event.key == pygame.K_RETURN:
                        if self.setting_select[3][0] or self.setting_select[3][1]:
                            return
                        elif self.setting_select[0][0]:
                            self.bgm_factor = max(0,self.bgm_factor-1)
                        elif self.setting_select[0][1]:
                            self.bgm_factor = min(10,self.bgm_factor+1)
                        elif self.setting_select[1][0]:
                            self.sfx_factor = max(0,self.sfx_factor-1)
                        elif self.setting_select[1][1]:
                            self.sfx_factor = min(10,self.sfx_factor+1)
                        elif self.setting_select[2][0]:
                            self.brightness = max(0,self.brightness-1)
                        elif self.setting_select[2][1]:
                            self.brightness = min(3,self.brightness+1) 
                    if event.key == pygame.K_LEFT:
                        if self.setting_index[0]==0 and self.setting_index[1]==0:
                            self.setting_index=[1,1]
                        elif self.setting_select_cd == 0:
                            self.setting_index[1] = max(self.setting_index[1]-1,1)
                            self.setting_select=[[False,False],[False,False],[False,False],[False,False]]
                            self.setting_select[self.setting_index[0]-1][self.setting_index[1]-1] = True
                            self.setting_select_cd = 10
                    if event.key == pygame.K_RIGHT:
                        if self.setting_index[0]==0 and self.setting_index[1]==0:
                            self.setting_index=[1,1]
                        elif self.setting_select_cd == 0:
                            self.setting_index[1] = min(self.setting_index[1]+1,2)
                            self.setting_select=[[False,False],[False,False],[False,False],[False,False]]
                            self.setting_select[self.setting_index[0]-1][self.setting_index[1]-1] = True
                            self.setting_select_cd = 10
                    if event.key == pygame.K_UP:
                        if self.setting_index[0]==0 and self.setting_index[1]==0:
                            self.setting_index=[1,1]
                        elif self.setting_select_cd == 0:
                            self.setting_index[0] = max(self.setting_index[0]-1,1)      
                            self.setting_select=[[False,False],[False,False],[False,False],[False,False]]
                            self.setting_select[self.setting_index[0]-1][self.setting_index[1]-1] = True
                            self.setting_select_cd = 10
                    if event.key == pygame.K_DOWN:
                        if self.setting_index[0]==0 and self.setting_index[1]==0:
                            self.setting_index=[1,1]
                        elif self.setting_select_cd == 0:
                            self.setting_index[0] = min(self.setting_index[0]+1,4)
                            self.setting_select=[[False,False],[False,False],[False,False],[False,False]]
                            self.setting_select[self.setting_index[0]-1][self.setting_index[1]-1] = True
                            self.setting_select_cd = 10

                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if self.setting_select[3][0] or self.setting_select[3][1]:
                            return
                        elif self.setting_select[0][0]:
                            self.bgm_factor = max(0,self.bgm_factor-1)
                        elif self.setting_select[0][1]:
                            self.bgm_factor = min(10,self.bgm_factor+1)
                        elif self.setting_select[1][0]:
                            self.sfx_factor = max(0,self.sfx_factor-1)
                        elif self.setting_select[1][1]:
                            self.sfx_factor = min(10,self.sfx_factor+1)
                        elif self.setting_select[2][0]:
                            self.brightness = max(0,self.brightness-1)
                        elif self.setting_select[2][1]:
                            self.brightness = min(3,self.brightness+1) 
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 1 and self.setting_select_cd == 0:
                        if self.setting_index[0]==0 and self.setting_index[1]==0:
                            self.setting_index=[1,1]
                        elif event.value < -0.5 and self.setting_select_cd == 0:
                            self.setting_index[0] = max(self.setting_index[0]-1,1)
                        elif event.value > 0.5 and self.setting_select_cd == 0:
                            self.setting_index[0] = min(self.setting_index[0]+1,4)
                        if abs(event.value) > 0.5:
                            self.setting_select=[[False,False],[False,False],[False,False],[False,False]]
                            self.setting_select[self.setting_index[0]-1][self.setting_index[1]-1] = True
                            self.setting_select_cd = 10
                    if event.axis == 0 and self.setting_select_cd == 0:
                        if self.setting_index[0]==0 and self.setting_index[1]==0:
                            self.setting_index=[1,1]
                        elif event.value < -0.5 and self.setting_select_cd == 0:
                            self.setting_index[1] = max(self.setting_index[1]-1,1)
                        elif event.value > 0.5 and self.setting_select_cd == 0:
                            self.setting_index[1] = min(self.setting_index[1]+1,2)
                        if abs(event.value) > 0.5:
                            self.setting_select=[[False,False],[False,False],[False,False],[False,False]]
                            self.setting_select[self.setting_index[0]-1][self.setting_index[1]-1] = True
                            self.setting_select_cd = 10
            #setting
            pygame.mixer.music.set_volume(self.bgm_factor/5*0.3)
            self.sfx["ambience"].set_volume(0.2*self.sfx_factor/5)
            self.sfx["shoot"].set_volume(0.5*self.sfx_factor/5)
            self.sfx["jump"].set_volume(0.7*self.sfx_factor/5)
            self.sfx["dash"].set_volume(0.7*self.sfx_factor/5)
            self.sfx["swing"].set_volume(0.7*self.sfx_factor/5)
            self.sfx["hit"].set_volume(0.8*self.sfx_factor/5) 
            self.sfx["got_hit"].set_volume(1*self.sfx_factor/5)
            self.clock.tick(FPS)
            self.display_brightness.fill((0, 0, 0, 40*(3-self.brightness)))  # RGBA: (0, 0, 0, 128) for half transparency
            self.screen.blit(self.display_brightness, (0, 0))
            pygame.display.flip()
    
    def craft_menu(self):
        self.transition = -50
        self.craft_select=[[True,False,False],[False,False,False],[False,False,False]]
        self.craft_index = [1,1]
        decrease_light = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        decrease_light.fill((0, 0, 0, 128))  # RGBA: (0, 0, 0, 128) for half transparency
        self.screen.blit(decrease_light, (0, 0))

        self.temp_screen = self.screen.copy()

        while True:
            self.craft_select_cd = max(0,self.craft_select_cd-1)
            self.screen.blit(self.temp_screen, (0,0))
            #blit setting_bg in the middle of the screen
            #self.screen.blit(pygame.transform.scale(self.assets["setting_screen"], (2*SCREEN_WIDTH/3, 2*SCREEN_HEIGHT/3)),(SCREEN_WIDTH/6, SCREEN_HEIGHT/6))
            self.screen.blit(pygame.transform.scale(self.assets["craft_screen"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(0,0))

            #check which item can be craft

            can = self.HP_can
            if self.scrap >= 10 and not can:
                self.can_craft[0] = True
            elif self.scrap >= 30 and can == 1:
                self.can_craft[0] = True
            elif self.scrap >= 50 and can == 2:
                self.can_craft[0] = True
            elif self.scrap >= 100 and can == 3:
                self.can_craft[0] = True
            else:
                self.can_craft[0] = False

            if "dash_material" in self.tools and self.scrap >= 50:
                self.can_craft[1] = True
            else:
                self.can_craft[1] = False

            if "shield_material" in self.tools and self.scrap >= 50:
                self.can_craft[2] = True
            else:
                self.can_craft[2] = False

            if "hook_material" in self.tools and self.scrap >= 70:
                self.can_craft[3] = True
            else:
                self.can_craft[3] = False

            if "sword_material" in self.tools and self.scrap >= 70:
                self.can_craft[4] = True
            else:
                self.can_craft[4] = False

            if "harpoon_material" in self.tools and self.scrap >= 100:
                self.can_craft[5] = True
            else:
                self.can_craft[5] = False
            
            #etra text at the buttom
            extra_text = " Missing material"
            
            cost = 10
            if self.craft_select[0][0]:
                t = str(self.HP_can)
                if self.HP_can == 0:
                    cost = 10
                elif self.HP_can == 1:
                    cost = 30
                elif self.HP_can == 2:
                    cost = 50
                elif self.HP_can == 3:
                    cost = 100
                else:
                    cost = 0
                extra_text = " (" + t + "/4 obtained)"
                if self.can_craft[0]:
                    self.screen.blit(self.assets["craftable_selected"],(-10,210))
                else:
                    self.screen.blit(self.assets["uncraftable_selected"],(-10,210))
            else:
                if self.can_craft[0]:
                    self.screen.blit(self.assets["craftable"],(-10,210))
                else:
                    self.screen.blit(self.assets["uncraftable"],(-10,210))
            if self.craft_select[0][1]:
                if "dash" not in self.tools:
                    cost = 50 
                    extra_text = ""
                else:
                    cost = 0
                    extra_text = " Press SPACE to dash"
                if self.can_craft[1]:
                    self.screen.blit(self.assets["craftable_selected"],(445,210))
                else:
                    self.screen.blit(self.assets["uncraftable_selected"],(445,210))
            else:
                if self.can_craft[1]:
                    self.screen.blit(self.assets["craftable"],(445,210))
                else:
                    self.screen.blit(self.assets["uncraftable"],(445,210))
            if self.craft_select[0][2]:
                cost = 50 if self.level >= 1 else 0
                if self.can_craft[2]:
                    self.screen.blit(self.assets["craftable_selected"],(900,210))
                else:
                    self.screen.blit(self.assets["uncraftable_selected"],(900,210))
            else:
                if self.can_craft[2]:
                    self.screen.blit(self.assets["craftable"],(900,210))
                else:
                    self.screen.blit(self.assets["uncraftable"],(900,210))
            if self.craft_select[1][0]:
                cost = 70 if self.level >= 2 else 0
                if self.can_craft[3]:
                    self.screen.blit(self.assets["craftable_selected"],(-10,620))
                else:
                    self.screen.blit(self.assets["uncraftable_selected"],(-10,620))
            else:
                if self.can_craft[3]:
                    self.screen.blit(self.assets["craftable"],(-10,620))
                else:
                    self.screen.blit(self.assets["uncraftable"],(-10,620))
            if self.craft_select[1][1]:
                cost = 70 if self.level >= 3 else 0
                if self.can_craft[4]:
                    self.screen.blit(self.assets["craftable_selected"],(445,620))
                else:   
                    self.screen.blit(self.assets["uncraftable_selected"],(445,620)) 
            else:
                if self.can_craft[4]:
                    self.screen.blit(self.assets["craftable"],(445,620))
                else:
                    self.screen.blit(self.assets["uncraftable"],(445,620))
            if self.craft_select[1][2]:
                cost = 100  if self.level >= 4 else 0
                if self.can_craft[5]:
                    self.screen.blit(self.assets["craftable_selected"],(900,620))
                else:
                    self.screen.blit(self.assets["uncraftable_selected"],(900,620))
            else:
                if self.can_craft[5]:
                    self.screen.blit(self.assets["craftable"],(900,620))
                else:
                    self.screen.blit(self.assets["uncraftable"],(900,620))
            if True in self.craft_select[2]:
                cost = 0
                extra_text = " GO!"
                self.screen.blit(self.assets["craftable_selected"],(900, 4*SCREEN_HEIGHT/6+100))
            else:
                self.screen.blit(self.assets["craftable"],(900, 4*SCREEN_HEIGHT/6+100))

            text_font = self.assets["pixel_font"].render("craft", True, (255,237,193))
            self.screen.blit(text_font, (110, 335))
            self.screen.blit(text_font, (567, 335))
            self.screen.blit(text_font, (1025, 335))
            self.screen.blit(text_font, (110, 745))
            self.screen.blit(text_font, (567, 745))
            self.screen.blit(text_font, (1025, 745))

            text_font = self.assets["pixel_font"].render("GO!!", True, (255,237,193))
            self.screen.blit(text_font, (1055, 865))



            #buttom text
            self.screen.blit(self.assets["scrap"],(0,810))
            #show text according to the variable "cost"
            if cost:
                text = " x "+str(self.scrap) + " / "+str(cost) + " needed." + extra_text
            else:
                text = " x "+str(self.scrap) + " |"   + extra_text
            text_font = self.assets["font_setting"].render(text, True, (255,255,255))
            self.screen.blit(text_font, (100, 855))

            if self.HP_can < 4:
                self.screen.blit(self.assets["craft_back"],(68,50))
            else:
                self.screen.blit(self.assets["crafted_back"],(68,50))
            self.screen.blit(self.assets["extra_can"],(90,70))

            if "dash" not in self.tools:
                self.screen.blit(self.assets["craft_back"],(523,50))
            else:
                self.screen.blit(self.assets["crafted_back"],(523,50))
            self.screen.blit(self.assets["dash"],(620,70))

            if self.level > 0:
                if "sword" not in self.tools:
                    self.screen.blit(self.assets["craft_back"],(978,50))
                else:
                    self.screen.blit(self.assets["crafted_back"],(978,50))
                self.screen.blit(self.assets["sword"],(1020,80))
            else:
                self.screen.blit(self.assets["craft_back_locked"],(978,50))


            if self.level > 1:
                if "hook" not in self.tools:
                    self.screen.blit(self.assets["craft_back"],(68,450))
                else:
                    self.screen.blit(self.assets["crafted_back"],(68,450))
                self.screen.blit(self.assets["hook"],(92,480))
            else:
                self.screen.blit(self.assets["craft_back_locked"],(68,450))

            if self.level > 2:
                if "harpoon" not in self.tools:
                    self.screen.blit(self.assets["craft_back"],(523,450))
                else:
                    self.screen.blit(self.assets["crafted_back"],(523,450))
                self.screen.blit(self.assets["harpoon"],(550,480))
            else:
                self.screen.blit(self.assets["craft_back_locked"],(523,450))

            if self.level > 3:  
                if "harpoon" not in self.tools:
                    self.screen.blit(self.assets["craft_back"],(978,450))
                else:
                    self.screen.blit(self.assets["crafted_back"],(978,450))
            else:
                self.screen.blit(self.assets["craft_back_locked"],(978,450))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if True in self.craft_select[2]:
                            return
                        elif self.craft_select[0][0]:
                            self.craft("can")
                        elif self.craft_select[0][1]:
                            #craft dash
                            self.craft("dash")
                            
                        elif self.craft_select[0][2]:
                            #craft shield
                            self.craft("sword")
                            
                        elif self.craft_select[1][0]:
                            #craft hook
                            self.craft("hook")
                            
                        elif self.craft_select[1][1]:
                            #craft sord
                            self.craft("harpoon")
                            
                        elif self.craft_select[1][2]:
                            #craft harpoon
                            self.craft("harpoon")
                            
                    if event.key == pygame.K_LEFT:
                        if self.craft_select_cd == 0:
                            self.craft_index[1] = max(self.craft_index[1]-1,1)
                            self.craft_select=[[False,False,False],[False,False,False],[False,False,False]]
                            self.craft_select[self.craft_index[0]-1][self.craft_index[1]-1] = True
                            self.craft_select_cd = 10
                    if event.key == pygame.K_RIGHT:
                        if self.craft_select_cd == 0:
                            self.craft_index[1] = min(self.craft_index[1]+1,3)
                            self.craft_select=[[False,False,False],[False,False,False],[False,False,False]]
                            self.craft_select[self.craft_index[0]-1][self.craft_index[1]-1] = True
                            self.craft_select_cd = 10
                    if event.key == pygame.K_UP:
                        if self.craft_select_cd == 0:
                            self.craft_index[0] = max(self.craft_index[0]-1,1)      
                            self.craft_select=[[False,False,False],[False,False,False],[False,False,False]]
                            self.craft_select[self.craft_index[0]-1][self.craft_index[1]-1] = True
                            self.craft_select_cd = 10
                    if event.key == pygame.K_DOWN:
                        if self.craft_select_cd == 0:
                            self.craft_index[0] = min(self.craft_index[0]+1,3)
                            self.craft_select=[[False,False,False],[False,False,False],[False,False,False]]
                            self.craft_select[self.craft_index[0]-1][self.craft_index[1]-1] = True
                            self.craft_select_cd = 10

            #setting
            pygame.mixer.music.set_volume(self.bgm_factor/5*0.3)
            self.sfx["ambience"].set_volume(0.2*self.sfx_factor/5)
            self.sfx["shoot"].set_volume(0.5*self.sfx_factor/5)
            self.sfx["jump"].set_volume(0.7*self.sfx_factor/5)
            self.sfx["dash"].set_volume(0.7*self.sfx_factor/5)
            self.sfx["swing"].set_volume(0.7*self.sfx_factor/5)
            self.sfx["hit"].set_volume(0.8*self.sfx_factor/5) 
            self.sfx["got_hit"].set_volume(1*self.sfx_factor/5)
            self.clock.tick(FPS)
            self.display_brightness.fill((0, 0, 0, 40*(3-self.brightness)))  # RGBA: (0, 0, 0, 128) for half transparency
            self.screen.blit(self.display_brightness, (0, 0))

            self.transition = min(self.transition+1,0)
            if self.transition:
                tran_surf=pygame.Surface(self.screen.get_size())
                pygame.draw.circle(tran_surf,(255,255,255),(self.screen.get_width()//2,self.screen.get_height()//2),(30-abs(self.transition))*24)
                tran_surf.set_colorkey((255,255,255))
                self.screen.blit(tran_surf,(0,0))
            pygame.display.flip()
            

    def craft(self,item="can",cost = 10):
        if item == "can" and self.can_craft[0]:
            can = self.HP_can
            if can == 1:
                cost = 30
            elif can == 2:
                cost = 50
            elif can == 3:
                cost = 100
            self.tools.append("can")
            self.HP_can += 1
            
        elif item == "dash" and self.can_craft[1]:
            cost = 50
            self.tools.append("dash")
            self.tools.remove("dash_material")
        elif item == "shield" and self.can_craft[2]:
            cost = 50
            self.tools.append("sword")
            self.tools.remove("sword_material")
        elif item == "hook" and self.can_craft[3]:
            cost = 70
            self.tools.append("hook")
            self.tools.remove("hook_material")
        elif item == "sword" and self.can_craft[4]:
            cost = 70   
            self.tools.append("harpoon")
            self.tools.remove("harpoon_material") 
        elif item == "harpoon" and self.can_craft[5]:
            cost = 100
            self.tools.append("harpoon")
            self.tools.remove("harpoon_material")
        else:
            return
        self.scrap -= cost

if __name__ == "__main__":
    main_game().run_main_menu()
