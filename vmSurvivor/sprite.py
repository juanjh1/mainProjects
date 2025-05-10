from settings import *

import pygame 

from groups import AllSprites

class ColisionSprite(pygame.sprite.Sprite):
    group = AllSprites()
    mapgroup = pygame.sprite.Group()
    def __init__(self, *groups,pos, surface ):
        super().__init__(*groups)
        self.image =  surface
        self.rect = self.image.get_frect(topleft=pos)

class GroundSprinte(pygame.sprite.Sprite):
    group = AllSprites()
    def __init__(self, *groups, pos, image ):
        super().__init__(*groups)
        self.image = image
        self.rect = self.image.get_frect(topleft=pos)