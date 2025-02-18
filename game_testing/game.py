import pygame
import sys
import os
import random
import math
from script.entity import Player, Enemy, Beam, Box, Scrap, Tutorial_trigger
from script.utils import load_image,load_white_image
from script.utils import load_tile,load_trans_tile
from script.utils import load_fix_tile
from script.utils import load_images
from script.utils import load_trans_images,load_trans_image,load_trans_scaled_images,load_scaled_images
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

        self.title_select = [False,False,False]
        self.setting_select = [[True,False],[False,False],[False,False],[False,False]]
        self.setting_index = [1,1]
        self.text_counter = 0

        self.assets = {
            "font": pygame.font.Font("game_testing/data/font/LXGWWenKaiMonoTC-Bold.ttf", 36),
            "font_setting": pygame.font.Font("game_testing/data/font/LXGWWenKaiMonoTC-Bold.ttf", 50),
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
            "button_background": load_trans_image("buttons/bg.png"),
            "text_box": load_image("text_box.png"),
            "head_1": load_trans_image("head/koakuma_head.png"),
            "head_2": load_trans_image("head/hong_head.png"),
            "head_1_shadow": load_trans_image("head/koakuma_shadow.png"),
            "head_2_shadow": load_trans_image("head/hong_shadow.png"),
            "music": load_trans_image("music.png"),
            "sun": load_trans_image("sun.png"),
            "battle_start": load_trans_image("BattleStart.png"),
            "decor" : load_tile("tiles/decor"),
            "stone" : load_tile("tiles/stone"),
            "grass" : load_tile("tiles/grass"),
            "large_decor" : load_trans_tile("tiles/large_decor"),
            "block" : load_fix_tile("tiles/block"),
            "player": load_image("entities/player.png"),
            "background_2": load_image("background3.jpg"),
            "background": load_image("back.png"),
            "enemy/idle" : Animation(load_trans_images("entities/enemy/idle"),duration=10,loop=True),
            "enemy/run" : Animation(load_trans_images("entities/enemy/run"),duration=10,loop=True),
            "enemy/jump" : Animation(load_trans_images("entities/enemy/jump"),duration=5,loop=True),
            "enemy/dash" : Animation(load_trans_images("entities/enemy/dash"),duration=4,loop=False),

            "beam/idle" : Animation(load_trans_images("entities/beam"),duration=5,loop=True),
            "scrap/idle" : Animation(load_trans_images("entities/scrap"),duration=5,loop=True),
            "box/idle" : Animation(load_scaled_images("entities/box",2),duration=5,loop=True),
            "trigger/idle" : Animation(load_trans_images("entities/trigger"),duration=5,loop=True),

            "player/idle" : Animation(load_trans_images("entities/player/idle"),duration=10,loop=True),
            "player/run" : Animation(load_trans_images("entities/player/run"),duration=10,loop=True),
            "player/jump" : Animation(load_trans_images("entities/player/jump"),duration=5,loop=True),
            "player/attack" : Animation(load_trans_images("entities/player/attack"),duration=4,loop=False),
            "particle/leaf" : Animation(load_images("particles/leaf"),duration=20,loop=False),
            "particle/fire" : Animation(load_images("particles/fire"),duration=10,loop=False),
            "particle/particle" : Animation(load_images("particles/particle"),duration=6,loop=False),
            "particle/slash" : Animation(load_trans_scaled_images("entities/slash",0.15),duration=4,loop=False),
            "particle/hp" : Animation(load_images("particles/hp"),duration=10,loop=False),
            "projectile" : load_image("projectile.png"),
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
        self.checkpoint = 0

    def load_level(self,new_level=True):
        self.pause = False
        self.tutorial = 0
        self.tutorial_pause = False
        self.pause_select = 0
        self.pause_select_cd = 0
        self.battle_count_down = 0
        self.movements = [False,False]

        self.player = Player(self, (100,100), (8,15) , HP = 5)

        self.tilemap = Tilemap(self)

        self.projectiles = []
        self.special_projectiles = [] #object [pos,direction,speed,timer,img_name]
        self.particles = []
        self.sparks = []  

        self.camera = [0,0] #camera position = offset of everything
        self.min_max_camera = [0,2440] #min and max camera x position
        self.screen_shake_timer = 0
        self.screen_shake_offset = [0,0]
        self.dead = 0 #dead animation
        self.in_cutscene = False
        self.cutscene_timer = 0

        self.tilemap.load("game_testing/"+str(self.level)+".pickle")

        self.fire_spawners = []

        for fire in self.tilemap.extract([('large_decor',8)],keep=True):
            self.fire_spawners.append(pygame.Rect(4+fire.pos[0], 4+fire.pos[1], 23, 13))

        self.enemy_spawners = []
        for spawner in self.tilemap.extract([('spawners',0),('spawners',1),('spawners',2),('spawners',3),('spawners',4),('spawners',5)],keep=False):
            if spawner.variant == 0:
                self.player.position = spawner.pos #player start position
            elif spawner.variant == 1:
                self.enemy_spawners.append(Enemy(self,spawner.pos,(8,15),phase=1))
            elif spawner.variant == 2:
                self.enemy_spawners.append(Beam(self,spawner.pos,(20,144),duration=-1))
            elif spawner.variant == 3:
                self.enemy_spawners.append(Box(self,(spawner.pos[0]+2,spawner.pos[1]+2),(26,29),duration=-1))
            elif spawner.variant == 4:
                self.enemy_spawners.append(Scrap(self,spawner.pos,(8,8),duration=-1))
            elif spawner.variant == 5:
                self.enemy_spawners.append(Tutorial_trigger(self,spawner.pos,(20,144),duration=-1))


        if self.level == 0:
            self.min_max_camera = [0,0]
            self.transition = -30
        elif self.level == 1:
            self.transition = -50
        elif self.level == -1:
            self.transition = -50

        self.win = 0
        self.phase_3_start = False

        if self.level == -1:
            if new_level:
                pygame.mixer.music.load("game_testing/data/sfx/music_0.wav")
                pygame.mixer.music.set_volume(self.bgm_factor/5*0.2)
                pygame.mixer.music.play(-1)
        if self.level == 0:
            if new_level:
                self.in_cutscene = True
                self.text_list = ["我回來了!","zzz...zzz...","門番又在偷懶了","安靜的從旁邊溜進去......","zzz......!","有入侵者！？"]
                self.order_list = [True,False,True,True,False,False]
                self.battle_count_down = 60
                '''
                pygame.mixer.music.load("game_testing/data/sfx/music_1.wav")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)
                '''

            
        elif self.level == 1:
            if new_level:
                pygame.mixer.music.load("game_testing/data/sfx/Locked_girl.wav")
                pygame.mixer.music.set_volume(self.bgm_factor/5*0.4)
                pygame.mixer.music.play(-1)

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
                if self.win == 90 and self.level == 0:
                    self.first_phase_cutscene()
                if self.win > 90:
                    self.transition += 1
                    if self.transition > 30:
                        self.level += 1
                        self.load_level()

            if self.dead > 0:
                self.dead += 1
                if self.dead >=10:
                    self.transition = min(30,self.transition+1)
                if self.dead > 40:
                    self.load_level(False)

            self.camera[0] += (self.player.rect().centerx - self.display.get_width()/4 -self.camera[0])/20 #camera follow player x
            self.camera[0] = max(self.min_max_camera[0],self.camera[0])
            self.camera[0] = min(self.min_max_camera[1],self.camera[0])
            #self.camera[1] += (self.player.rect().centery - self.display.get_height()/2 - self.camera[1])/20 #camera follow player y
            self.render_camera = [int(self.camera[0])+50, int(self.camera[1])]

            self.tilemap.render(self.display,offset=self.render_camera) #render background

            if self.in_cutscene == False and self.cutscene_timer == 0:
                #tutorial end
                if self.player.position[0] > 2880 and self.level == -1 and self.win == 0:
                    self.win = 1
                for spawner in self.fire_spawners:
                    if random.random() * 4999 < spawner.width* spawner.height:
                        pos = (spawner.x + random.random()*spawner.width, spawner.y + random.random()*spawner.height-8)
                        self.particles.append(Particle(self,'fire',pos,velocity=[-0.2,0.3],frame=random.randint(0,20)))
                

                for enemy in self.enemy_spawners.copy():
                    kill = enemy.update((0,0),self.tilemap)
                    if enemy.render_type == "obstacle":
                        enemy.render(self.display,offset=self.render_camera)
                    if kill and enemy.type == "trigger":
                        self.enemy_spawners.remove(enemy)
                        self.tutorial_pause = True
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
                    elif kill:
                        self.enemy_spawners.remove(enemy)
                        for i in range(4):
                            self.sparks.append(Flame((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 3+random.random()))
                            self.sparks.append(Flexible_Spark((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 3+random.random(),(255,127,0)))
                            self.sparks.append(Gold_Flame((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 2+random.random()))
                            self.sparks.append(Flexible_Spark((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 1+random.random(),(0,255,0)))
                            self.sparks.append(Ice_Flame((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 5+random.random()))
                            self.sparks.append(Flexible_Spark((enemy.rect().center[0]+random.randint(-8,8),enemy.rect().center[1]), 1.5*math.pi, 4+random.random(),(148,0,211)))
                        
                if not self.dead:
                    self.player.update((self.movements[1] - self.movements[0],0),self.tilemap) #update player
                    #self.player.render(self.display,offset=self.render_camera) #render player

                #[[x,y],direction,timer]
                for projectile in self.projectiles.copy():
                    projectile[0][0] += projectile[1]
                    projectile[2] += 1
                    img = self.assets['projectile']
                    #img = pygame.transform.scale(img,(img.get_width()//8,img.get_height()//8))
                    if projectile[1] > 0:
                        self.display.blit(img,(projectile[0][0]-img.get_width()/2 -self.render_camera[0],projectile[0][1]-img.get_height()/2-self.render_camera[1]))
                    else:
                        self.display.blit(pygame.transform.flip(img, True, False),(projectile[0][0]-img.get_width()/2 -self.render_camera[0],projectile[0][1]-img.get_height()/2-self.render_camera[1]))
                    if self.tilemap.solid_check(projectile[0]):
                        try:
                            self.projectiles.remove(projectile) 
                        except:
                            pass
                        for i in range(4):
                            self.sparks.append(Spark(projectile[0],random.random()*math.pi*2,2+random.random()))
                    elif projectile[2] > 360:
                        try:
                            self.projectiles.remove(projectile)
                        except:
                            pass
                    elif abs(self.player.dashing) < 50:
                        if self.player.rect().collidepoint(projectile[0]):
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
                        if event.key == pygame.K_j:
                            self.player.jump()
                        if event.key == pygame.K_k:
                            self.player.fast_fall()
                        if event.key == pygame.K_SPACE:
                            self.player.dash()
                        if event.key == pygame.K_z: 
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
                        if event.key == pygame.K_j:
                            self.player.stop_jump()

                #player keeps move right
                self.movements[1] = True
    

                self.screen_shake_timer = max(0,self.screen_shake_timer-1)
                self.screen_shake_offset = [random.randint(-self.screen_shake_timer,self.screen_shake_timer),random.randint(-self.screen_shake_timer,self.screen_shake_timer)]  
            
            if not self.in_cutscene:
                for i in range(self.player.HP):
                    self.display_for_outline.blit(self.assets['HP'],(i*18,20))
            
            self.display_for_outline.blit(self.display, (0,0))
            
            self.screen.blit(pygame.transform.scale(self.display_for_outline, (2*SCREEN_WIDTH, 2*SCREEN_HEIGHT)), self.screen_shake_offset) 
            
            #blit self.display_entity to screen without scaling
            #if not self.dead and abs(self.player.dashing) < 50:
            if not self.dead :
                self.player.render_new(self.screen,offset=self.render_camera) #render player

            if not self.in_cutscene:
                if self.player.charge < self.player.max_charge:
                    ratio = self.player.charge/self.player.max_charge
                    pygame.draw.rect(self.screen,(0,137,255),(21,171,390*ratio,20))
                    img = pygame.transform.scale(self.assets['energy_empty'],(58*8,12*8))
                    self.screen.blit(pygame.transform.flip(img,False,True),(-20,130))
                else:
                    img = pygame.transform.scale(self.assets['energy_max'],(58*8,12*8))
                    self.screen.blit(pygame.transform.flip(img,False,True),(-20,130))
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
                pause_screen.fill((0, 0, 0, 128))  # RGBA: (0, 0, 0, 128) for half transparency
                pygame.draw.circle(pause_screen,(255,255,255),(500,500),10)
                pause_screen.set_colorkey((255,255,255))
                self.screen.blit(pygame.transform.scale(self.display, (2*SCREEN_WIDTH, 2*SCREEN_HEIGHT)), (0,0)) 
                self.screen.blit(pause_screen, (0, 0))
                self.temp_screen = self.screen.copy()

            if self.in_cutscene == True and not self.transition: 
                speed = 4
                #blit the text box at the buttom of the screen
                self.screen.blit(pygame.transform.scale(self.assets["text_box"], (SCREEN_WIDTH, SCREEN_HEIGHT//4)),(0,3*SCREEN_HEIGHT//4))
                #blit headd_1 at the left of the text box while scale it up to 2x
                if self.order_list[0]:
                    self.screen.blit(pygame.transform.scale(pygame.transform.flip(self.assets["head_1"],True,False),(self.assets["head_1"].get_width()*1.8,self.assets["head_1"].get_height()*1.8-3)),(10,3*SCREEN_HEIGHT//4+7))
                    img = self.assets["head_2"].copy()
                    img.blit(self.assets["head_2_shadow"],(0,0))
                    self.screen.blit(pygame.transform.scale(img,(self.assets["head_2"].get_width()*1.8,self.assets["head_2"].get_height()*1.8-3)),(SCREEN_WIDTH-10-self.assets["head_2"].get_width()*1.8,3*SCREEN_HEIGHT//4+7))

                else:
                    self.screen.blit(pygame.transform.scale(self.assets["head_2"],(self.assets["head_2"].get_width()*1.8,self.assets["head_2"].get_height()*1.8-3)),(SCREEN_WIDTH-10-self.assets["head_2"].get_width()*1.8,3*SCREEN_HEIGHT//4+7))
                    img= self.assets["head_1"].copy()
                    img.blit(self.assets["head_1_shadow"],(0,0))
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
                            self.text_counter = 0
                            if not self.text_list:
                                self.in_cutscene = False
                                pygame.mixer.music.load("game_testing/data/sfx/music_1.wav")
                                pygame.mixer.music.set_volume(self.bgm_factor/5*0.2)
                                pygame.mixer.music.play(-1)
                   
            if self.battle_count_down > 0 and not self.in_cutscene:
                self.battle_count_down -= 1
                #blit battle_start at the middle of the screen
                #the img will first scale up and then shrink to its original size, and than fade out as the countdown goes down
                if self.battle_count_down > 45:
                    img = pygame.transform.scale(self.assets["battle_start"], (self.assets["battle_start"].get_width()*1.5*(self.battle_count_down)//45, self.assets["battle_start"].get_height()*1.5*(self.battle_count_down)//45))
                    self.screen.blit(img, (HALF_SCREEN_WIDTH/2, HALF_SCREEN_HEIGHT/2-100))
                elif self.battle_count_down > 0:
                    img = pygame.transform.scale(self.assets["battle_start"], (self.assets["battle_start"].get_width()*1.5, self.assets["battle_start"].get_height()*1.5))
                    img.set_alpha(255*(self.battle_count_down)/45)
                    self.screen.blit(img, (HALF_SCREEN_WIDTH/2, HALF_SCREEN_HEIGHT/2-100))
                else:
                    self.battle_count_down = 0
            self.screen.blit(self.display_brightness, (0, 0))
            pygame.display.update()
            self.clock.tick(FPS)

    def first_phase_cutscene(self):
        self.in_cutscene = True
        self.text_list = ["原來是小惡魔啊，還以為是入侵者呢（呵欠","......zzz...zzz","竟然睡回去了......","算了，趕快進屋吧"]
        self.order_list = [False,False,True,True]

    def run_main_menu(self):
        pygame.mixer.music.load("game_testing/data/sfx/Raise_the_Flag_of_Cheating.wav")
        pygame.mixer.music.set_volume(self.bgm_factor/5*0.3)
        pygame.mixer.music.play(-1)
        while True:
            #blit the title screen and scale it to the screen size
            self.screen.blit(pygame.transform.scale(self.assets["title_screen"], (SCREEN_WIDTH, SCREEN_HEIGHT)),(0,0))
            self.clock.tick(FPS)
            #blit a half transparent background for the button
            button_bg = self.assets["button_background"].copy()
            button_bg.set_alpha(128)  # Set transparency level (0-255)
            self.screen.blit(pygame.transform.scale(button_bg,(650,600)), (-30, 350))
            self.screen.blit(pygame.transform.scale(self.assets["title"],(450,450)),(65,-20))
            #blit the buttons
            if self.title_select[0]:
                self.screen.blit(pygame.transform.scale(self.assets["title_start_selected"],(450,450)),(70,300))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["title_start"],(450,450)),(70,300))
            if self.title_select[2]:
                self.screen.blit(pygame.transform.scale(self.assets["title_setting_selected"],(450,450)),(70,420))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["title_setting"],(450,450)),(70,420))
            if self.title_select[1]:
                self.screen.blit(pygame.transform.scale(self.assets["title_quit_selected"],(450,450)),(70,540))
            else:
                self.screen.blit(pygame.transform.scale(self.assets["title_quit"],(450,450)),(70,540))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.level = -1
                        self.load_level()
                        self.run_game()
                        pygame.mixer.music.load("game_testing/data/sfx/Raise_the_Flag_of_Cheating.wav")
                        pygame.mixer.music.set_volume(self.bgm_factor/5*0.3)
                        pygame.mixer.music.play(-1)

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

if __name__ == "__main__":
    main_game().run_main_menu()
