import pygame
from os.path import join
from random import randrange, uniform

#const
WIDTH, HEIGHT = 1000, 650
COORD_Y = 1



EXPLOSION_IMG = [  pygame.image.load(join( "assets", "explosion",str(i)+".png")) for i in range(21)]


class Player(pygame.sprite.Sprite):
     
     def __init__(self, *groups):
          super().__init__(*groups)
          self.image = pygame.image.load(join("assets", "player.png")).convert_alpha()
          self.rect = self.image.get_rect(center=(WIDTH//2 , HEIGHT - 150))
          self.vector = pygame.math.Vector2(220,0)
          self.laser_last_time_shoted = 0 
          self.cooldown = False
          self.aceleration = 0.1
          self.mask = pygame.mask.from_surface(self.image)
          self.laser_sound = pygame.mixer.Sound(join("music", "laser.wav"))
          
     def update(self,time):
             direction = 0  
             if pygame.key.get_pressed()[pygame.K_LEFT] and self.rect.x > 0 - self.image.width /2  :
                  direction = -1
                  self.aceleration += 0.3
             else:
                    self.aceleration = 0.1
             if pygame.key.get_pressed()[pygame.K_RIGHT] and self.rect.right < WIDTH + self.image.width/2 :
                  direction = 1
                  self.aceleration += 0.3
             else:
                  self.aceleration = 0.1
             self.rect.center += (self.vector + (self.vector * self.aceleration) )  * (dt/1000) * direction

             if(pygame.sprite.spritecollide(self, Meteor.meteor_list, False, pygame.sprite.collide_mask)):
                  return True
          
            
            #  if direction == 1 and self.rect.right > WIDTH + 3:
            #      direction = 0
            #  if direction == -1 and self.rect.left < 0:
            #     direction = 0
             
             
             self.fire_the_laser(time)

    
     def fire_the_laser(self, time):
        if not self.cooldown:
            if pygame.key.get_just_pressed()[pygame.K_SPACE]: 
              self.laser_sound.play()
              self.laser_last_time_shoted = time                   
              Laser(Laser.lasers,current_player_pos=(player.rect.center))
              self.cooldown = True
        else:
             if (time - self.laser_last_time_shoted)/1000 > 0.5:
                   self.cooldown = False
                   self.fire_the_laser(time)

class Laser(pygame.sprite.Sprite):
     lasers = pygame.sprite.Group()
     def __init__(self, *groups, current_player_pos):
          super().__init__(*groups)
          self.image = pygame.image.load(join("assets", "laser.png"))
          self.rect= self.image.get_frect(midbottom =current_player_pos)
          self.vector = pygame.math.Vector2(0,250)
          self.mask = pygame.mask.from_surface(self.image)
          self.sound_ex = pygame.mixer.Sound(join("music", "explosion.wav"))
     
     def remove_lasers_out_secreen(self):
            if laser.rect.centery <  -100:
                Laser.lasers.remove(laser)

     def update(self,dt):
         self.rect.center -= self.vector * dt/1000 
         self.remove_lasers_out_secreen()
         meteor = pygame.sprite.spritecollide(self,Meteor.meteor_list, False)
         if len(meteor) != 0 :
              self.sound_ex.play(0)
              AnimatedExplosion(AnimatedExplosion.explosions,pos=meteor[0].rect.center,frames=EXPLOSION_IMG )
              meteor[0].kill()
              self.kill()
      

          
     
      
class Meteor (pygame.sprite.Sprite):
     meteor_list = pygame.sprite.Group()
     def __init__(self, *groups, start_time):
          super().__init__(*groups)
          self.original_image = pygame.image.load(join("assets", "meteor.png ")).convert_alpha()
          self.image = self.original_image
          self.rect = self.image.get_frect(center = (int(randrange(10,WIDTH -10)),int(randrange(-20,-10))))
          self.start_time = start_time
          self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
          self.speed = 200
          self.mask = pygame.mask.from_surface(self.image)
          self.speed_r= randrange(1,3)
          self.current_angle = 0
     def update(self, time, dt):
         self.rect.center += self.direction * (dt/1000) * self.speed
         if (pygame.time.get_ticks()//100) % self.speed_r == 0:
              self.image = pygame.transform.rotate(self.original_image, angle=self.current_angle)
              if self.current_angle <= 360:
                    self.current_angle += 3
              else:
                   self.current_angle = 0
              self.rect = self.image.get_rect(center=self.rect.center)
              
         if(self.rect.x  <= 0 or self.rect.right >= WIDTH):
             self.direction.x = self.direction.x * -1
         if  self.rect.y > HEIGHT + 100:
              self.kill()


class AnimatedExplosion(pygame.sprite.Sprite):
     explosions = pygame.sprite.Group()
     def __init__(self, *groups, frames, pos):
          super().__init__(*groups)
          self.image = frames[0]
          self.buffer = frames
          self.rect = self.image.get_frect(center=pos)
          self.frame = 0
        
     def update(self,dt ):
          self.frame += 20 *dt/1000
          if self.frame >= len(self.buffer):
               self.kill()
               return
          self.image = self.buffer[int(self.frame)] 
          
def display_score():
     current_time = pygame.time.get_ticks()//1000
     font_none = pygame.font.Font(join("assets", "Oxanium-Bold.ttf"), 20)
     text_surf = font_none.render(str(current_time), True, "white")
     text_rect = text_surf.get_rect(midbottom = (WIDTH/2, HEIGHT -50  ))
     pygame.draw.rect(dispay_surface, "white", (text_rect.left - text_rect.width , text_rect.top - text_surf.height + text_rect.height/2, text_rect.width *3 , text_rect.height*2), 5, 10)
     dispay_surface.blit(text_surf, text_rect)

pygame.init()
dispay_surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("monda abarcadora")
runing:bool = True
Game_loop_music = pygame.mixer.music.load(join("music", "game_music.wav"))

pygame.mixer.music.set_volume(0.1)





clock = pygame.time.Clock()


# Import imgs 
#METOR_IMG = pygame.image.load(join("assets", "meteor.png ")).convert_alpha()
STARS_IMG = pygame.image.load(join("assets", "star.png")).convert_alpha()


### rects
#metor_rect = METOR_IMG.get_frect(center = (WIDTH/2 , HEIGHT/2))
#player_rect = PLAYER_IMG.get_frect(center =(PLAYER_IMG.get_width()//2 , 600))


#vectoes 

   

starts_img = []
for star in range(20):
    starts_img.append((int(randrange(1000)),int(randrange(650))))

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)

#color vaiables
surf = pygame.Surface((100,200))
surf.fill("#7E57C2")

#bucle helpers 
moving_right = False
moving_left = False
direction = 0


meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 2000)


#font 

pygame.mixer.music.play(-1)



while (runing):
    
     #timers
     dt = clock.tick(60)
     time = pygame.time.get_ticks()
     
     events = pygame.event.get()
     for event in events:
        if pygame.QUIT == event.type:
            runing = False

        if event.type == meteor_event:
             Meteor(Meteor.meteor_list, start_time=time)
             #print("disparale a ese cara de monda")
        # if pygame.KEYDOWN == event.type:
        #     #print(event.key)
        #     if event.key == pygame.K_RIGHT and not moving_left:
        #         direction = 1
        #     if event.key == pygame.K_LEFT and not moving_right:
        #         direction = -1
            # if event.key == pygame.K_SPACE:
            #     print(player_rect.centerx , player_rect.top)
            #     lasers.append(pygame.FRect((player_rect.centerx , player_rect.y),(LASER_IMG.get_frect().center)))

        if pygame.KEYUP == event.type:
                if event.key == pygame.K_RIGHT:
                    direction = 0
                if event.key == pygame.K_LEFT:
                    direction = 0

     for meteor in Meteor.meteor_list.sprites():
          meteor.update(time, dt)
     if(player.update(time)):
          runing = False
     for laser in Laser.lasers.sprites():
        laser.update(dt)
     
     for animation in AnimatedExplosion.explosions.sprites():
          animation.update(dt)
     

     dispay_surface.fill("#0D1B2A") 
     for cord in starts_img:
             dispay_surface.blit(STARS_IMG, cord )
    # dispay_surface.blit(METOR_IMG, metor_rect)
    
     #if pygame.key.get_pressed()[pygame.K_SPACE]:
            #lasers.append(pygame.FRect((player_rect.centerx , player_rect.y),(LASER_IMG.get_frect().center)))
         
    #  if(len(lasers) > 0):
    #     for laser in lasers:
    #          dispay_surface.blit(LASER_IMG, laser.center)
    #          laser.center -= bulets_vector * dt/1000
     """
     if(len(lasers) > 0):
         cord_y = 1
         runing = True
         index = 0
         while (index < len(lasers)):
             if(lasers[index][cord_y] < 200):
                    lasers.pop(index)
                    index -= 1;
             index += 1
     """
    #  if(len(lasers) > 0):
    #     lasers = [laser for laser in lasers if laser[COORD_Y] >= -120]
     #dispay_surface.blit(surf, (x_pos, 150-surf.height // 2 ))
     #dispay_surface.blit(PLAYER_IMG, player_rect)
     # for  meteoro in Meteor.meteor_list.sprites() :
     #      pygame.draw.rect(dispay_surface,"red ", meteoro.rect) 
     Meteor.meteor_list.draw(dispay_surface)
     Laser.lasers.draw(dispay_surface)
     AnimatedExplosion.explosions.draw(dispay_surface)
     all_sprites.draw(dispay_surface)
     display_score() 
     pygame.display.flip()

pygame.quit()