import pygame
from player import Player
from settings import WIDTH, HEIGTH, TIELSIZE, screeen
from sprite import ColisionSprite, GroundSprinte
from random import randint, randrange
from os.path import join
from pytmx.util_pygame import load_pygame
#






class Game():

    def __init__(self):
        self.runing = True
        self.bacground = "purple"
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick(60) / 1000
        self.player = None 
        self.setup()

    def game_loop(self):

        while self.runing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                     self.runing = False
            self.update()
            screeen.fill(self.bacground)
            self.draw()
            pygame.display.flip()
        pygame.quit()
    
    def update(self):
        self.player.update(self.dt)
        pass

    def draw(self):
        GroundSprinte.group.draw(screeen, self.player.rect.center) 
        Player.group.draw(screeen, self.player.rect.center)
        ColisionSprite.group.draw(screeen,self.player.rect.center )
        

    def setup(self):
        map = load_pygame(join("data", "maps", "world.tmx"))
        for object in map.get_layer_by_name("Collisions"):
            ColisionSprite(ColisionSprite.mapgroup, pos=( object.x, object.y), surface=pygame.Surface(size=(object.width, object.height)))

        for object in map.get_layer_by_name("Objects"):
            ColisionSprite(ColisionSprite.group, pos=(object.x,object.y), surface=object.image )

     
        for (x, y, image) in map.get_layer_by_name("Ground").tiles():
             GroundSprinte(GroundSprinte.group, pos=( x * TIELSIZE, y * TIELSIZE), image=image)
        
        for  object in map.get_layer_by_name("Entities"):
            if object.name == "Player":
                print("hola")
                self.player = Player(Player.group, collision_sprites=ColisionSprite.group, map_colitions=ColisionSprite.mapgroup, pos=(object.x, object.y))
    

    def create_colition_instances(self):
        for sp in range(6):
            x, y = randrange(WIDTH), randrange(HEIGTH)
            w, h  = randint(60, 100), randint(60, 100)
            ColisionSprite(ColisionSprite.group, pos=(x,y), size=(w,h) )




new_game = Game()
new_game.game_loop()