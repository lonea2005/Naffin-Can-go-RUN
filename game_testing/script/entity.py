import pygame
from script.particle import Particle
from script.spark import Spark, Flame, Gold_Flame, Ice_Flame, Flexible_Spark
import math
import random

class Diagnal_Projectile:
    def __init__(self,pos=[0,0],direction=[1,0],speed=1,img_name=""):
        self.pos = list(pos)
        self.direction = direction
        self.speed = speed
        self.timer = 0
        self.img_name = img_name
        self.length_of_direction = math.sqrt(self.direction[0]**2 + self.direction[1]**2)
    def update(self):
        self.pos[0] += self.direction[0] * self.speed / self.length_of_direction
        self.pos[1] += self.direction[1] * self.speed / self.length_of_direction
        self.timer += 1
    def reverse(self):
        return True

class Special_Projectile(Diagnal_Projectile):
    def __init__(self,pos=[0,0],direction=[1,0],speed=1,img_name="",max_timer=180,type="normal",main_game=None,reverse=False):
        super().__init__(pos,direction,speed,img_name)
        self.max_timer = max_timer
        self.type = type
        self.main_game = main_game
        self.can_reverse = reverse

    def update(self):
        if self.type == ("two_stage_spin" or "two_stage_random") and self.timer < self.max_timer:
            self.speed *= 0.9
        if self.timer == self.max_timer:
            if self.type == "explode_shoot":
                self.explode()
            elif self.type == "two_stage_spin" or self.type == "two_stage_random":    
                self.second_stage()
            elif self.type == "small_explode":
                self.small_explode()
        super().update()

    def second_stage(self):
        self.speed = 3 if self.type == "two_stage_spin" else 2
    
    def explode(self):
        #boss will shoot 8 special projectiles in all directions
        self.velocity = [0,0]
        for i in range(12):
            angle = i * math.pi / 6
            self.main_game.special_projectiles.append(Diagnal_Projectile(self.pos,[math.cos(angle),math.sin(angle)],1.5,"projectile_"+str(random.randint(1,7))))
            for i in range(4):
                self.main_game.sparks.append(Ice_Flame(self.main_game.special_projectiles[-1].pos,random.random()*math.pi*2,1+random.random()))
        self.main_game.special_projectiles.remove(self)
    
    def small_explode(self):
        #boss will shoot 8 special projectiles in all directions
        self.velocity = [0,0]
        random_angle = random.random()*math.pi*2
        for i in range(6):
            angle = i * math.pi / 3 + random_angle  
            self.main_game.special_projectiles.append(Diagnal_Projectile(self.pos,[math.cos(angle),math.sin(angle)],3,"projectile_"+str(random.randint(1,7))))
            for i in range(4):
                self.main_game.sparks.append(Ice_Flame(self.main_game.special_projectiles[-1].pos,random.random()*math.pi*2,1+random.random()))
        self.main_game.special_projectiles.remove(self)

    def reverse(self):
        if self.can_reverse:
            self.direction = [-self.direction[0],-self.direction[1]]
            self.can_reverse = False
            return False
        return True


