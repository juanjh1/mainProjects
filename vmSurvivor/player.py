import pygame
from os.path import join
from os import walk

import pygame.locals
from settings import WIDTH, HEIGTH
from groups import AllSprites

class Player(pygame.sprite.Sprite):
    group = AllSprites()
    def __init__(self, *groups, collision_sprites, map_colitions, pos):
        super().__init__(*groups)
        self.load_images()
        self.state, self.frame_index = "down", 0
        self.frame_down = [pygame.image.load(join("images", "player", "down", f"{img}.png")) for img in range(4)]
        self.image = self.frame_down[0]
        self.rect = self.image.get_frect(center = pos)
        self.vector = pygame.math.Vector2(0, 0)
        self.x_direction = 65
        self.collision_sprites = collision_sprites
        self.map_colitions = map_colitions
        self.hit_box_rect = self.rect.inflate(-60,-60)
    
    def input(self):
        key_presed = pygame.key.get_pressed()

        self.vector.x = int(key_presed[pygame.K_RIGHT]) - int(key_presed[pygame.K_LEFT])
        self.vector.y =  int(key_presed[pygame.K_DOWN]) - int(key_presed[pygame.K_UP])
        self.vector = self.vector.normalize() if self.vector else self.vector
        #self.vector.x = int 

        #if key_presed[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:

            #self.y_direction = -1
        #     pass
        # elif key_presed[pygame.K_DOWN] or key_presed[pygame.K_s]: 
        #     self.y_direction = 1
        # else: 
        #     self.y_direction = 0

        # if key_presed[pygame.K_d]:
        #     self.x_direction = 1
        # elif key_presed[pygame.K_a]:
        #     self.x_direction = -1
        # else:
        #     self.x_direction = 0

    def movement(self, dt):
        #self.rect.center += self.vector_y * dt * self.y_direction 
        #self.rect.center += self.vector * dt * self.x_direction

    
        self.hit_box_rect.x += self.vector.x * dt * self.x_direction
        self.rect.centerx = self.hit_box_rect.centerx
        self.collision("Horizontal")
        self.hit_box_rect.y += self.vector.y * dt * self.x_direction
        self.rect.centery = self.hit_box_rect.centery         
        self.collision("Vertical")
    
    def collision(self, direction):
        self.collition_by_group(self.collision_sprites, direction)  
        self.collition_by_group(self.map_colitions, direction)  

    def collition_by_group (self, group, direction):
           for sprite in group:
            if sprite.rect.colliderect(self.hit_box_rect):
                if(direction == "Horizontal"):
                        if self.vector.x > 0 : self.hit_box_rect.right = sprite.rect.left
                        if self.vector.x < 0: self.hit_box_rect.left = sprite.rect.right
                if direction == "Vertical":
                        if self.vector.y < 0: self.hit_box_rect.top = sprite.rect.bottom
                        if self.vector.y > 0: self.hit_box_rect.bottom = sprite.rect.top
        
    def update(self, dt):
        self.input()
        self.movement(dt)
        self.animate(dt)

    def animate(self, dt):
         move = 0
         if self.vector.x != 0:
              self.state = "right" if ( self.vector.x > 0)   else  "left"
              move = 1
         if self.vector.y != 0:
              self.state = "down" if ( self.vector.y > 0)   else  "up"
              move = 1
            
         if self.vector.x == 0 and self.vector.y == 0:
              move = 0

         #animate 
         self.frame_index += 2.5 * move*dt
         self.image = self.frames[self.state][int(self.frame_index)% len(self.frames[self.state])]

    def load_images(self):
         self.frames = {
              "left":None,
              "right":None,
              "up":None,
              "down":None
         }
         for state in self.frames.keys():           
            for folder_name , sub_folder, file_names in walk(join("images", "player", state)):
                   self.frames[state]= [ pygame.image.load(join(folder_name, value)) 
                                        for value in 
                                        sorted(file_names, key=lambda name :int(name.split(".")[0]) ) ]
                 
                 