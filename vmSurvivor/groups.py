import pygame
from settings import WIDTH, HEIGTH



class AllSprites(pygame.sprite.Group):

    def __init__(self ):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
    
    def draw(self, surface, target):
        self.offset.x = -(target[0] - WIDTH/2)
        self.offset.y = -(target[1] - HEIGTH/2)

        for sprite in sorted(self, key=lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect.topleft + self.offset)