class physics_entity:
    def __init__(self,main_game,entity_type,position,size):
        self.main_game = main_game
        self.entity_type = entity_type
        self.position = list(position)  
        self.size = size
        self.velocity = [0,0]
        self.dashing = 0
        self.jumping = False
        self.render_type = 'normal'

        #Animation
        self.action = ''
        self.anim_offset = (-5,-10) #避免動畫比原本圖片大所以預留空間
        self.flip = False
        self.set_action('idle')

    def set_action(self,action):
        if self.action != action:
            self.action = action
            self.anim = self.main_game.assets[self.entity_type + "/" + action].copy()

    def rect(self):
        return pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def update(self, movement=(0,0),tilemap=None):
        self.check_collision = {'up':False, 'down':False, 'left':False, 'right':False}
        frame_movement = [(movement[0] + self.velocity[0]), movement[1] + self.velocity[1]]

        self.position[0] += frame_movement[0]
        entity_rect = self.rect()

        for rect in tilemap.tile_collision(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    self.check_collision['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.check_collision['left'] = True
                self.position[0] = entity_rect.x

        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.position[1] += frame_movement[1]
        entity_rect = self.rect()

        for rect in tilemap.tile_collision(self.position):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.check_collision['down'] = True
                    self.jumping = False
                if frame_movement[1] < 0:
                    self.check_collision['up'] = True
                self.position[1] = entity_rect.y


        if self.check_collision['down']:
            self.velocity[1] = 0  
              
        self.anim.update()  

    def render(self,surface,offset=[0,0]):
        surface.blit(pygame.transform.flip(self.anim.img(),self.flip,False),(self.position[0]-offset[0]+self.anim_offset[0],self.position[1]-offset[1]+self.anim_offset[1]))
        #surface.blit(self.main_game.assets['player'],(self.position[0]-offset[0],self.position[1]-offset[1])    )
    def render_new(self,surface,offset=[0,0]):
        if self.entity_type == "player" or self.type == "boss":
            surface.blit(pygame.transform.scale(pygame.transform.flip(self.anim.img(),self.flip,False),(80,100)),(4*int(self.position[0]-offset[0]+self.anim_offset[0]),4*int(self.position[1]-offset[1]+self.anim_offset[1]+1))) #+1 for visually reg
            #surface.blit(pygame.transform.scale(pygame.transform.flip(self.anim.img(),not self.flip,False),(56,70)),(4*int(self.position[0]-offset[0]+self.anim_offset[0]),4*int(self.position[1]-offset[1]+self.anim_offset[1]+1))) #+1 for visually reg
        elif self.entity_type == "dummy":
            surface.blit(pygame.transform.scale(pygame.transform.flip(self.anim.img(),not self.flip,False),(120,150)),(4*int(self.position[0]-offset[0]+self.anim_offset[0]),4*int(self.position[1]-offset[1]+self.anim_offset[1]+1)))


class Player(physics_entity):
    def __init__(self,main_game,position,size,HP,weapon=None,spell_card=None,accessory=[]):     
        super().__init__(main_game,'player',position,size)
        self.air_time = 0
        self.jump_count = 1
        self.stop_jump_check = False
        self.HP = HP
        self.attack_cool_down = 0    
        self.attack_animation = 0
        self.inv_time = 0
        self.extra_attack = False
        self.extra_attack_frame = 0
        self.max_inv_time = 60
        self.max_attack_cool_down = 30
        self.weapon = weapon.name if weapon else "none"
        self.spell_card = spell_card
        self.accessory = accessory
        self.damage=2
        self.score = 0
        self.charge_effect = False
        self.weapon = "貪欲的叉勺"
        if self.weapon == "貪欲的叉勺":
            self.damage = 3
            self.max_attack_cool_down = 20
            self.max_charge = 8
            self.charge_per_hit = 1
            self.charge = 0
        elif self.weapon == "七耀魔法書":
            self.max_mana = 30
            self.mana = self.max_mana
        else:
            self.max_charge = 10
            self.charge_per_hit = 1
            self.charge = 0

        self.spell_card = spell_card.name if spell_card else "none"
        self.accessory = [accessory[i].name for i in range(len(accessory))]

        self.testing_stats()

        if "水晶吊墜" in self.accessory:
            self.max_mana += 10
            self.mana = self.max_mana
        if "心型吊墜" in self.accessory:
            self.HP += 1
        if "亡靈提燈" in self.accessory:    
            self.max_inv_time += 30
        #"蝙蝠吊墜" setting in enemy
        if "銀製匕首" in self.accessory:
            self.damage += 1
        if "斷線的人偶" in self.accessory:
            pass
        if "神社的符咒" in self.accessory:  
            pass
        if "巫女的御幣" in self.accessory:
            self.extra_attack = True

        self.harpoon_counter = 0
        self.tutorial_jumping = 0
        self.on_hook = False
        self.on_hook_moving = False
        self.hook_pos = (0,0)

        
    
    def testing_stats(self):
        #testing stats goes here
        #self.damage = 100
        #self.weapon = "貪欲的叉勺"
        #self.accessory = ["巫女的御幣"]
        self.accessory = ["亡靈提燈"]
        #self.weapon = "反則之書"
        #self.accessory = ["蝙蝠吊墜"]
        pass


    def update(self, movement=(0,0),tilemap=None):
        super().update(movement,tilemap)
        self.tutorial_jumping = max(0,self.tutorial_jumping-1)
        #if player is dashing, do not apply gravity
        if self.harpoon_counter > 0:
            self.harpoon_counter -= 1
            if self.harpoon_counter == 1920:
                self.main_game.projectiles.append([[self.rect().centerx,self.rect().centery],3,1,"harpoon"])
        if self.velocity[1]<5 and not (abs(self.dashing) > 50) and self.harpoon_counter<1800 and not self.on_hook:
            self.velocity[1] = min(5,self.velocity[1]+0.1) #gravity
        if self.harpoon_counter <= 1500:
            self.harpoon_counter = 0

        self.air_time += 1


        self.attack_cool_down = max(0,self.attack_cool_down-1)
        self.inv_time = max(0,self.inv_time-1)
        if abs(self.dashing)<20:
            self.dashing = 0

        if self.check_collision['down']:
            self.air_time = 0
            self.jump_count = 1
        #if self.check_collision['right'] and not self.check_collision['up']:
        #    self.take_damage(1,[1,0])
        elif self.check_collision['up']:
            self.inv_time = 10
        if self.attack_animation > 0:
            #self.set_action('attack')
            self.attack_animation -= 1
        elif self.air_time > 4:
            self.set_action('jump') 
        elif movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        if self.dashing > 0:
            self.dashing = max(0,self.dashing-1)
        if self.dashing < 0:
            self.dashing = min(0,self.dashing+1)
        if abs(self.dashing) > 50:
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            if abs(self.dashing) == 51:
                self.velocity[0] *= 0.1
            pv = [math.cos(random.random()*math.pi*2)*random.random()*0.5+0.5,math.sin(random.random()*math.pi*2)*random.random()*0.5+0.5]
            self.main_game.particles.append(Particle(self.main_game,'particle',self.rect().center,pv,frame=random.randint(0,7)))
        if self.velocity[0] > 0 and not self.on_hook:
            self.velocity[0] = max(0,self.velocity[0]-0.1)
        if self.velocity[0] < 0 and not self.on_hook:
            self.velocity[0] = min(0,self.velocity[0]+0.1)   

        self.extra_attack_frame = max(0,self.extra_attack_frame-1)
        if self.extra_attack_frame == 1:
            temp=self.attack_cool_down
            self.attack_cool_down = 0
            self.attack(self.extra_attack)
            self.attack_cool_down = temp


    def render(self,surface,offset=[0,0]):
        super().render(surface,offset)
        #surface.blit(self.main_game.assets['player'],(self.position[0]-offset[0],self.position[1]-offset[1])    )
    def jump(self):
        if self.jump_count > 0:
            self.stop_jump_check = False
            self.main_game.sfx['jump'].play()
            self.velocity[1] = -4
            self.jump_count -= 1
            self.air_time = 5
            self.set_action('jump')
            if self.dashing and self.weapon == "反則之書":
                self.dashing = 0
            return True
        return False
    def tutorial_jump(self):
        self.tutorial_jumping = 60
        self.stop_jump_check = False
        self.main_game.sfx['jump'].play()
        self.velocity[1] = -3.2
        self.jump_count -= 1
        self.air_time = 5
        self.set_action('jump')
        return True
    def stop_jump(self):
        if self.velocity[1] < 0 and not self.tutorial_jumping:
            self.velocity[1] = min(0,self.velocity[1]+1.3) if not self.stop_jump_check else self.velocity[1]
            self.stop_jump_check = True

    def fast_fall(self):
        if self.on_hook:
            self.hook_stop()
        if not self.check_collision['down']:
            self.velocity[1] = 10
        
            
    def attack(self,is_extra=False):
        if self.attack_cool_down == 0:
            self.main_game.sfx['swing'].play()
            self.attack_cool_down = self.max_attack_cool_down
            self.attack_animation = 20
            if self.weapon == "none":
                #attack a rect-space area in front of the player
                #if charge is full, attack will deal additional damage
                if self.flip:
                    hitbox = pygame.Rect(self.rect().centerx -36,self.rect().centery,28,16)
                    self.main_game.particles.append(Particle(self.main_game,'slash',(self.rect().centerx -18,self.rect().centery),velocity=[0,0],frame=10))
                else:
                    hitbox = pygame.Rect(self.rect().centerx +8,self.rect().centery,28,16) 
                    self.main_game.particles.append(Particle(self.main_game,'slash',(self.rect().centerx +18,self.rect().centery),velocity=[0,0],frame=10,flip=True))  
                for enemy in self.main_game.enemy_spawners:
                    if hitbox.colliderect(enemy.rect()) and enemy.type != 'beam':
                        enemy.HP -= 1.5*self.damage if self.charge_effect else self.damage
                        self.charge = min(self.charge+self.charge_per_hit,self.max_charge)
                        self.main_game.sfx['hit'].play()
                        for i in range(10):
                            angle = random.random()*math.pi*2
                            speed = random.random() *5
                            self.main_game.sparks.append(Gold_Flame(enemy.rect().center,angle,2+random.random()))  
                            self.main_game.particles.append(Particle(self.main_game,'particle',enemy.rect().center,[math.cos(angle+math.pi)*speed*0.5,math.sin(angle+math.pi)*speed*0.5],frame=random.randint(0,7)))  
                        self.main_game.sparks.append(Gold_Flame(enemy.rect().center, 0, 5+random.random()))
                        self.main_game.sparks.append(Gold_Flame(enemy.rect().center, math.pi, 5+random.random()))
                if self.extra_attack and not is_extra:
                    self.extra_attack_frame = 11
                if self.charge == self.max_charge and not self.charge_effect:
                    #green spark effect
                    for i in range(30):
                        angle = random.random()*math.pi*2
                        speed = random.random() *5
                        self.main_game.sparks.append(Flexible_Spark(self.rect().center,angle,2+random.random(),(0,255,0)))
                    self.charge_effect = True
            elif self.weapon == "貪欲的叉勺":
                if self.flip:
                    hitbox = pygame.Rect(self.position[0]-36,self.position[1],28,22)
                    self.main_game.particles.append(Particle(self.main_game,'slash',(self.rect().centerx -18,self.rect().centery),velocity=[0,0],frame=10))
                else:
                    hitbox = pygame.Rect(self.position[0]+8,self.position[1],28,22)   
                    self.main_game.particles.append(Particle(self.main_game,'slash',(self.rect().centerx +18,self.rect().centery),velocity=[0,0],frame=10,flip=True))  
                for enemy in self.main_game.enemy_spawners:
                    if hitbox.colliderect(enemy.rect()) and (enemy.type == 'box' or enemy.type == 'knife'):
                        enemy.HP -= self.damage
                        self.main_game.sfx['hit'].play()
                        for i in range(10):
                            angle = random.random()*math.pi*2
                            speed = random.random() *5
                            self.main_game.sparks.append(Gold_Flame(enemy.rect().center,angle,2+random.random()))  
                            self.main_game.particles.append(Particle(self.main_game,'particle',enemy.rect().center,[math.cos(angle+math.pi)*speed*0.5,math.sin(angle+math.pi)*speed*0.5],frame=random.randint(0,7)))  
                        self.main_game.sparks.append(Gold_Flame(enemy.rect().center, 0, 5+random.random()))
                        #self.main_game.sparks.append(Gold_Flame(enemy.rect().center, math.pi, 5+random.random()))
                for bullet in self.main_game.projectiles.copy():
                    if hitbox.colliderect(pygame.Rect(bullet[0][0]-4,bullet[0][1]-4,8,8)):
                        self.charge = min(self.charge+self.charge_per_hit,self.max_charge)
                        self.main_game.projectiles.remove(bullet)
                        self.attack_cool_down = 1
                        for i in range(10):
                            angle = random.random()*math.pi*2
                            speed = random.random() *5
                            self.main_game.sparks.append(Spark(bullet[0],angle,2+random.random()))  
                for bullet in self.main_game.special_projectiles:
                    if hitbox.colliderect(pygame.Rect(bullet.pos[0]-4,bullet.pos[1]-4,8,8)):
                        self.charge = min(self.charge+self.charge_per_hit,self.max_charge)
                        self.main_game.special_projectiles.remove(bullet)
                        for i in range(10):
                            angle = random.random()*math.pi*2
                            speed = random.random() *5
                            self.main_game.sparks.append(Spark(bullet.pos,angle,2+random.random()))
                if self.extra_attack and not is_extra:
                    self.extra_attack_frame = 11
            return True
        return False
    
    def charge_attack(self):
        self.charge_effect = False
        if self.weapon == "貪欲的叉勺":
            pass
        elif self.weapon == "七耀魔法書":
            pass
        else:
            #heal
            if self.charge == self.max_charge:
                for i in range(30):
                    #add leaf particle arround the player
                    angle = random.random()*math.pi*2
                    speed = random.random() *3
                    #self.main_game.sparks.append(Flexible_Spark(self.rect().center,angle,2+random.random(),(0,255,0)))
                    self.main_game.particles.append(Particle(self.main_game,'hp',(self.rect().centerx+random.randint(-10,10),self.rect().centery+random.randint(-3,3)),[math.cos(angle+math.pi)*speed*0.5*0,-1*abs(math.sin(angle+math.pi)*speed*0.5)],frame=random.randint(0,7)))

                #self.main_game.sfx['heal'].play()
                self.HP = min(self.HP+1,6)
                self.charge = 0
                return True



    def dash(self):
        #set verticle velocity to 0
        if not self.dashing:
            self.main_game.sfx['dash'].play()
            self.velocity[1] = 0
            self.dashing = -60 if self.flip else 60
            return True 
        return False
    
    def hook(self):
        if "hook" in self.main_game.tools:
            for hook_start in self.main_game.hook_spawners:
                if abs(hook_start.check_player_pos()[0]) <= 80 and hook_start.type == "hook_start":
                    self.hook_pos = hook_start.rect().center
                    self.velocity = [0,0]
                    self.main_game.sfx['jump'].play()
                    self.on_hook = True
                    direction = [self.hook_pos[0]-self.rect().centerx,self.hook_pos[1]-self.rect().centery]
                    length = math.sqrt(direction[0]**2 + direction[1]**2)
                    direction = [direction[0]/length,direction[1]/length]
                    self.velocity = [direction[0]*3,direction[1]*3]
                    return True
            return True
    
    def hook_move(self,pos):
        #calculate the diretion from player position to the hook_pos
        self.position = list(pos)
        for stop in self.main_game.hook_spawners:
            if stop.type == "hook_stop" and stop.used == False:
                self.hook_pos = stop.rect().center
                direction = [self.hook_pos[0]-self.rect().centerx,self.hook_pos[1]-self.rect().centery]
                length = math.sqrt(direction[0]**2 + direction[1]**2)
                direction = [direction[0]/length,direction[1]/length]
                self.velocity = [direction[0]*3,direction[1]*3]
                self.on_hook_moving = True
                stop.used = True
                return True
        
    def hook_stop(self):
        self.on_hook = False
        self.on_hook_moving = False
        self.velocity = [0,0]
        self.hook_pos = (0,0)
        return True

    def harpoon(self):
        if "harpoon" in self.main_game.tools and self.harpoon_counter <= 0:
            self.velocity = [0,0]
            self.main_game.sfx['jump'].play()
            self.harpoon_counter = 180+1800
            for i in range(30):
                #add leaf particle arround the player
                angle = random.random()*math.pi*2
                speed = random.random() *3
                self.main_game.sparks.append(Flexible_Spark(self.rect().center,angle,2+random.random(),(0,255,0)))
            return True


    def take_damage(self,damage=1,relative_pos=[0,0]):
        if self.inv_time == 0:
            self.relative_pos = relative_pos
            #if player takes damage, lose 1 HP and got knockback to the opposite direction of the enemy
            self.HP -= damage
            self.main_game.sfx['got_hit'].play()

            self.main_game.screen_shake_timer = max(10,self.main_game.screen_shake_timer) #shake screen for 10 frames

            self.inv_time = self.max_inv_time
            for i in range(30):
                angle = random.random()*math.pi*2
                speed = random.random() *5
                self.main_game.sparks.append(Flexible_Spark(self.rect().center,angle,2+random.random(),(0,0,0)))  
                self.main_game.particles.append(Particle(self.main_game,'particle',self.rect().center,[math.cos(angle+math.pi)*speed*0.5,math.sin(angle+math.pi)*speed*0.5],frame=random.randint(0,7)))
            if self.HP <= 0:
                self.main_game.dead += 1    

    def render(self,surface,offset=[0,0]):
        if abs(self.dashing) <= 50:
            super().render(surface,offset)

class Enemy(physics_entity):
    def __init__(self,main_game,position,size,phase=1,action_queue=[]):
        super().__init__(main_game,'enemy',position,size)
        self.type='boss'
        self.flip = True
        self.set_action('idle')

        self.phase = phase
        self.action_queue = action_queue

        self.idle_time = 0 #time that enemy do nothing
        self.walking = 0
        self.jumping = False
        self.air_dashing = False
        self.furiously_dashing = False
        self.dashing_towards_player = False
        self.froze_in_air  = False
        self.using_spell_card = False
        self.time_counter = 0
        self.current_counter = 0
        self.attack_cool_down = 300 #prevent enemy from spamming attack at the beginning

        self.attack_preview_pos_a = None    
        self.attack_preview_pos_b = None

        if self.phase == 1:
            self.HP = 35
            self.action_queue = [['empty',60],300]
            self.p1_shoot_count = 0
            #self.HP = 1
        elif self.phase == 2:
            self.HP = 40
            #self.HP = 1
        elif self.phase == 3:
            self.HP = 2200
            self.using_spell_card = True
            self.timer_HP = 2200
            self.max_HP = 2200
        self.attack_combo = 0
        self.max_HP = self.HP
        #combo 1: jump - dash - drop attack - land shot
        #combo 2: dash forward and shoot 3 bullets
        self.test_stats()
    
    def test_stats(self):
        #self.HP=25
        pass

    def update(self, movement=(0,0),tilemap=None):

        if self.check_player_pos()[0] > 0:
            self.flip = False
        else:
            self.flip = True
        
        if self.phase == 1:
            self.attack_cool_down = max(0,self.attack_cool_down-1)
            if not (self.air_dashing):
                self.velocity[1] = min(7,self.velocity[1]+0.1) #gravity
            if len(self.action_queue)>0 and isinstance(self.action_queue[0],int):
                self.action_queue[0] -= 1
                self.jumping = False
                if self.action_queue[0] == 0:
                    self.action_queue.pop(0)
                    self.p1_shoot_count = 0
                    self.attack_combo = random.choice([1,2])
                    self.action_queue.insert(0,["empty",30])
                    self.action_queue.insert(1,"combo()")
                #normal detection
                movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
                if self.p1_shoot_count > 2:
                    self.action_queue.pop(0)
                    self.attack_combo = random.choice([1,2])
                    self.p1_shoot_count = 0
                    self.action_queue.insert(0,["empty",30])
                    self.action_queue.insert(1,"combo()")
                elif abs(self.check_player_pos()[0])<32:
                    self.p1_shoot_count +=1
                    self.action_queue.insert(0,"prepare_attack()")
                    self.action_queue.insert(1,["empty",30])
                    self.action_queue.insert(2,"ground_smash()")
                    self.action_queue.insert(3,["empty",5])
                    self.action_queue.insert(4,"screen_shake(20)")
                    self.action_queue.insert(5,["empty",30])
                elif abs(self.check_player_pos()[0])<144:
                    self.p1_shoot_count +=1
                    self.action_queue.insert(0,"normal_shoot()")
                    self.action_queue.insert(1,["empty",20])
                    self.action_queue.insert(1,["empty_walk",80])

            elif len(self.action_queue)>0 and isinstance(self.action_queue[0],list):
                if self.action_queue[0][0] == "empty_walk":
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
                    self.action_queue[0][1] -= 1
                    if self.action_queue[0][1] == 0:
                        self.action_queue.pop(0)
                elif self.action_queue[0][0] == "empty":
                    self.action_queue[0][1] -= 1
                    if self.action_queue[0][1] == 0:
                        self.action_queue.pop(0)
                elif self.action_queue[0][0] == "aim_drop":
                    self.action_queue[0][1] -= 1
                    player_pos = self.check_player_pos()
                    if abs(player_pos[0]) < 8 or self.action_queue[0][1] == 0:
                        self.air_dashing = False
                        self.velocity = [0,0]
                        self.action_queue.pop(0)
                elif self.action_queue[0][0] == "land_detect":
                    self.action_queue[0][1] -= 1
                    if self.check_collision['down'] or self.action_queue[0][1] == 0:
                        self.attack_combo = 0
                        self.current_counter = self.time_counter
                        self.screen_shake(10)
                        self.action_queue.pop(0)
                
            elif len(self.action_queue)>0:
                exec("self."+self.action_queue.pop(0))
            else:
                pass


        elif self.phase == 2:
            #apply gravity if not froze
            if not self.froze_in_air:
                self.velocity[1] = min(7,self.velocity[1]+0.1)
            if len(self.action_queue)>0 and isinstance(self.action_queue[0],int):
                self.action_queue[0] -= 1
                if self.action_queue[0] == 0:
                    self.action_queue.pop(0)
            elif len(self.action_queue)>0 and isinstance(self.action_queue[0],list):
                if self.action_queue[0][0] == "attack_preview()":   
                    if not self.attack_preview_pos_a:
                        self.attack_preview_pos_a,self.attack_preview_pos_b = self.attack_preview()
                    else:
                        self.attack_preview(self.attack_preview_pos_a,self.attack_preview_pos_b)
                elif self.action_queue[0][0] == "dash_to()":   
                    self.dash_towards_player(self.attack_preview_pos_b)
                self.action_queue[0][1] -= 1
                if self.action_queue[0][1] == 0:
                    self.action_queue.pop(0) 
            elif len(self.action_queue)>0:
                exec("self."+self.action_queue.pop(0))
            else:
                if self.dashing_towards_player:
                    if self.check_collision['down']:
                        self.dashing_towards_player = False
                        self.velocity = [0,0]
                        self.screen_shake(10)
                        for i in range(20):
                            angle = random.random()*math.pi*2
                            speed = random.random() *3
                            self.main_game.sparks.append(Flame(self.rect().center,angle,2+random.random()))
                        self.ground_8_shoot()
                        self.froze_in_air = False
                elif self.furiously_dashing:
                    #horizontal Flame effect
                    for i in range(5):
                        self.main_game.sparks.append(Flame((self.rect().centerx,self.rect().centery+random.random()*4),-1*self.velocity[0]*math.pi,2+random.random())) 

                    if self.check_collision['right'] or self.check_collision['left']:
                        self.screen_shake(10)
                        self.furiously_dashing = False
                        self.velocity = [0,0]
                        for i in range(20):
                            angle = random.random()*math.pi*2
                            speed = random.random() *3
                            self.main_game.sparks.append(Flame(self.rect().center,angle,2+random.random()))
                        if random.choice([True,False]):
                            self.action_queue=[60,"prepare_attack()",40,"dash()",20,"frozen_in_air()",3,"ground_smash()",5,"screen_shake(20)"]
                        else:
                            self.froze_in_air = False
                            self.action_queue=[60,"jump()",20,"direction_shoot()",40,"direction_shoot()",80]

                else:
                    self.froze_in_air = False
                    self.action_queue=[60,"jump()",40,"frozen_in_air()",10,"air_8_shoot(1)",30,"air_8_shoot(2)",30,"air_8_shoot(1)",30,"prepare_attack()",["attack_preview()",30],5,["dash_to()",1]]
        elif self.phase == 3:
            if self.main_game.phase_3_start:
                self.timer_HP -= 1
            if self.timer_HP == 0:
                self.HP = 0
            if not self.using_spell_card and not self.froze_in_air:
                self.velocity[1] = min(7,self.velocity[1]+0.1)
            if len(self.action_queue)>0 and isinstance(self.action_queue[0],int):
                self.action_queue[0] -= 1
                if self.action_queue[0] == 0:
                    self.action_queue.pop(0)
            elif len(self.action_queue)>0 and isinstance(self.action_queue[0],list):
                if self.action_queue[0][0] == "attack_preview()":   
                    if not self.attack_preview_pos_a:
                        self.attack_preview_pos_a,self.attack_preview_pos_b = self.attack_preview()
                    else:
                        self.attack_preview(self.attack_preview_pos_a,self.attack_preview_pos_b)
                elif self.action_queue[0][0] == "dash_to()":   
                    self.dash_towards_player(self.attack_preview_pos_b)
                elif self.action_queue[0][0] == "spell_card()":
                    self.spell_card_spin(self.action_queue[0][1])
                elif self.action_queue[0][0] == "spread()":
                    self.spell_card_spread()
                self.action_queue[0][1] -= 1
                if self.action_queue[0][1] == 0:
                    self.action_queue.pop(0) 
            elif len(self.action_queue)>0:
                exec("self."+self.action_queue.pop(0))
            else:
                if self.dashing_towards_player:
                    if self.check_collision['down']:
                        self.dashing_towards_player = False
                        self.velocity = [0,0]
                        for i in range(20):
                            angle = random.random()*math.pi*2
                            speed = random.random() *3
                            self.main_game.sparks.append(Flame(self.rect().center,angle,2+random.random()))
                        self.ground_8_shoot()
                        self.froze_in_air = False

        #if player collides with enemy, player takes damage
        if self.rect().colliderect(self.main_game.player.rect()) and abs(self.main_game.player.dashing) < 50: 
            self.main_game.player.take_damage(1,self.check_player_pos())
        elif self.rect().colliderect(self.main_game.player.rect()) and abs(self.main_game.player.dashing) > 50 and "蝙蝠吊墜" in self.main_game.player.accessory:
            self.HP -= self.main_game.player.damage
            self.main_game.sfx['hit'].play()
            for i in range(10):
                angle = random.random()*math.pi*2
                speed = random.random() *5
                self.main_game.sparks.append(Gold_Flame(self.rect().center,angle,2+random.random()))  
                self.main_game.particles.append(Particle(self.main_game,'particle',self.rect().center,[math.cos(angle+math.pi)*speed*0.5,math.sin(angle+math.pi)*speed*0.5],frame=random.randint(0,7)))  
            if self.HP <= 0:
                return True
        if self.dashing_towards_player or self.furiously_dashing or self.air_dashing or self.dashing:
            self.set_action('dash')
        elif abs(movement[0]) > 0:
            self.set_action('run')
        elif self.jumping:
            self.set_action('jump')
        else:
            self.set_action('idle') 

        if self.HP <= 0:
            return True
        super().update(movement,tilemap)

    def check_player_pos(self):
        return list((self.main_game.player.rect().centerx - self.rect().centerx, self.main_game.player.rect().centery - self.rect().centery))
    
    def prepare_attack(self,variant=0):
        if variant == 0:
            for i in range (20):
                #flame effect
                angle = random.random()*math.pi*2
                self.main_game.sparks.append(Flame(self.rect().center,angle,2+random.random()))
        elif variant == 1:
            for i in range (40):
                #flame effect
                angle = random.random()*math.pi*2
                color_code = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
                self.main_game.sparks.append(Flexible_Spark(self.rect().center,angle,2+random.random(),color_code))
    def dash(self):
        #boss will move towards player's direction at a high speed for a short duration
        self.dashing = True
        distance = self.check_player_pos()  
        if distance[0] > 0:
            self.velocity[0] = 5
        else:
            self.velocity[0] = -5

    def furiously_dash(self):
        #boss will move towards player's direction at a high speed for a short duration
        distance = self.check_player_pos()  
        self.furiously_dashing = True
        if distance[0] > 0:
            self.velocity[0] = 10
        else:
            self.velocity[0] = -10
    def air_dash(self):
        #boss will move towards player's direction at a high speed for a short duration
        distance = self.check_player_pos()
        if distance[0] > 0:
            self.velocity[0] = 5
        else:
            self.velocity[0] = -5
        self.air_dashing = True
    def land_shoot(self):
        self.main_game.projectiles.append([[self.rect().centerx-7,self.rect().centery],-1.5,0])
        self.main_game.projectiles.append([[self.rect().centerx-7,self.rect().centery-7],-1.5,-1.5])
        self.main_game.projectiles.append([[self.rect().centerx+7,self.rect().centery-7],1.5,1.5])
        self.main_game.projectiles.append([[self.rect().centerx+7,self.rect().centery],1.5,0])
        for i in range(30):
            angle = random.random()*math.pi*2
            self.main_game.sparks.append(Flame(self.rect().center,angle,2+random.random()))  

    def normal_shoot(self):
        self.main_game.sfx['shoot'].play()
        distance = (self.main_game.player.rect().centerx - self.rect().centerx, self.main_game.player.rect().centery - self.rect().centery)
        if True:  
            if(self.flip and distance[0] < 0): #player is to the left and enemy is facing left
                self.main_game.projectiles.append([[self.rect().centerx-7,self.rect().centery],-1.5,0])
                for i in range(4):
                    self.main_game.sparks.append(Spark(self.main_game.projectiles[-1][0],random.random()+math.pi-0.5,2+random.random()))
            elif(not self.flip and distance[0] > 0): #player is to the right and enemy is facing right
                self.main_game.projectiles.append([[self.rect().centerx+7,self.rect().centery],1.5,0])
                for i in range(4):
                    self.main_game.sparks.append(Spark(self.main_game.projectiles[-1][0],random.random()-0.5,2+random.random()+2))
            
                        
    def jump(self):
        #boss will jump and dash towards player's direction after a short delay
        self.velocity[1] = -4
        self.jumping = True
    def drop_attack(self):
        #boss will drop down and land, dealing damage to player if player is below
        self.velocity[1] = 7
        self.main_game.sparks.append(Spark(self.rect().center, 1.5*math.pi, 5+random.random()))


    def combo(self):
        if self.attack_combo == 1:
            self.action_queue = ["jump()",["empty",30],"frozen_in_air()","air_dash()",["aim_drop",30],"drop_attack()",["land_detect",60],"land_shoot()",["empty",30],["empty_walk",60],300]
        elif self.attack_combo == 2:
            if random.random() > 0.7:
                self.action_queue = ["prepare_attack()",["empty",55],"dash()",["empty",10],"frozen_in_air()","normal_shoot()",["empty",20],"normal_shoot()",["empty",20],"normal_shoot()",["empty",20],"normal_shoot()",["empty",140],["empty_walk",60],300]
            else:   
                self.attack_combo = 1
                self.action_queue = ["prepare_attack()",["empty",55],"dash()",["empty",10],"frozen_in_air()","normal_shoot()",["empty",20],"normal_shoot()",["empty",20],"normal_shoot()",["empty",20],"normal_shoot()",["empty",100],"combo()"]

    def frozen_in_air(self):
        self.velocity = [0,0]
        self.dashing = False
        self.air_dashing = False
        self.dashing_towards_player = False
        self.furiously_dashing = False
        self.froze_in_air = True
        #if collision with ground, stop the action
        if self.check_collision['down']:
            self.froze_in_air = False

    def air_8_shoot(self,variant=0):
        #boss will shoot 8 special projectiles in all directions
        self.velocity = [0,0]
        if variant == 1:
            for i in range(8):
                angle = i * math.pi / 4
                self.main_game.special_projectiles.append(Diagnal_Projectile(self.rect().center,[math.cos(angle),math.sin(angle)],1.5,"projectile"))
                for i in range(4):
                    self.main_game.sparks.append(Spark(self.main_game.special_projectiles[-1].pos,random.random()*math.pi*2,2+random.random()))
        elif variant == 2: #rotate 22.5 degree
            for i in range(8):
                angle = i * math.pi / 4 + math.pi/8
                self.main_game.special_projectiles.append(Diagnal_Projectile(self.rect().center,[math.cos(angle),math.sin(angle)],1.5,"projectile"))
                for i in range(4):
                    self.main_game.sparks.append(Spark(self.main_game.special_projectiles[-1].pos,random.random()*math.pi*2,2+random.random()))
    
    def ground_8_shoot(self):
        if self.phase == 2:
            for i in range(16):
                angle = i * math.pi / 8
                self.main_game.special_projectiles.append(Diagnal_Projectile((self.rect().centerx,self.rect().centery-7),[math.cos(angle),math.sin(angle)],1.5,"projectile"))
            x_pos = self.check_player_pos()[0]
            self.action_queue = [120,"dash_back("+str(x_pos)+")",15,"frozen_in_air()",20]
            if random.choice([True,False]):
                self.action_queue.append("diag_explode_shoot()")
                self.action_queue.append(40)
            else:
                self.action_queue.append("prepare_attack()")
                self.action_queue.append(40)
                self.action_queue.append("furiously_dash()")
        else:
            for i in range(16):
                angle = i * math.pi / 8
                self.main_game.special_projectiles.append(Special_Projectile((self.rect().centerx,self.rect().centery-7),[math.cos(angle),math.sin(angle)],1.5,"projectile",max_timer=30,type="small_explode",main_game=self.main_game))
            self.action_queue=[60,"jump()",20,"frozen_in_air()",10,"prepare_attack(1)",60,["spell_card()",80],90,"air_dash()",25,"frozen_in_air()",10,["spell_card()",80],90,["spread()",15],90,"prepare_attack()",["attack_preview()",30],5,["dash_to()",1]]
            self.set_action('jump')

    def diag_explode_shoot(self):
        relavtive_pos = self.check_player_pos()
        relavtive_pos[1] = -60
        self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[relavtive_pos[0],relavtive_pos[1]],3,"projectile",max_timer=50,type="explode_shoot",main_game=self.main_game))
        relavtive_pos[1] = -40
        self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[relavtive_pos[0],relavtive_pos[1]],3.5,"projectile",max_timer=50,type="explode_shoot",main_game=self.main_game))
        relavtive_pos[1] = -20
        self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[relavtive_pos[0],relavtive_pos[1]],4,"projectile",max_timer=50,type="explode_shoot",main_game=self.main_game))
        if True:  
            if(self.flip): #player is to the left and enemy is facing left
                for i in range(4):
                    self.main_game.sparks.append(Flame(self.main_game.special_projectiles[-1].pos,random.random()+math.pi-0.5,2+random.random()))
            else: #player is to the right and enemy is facing right
                for i in range(4):
                    self.main_game.sparks.append(Flame(self.main_game.special_projectiles[-1].pos,random.random()-0.5,2+random.random()+2))    

        if random.choice([True,False]):
            self.action_queue=[80,"prepare_attack()",40,"dash()",20,"frozen_in_air()",10,"ground_smash()",5,"screen_shake(20)"]
        else:
            self.froze_in_air = False
            self.action_queue=[80,"jump()",20,"direction_shoot()",40,"direction_shoot()",80]
    
    def direction_shoot(self,direction=[0,0]):
        #boss will shoot a projectile towards player's direction
        if direction==[0,0]:
            direction = self.check_player_pos()
        self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,direction,2,"projectile",max_timer=30,type="explode_shoot",main_game=self.main_game))
        for i in range(4):
            self.main_game.sparks.append(Spark(self.position,random.random()-0.5,2+random.random()+2))

    def ground_smash(self):
        for i in range(20):
            if self.flip:
                self.main_game.sparks.append(Flame((self.rect().center[0]+random.randint(-6,6)-20,self.rect().center[1]-40), -1.5*math.pi, 3+random.random()))
                #check if player is hit
                if self.main_game.player.rect().colliderect(pygame.Rect(self.rect().center[0]-36,self.rect().center[1]-40,24,40)):
                    self.main_game.player.take_damage(1)
            else:
                self.main_game.sparks.append(Flame((self.rect().center[0]+random.randint(-6,6)+20,self.rect().center[1]-40), -1.5*math.pi, 3+random.random()))
                #check if player is hit
                if self.main_game.player.rect().colliderect(pygame.Rect(self.rect().center[0]+20,self.rect().center[1]-40,24,40)):
                    self.main_game.player.take_damage(1)
        
        
    
    def screen_shake(self,frame):
        self.main_game.screen_shake_timer = max(frame,self.main_game.screen_shake_timer)

    def attack_preview(self,pos_a=(0,0),pos_b=(0,0)):
        #draw a red line from pos_a to pos_b
        if pos_a == (0,0) and pos_b == (0,0):
            pos_a,pos_b =(self.rect().centerx,self.rect().centery),(self.main_game.player.rect().centerx,self.main_game.player.rect().centery+7)
        pygame.draw.line(self.main_game.display,(255,0,0),(pos_a[0]-self.main_game.render_camera[0],pos_a[1]-self.main_game.render_camera[1]),(pos_b[0]-self.main_game.render_camera[0],pos_b[1]-self.main_game.render_camera[1]),1)
        return pos_a,pos_b

    def dash_towards_player(self,end_pos=(0,0)):
        #dash diagnaly towards end_pos
        self.dashing_towards_player = True
        direction = (end_pos[0]-self.rect().centerx,end_pos[1]-self.rect().centery)
        direction_length = math.sqrt(direction[0]**2 + direction[1]**2)
        direction = (direction[0]/direction_length,direction[1]/direction_length)   
        self.velocity = [direction[0]*10,direction[1]*10]
        self.attack_preview_pos_a,self.attack_preview_pos_b = None,None

    def dash_back(self,relative_pos):
        #dash away from player
        if relative_pos > 0:
            self.velocity = [-4,0]
        else:
            self.velocity = [4,0]

    def spell_card_spin(self,count_down_timer):
        self.using_spell_card = True
        self.set_action('jump')
        if count_down_timer <=48:
            if self.timer_HP > 1500:
                for i in range(4):
                    angle = math.pi*2/32*(97-count_down_timer)+math.pi*i/2
                    self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[math.cos(angle),math.sin(angle)],3,"projectile_"+str(count_down_timer%7+1),max_timer=40,type="two_stage_spin",main_game=self.main_game))
            elif self.timer_HP > 800:
                for i in range(6):
                    angle = math.pi*2/36*(97-count_down_timer)+math.pi*i/3
                    self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[math.cos(angle),math.sin(angle)],3,"projectile_"+str(count_down_timer%7+1),max_timer=40,type="two_stage_spin",main_game=self.main_game))
            else:
                for i in range(6):
                    angle = math.pi*2/32*(97-count_down_timer)+math.pi*i/3
                    self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[math.cos(angle),math.sin(angle)],3,"projectile_"+str(count_down_timer%7+1),max_timer=40,type="two_stage_spin",main_game=self.main_game))
                
        else:
            #shoot a completely random direction projectile
            for i in range(2):
                self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[random.random()*2-1,random.random()*2-1],1,"projectile_"+str(count_down_timer%7+1),max_timer=70,type="two_stage_",main_game=self.main_game))

    def spell_card_spread(self):
        for i in range(3):
            self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[random.random()*2-1,random.random()*2-1],1,"projectile",max_timer=30,type="small_explode",main_game=self.main_game))
            #self.main_game.special_projectiles.append(Special_Projectile(self.rect().center,[random.random()*2-1,random.random()*2-1],1,"fireball",max_timer=30,type="small_explode",main_game=self.main_game))

    def cut_in(self):
        self.main_game.cutscene_timer = 120

    def render(self,surface,offset=[0,0]):
        super().render(surface,offset)

class obstacle(physics_entity):
    def __init__(self, main_game, entity_type, position, size):
        super().__init__(main_game, entity_type, position, size)
        self.render_type = 'obstacle'
        self.check_pos_reult = [0,0]
        self.HP = 1
    def check_player_pos(self):
        return list((self.main_game.player.rect().centerx - self.rect().centerx, self.main_game.player.rect().centery - self.rect().centery))

    def render(self,surface,offset=[0,0]):
        if abs(self.check_pos_reult[0]) < 250:
            super().render(surface,offset)
    
    def update(self, movement=(0, 0), tilemap=None):
        self.check_pos_reult = self.check_player_pos()
        if self.check_pos_reult[0] > 200:
            return True
        if abs(self.check_pos_reult[0]) < 200:
            super().update(movement, tilemap)


class Beam(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'beam',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'beam'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            self.main_game.player.take_damage(1,self.check_player_pos())
        return super().update(movement,tilemap)
        

class Box(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'box',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'box'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.HP <= 0:
            self.main_game.scrap += 2
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            if self.main_game.player.velocity[1] > 9 and "sword" in self.main_game.tools:
                self.HP -= 1
                self.main_game.sfx['hit'].play()
                for i in range(10):
                    angle = random.random()*math.pi*2
                    speed = random.random() *5
                    self.main_game.sparks.append(Gold_Flame(self.rect().center,angle,2+random.random()))  
                    self.main_game.particles.append(Particle(self.main_game,'particle',self.rect().center,[math.cos(angle+math.pi)*speed*0.5,math.sin(angle+math.pi)*speed*0.5],frame=random.randint(0,7)))  
            else:
                self.main_game.player.take_damage(1,self.check_player_pos())

        return super().update(movement,tilemap)
    
class Spike(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'spike',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'spike'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            self.main_game.player.take_damage(1,self.check_player_pos())

        return super().update(movement,tilemap)
        
class pillar(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'pillar',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'pillar'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            self.main_game.player.take_damage(1,self.check_player_pos())

        return super().update(movement,tilemap)
        
class Scrap(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'scrap',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'scrap'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            #play coin sfx
            self.main_game.sfx['coin'].play()
            self.main_game.scrap += 1
            self.main_game.player.score += 1
            #remove the scrap
            return True
        return super().update(movement,tilemap)
    
class Hook_start(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'hook_start',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'hook_start'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            return True
        return super().update(movement,tilemap)

class Hook_stop(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'hook_stop',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'hook_stop'        
        self.used = False

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            return True
        return super().update(movement,tilemap)
        
class Tutorial_trigger(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'trigger',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'trigger'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            return True
        return super().update(movement,tilemap)
    
class Knife(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'trigger',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'knife'

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if abs(self.check_player_pos()[0]) <= 300:
            self.main_game.projectiles.append([self.position,-2,1,"knife"])
            return True
        return super().update(movement,tilemap)

class Cutscene_trigger(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'cut_trigger',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'cut_trigger'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            return True
        return super().update(movement,tilemap)
    
class Camera_trigger(obstacle):
    def __init__(self,main_game,position,size,velocity=[0,0],duration=0):
        super().__init__(main_game,'camera_trigger',position,size)
        self.duration = duration
        self.velocity = velocity
        self.anim_offset = [0,0]
        self.type = 'camera_trigger'        

    def update(self,movement=(0,0),tilemap=None):
        self.duration -= 1
        if self.duration == 0:
            return True
        if self.rect().colliderect(self.main_game.player.rect()): 
            return True
        return super().update(movement,tilemap)
        
