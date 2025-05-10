import pygame
import pygame.sprite
from random import randrange,uniform

WIDTH, HEIGTH = 1000, 650

surface = pygame.display.set_mode((WIDTH,HEIGTH))
pygame.display.set_caption("Particle emulator")

class Scope(pygame.sprite.Sprite):
    group = pygame.sprite.Group()
    def __init__(self, *groups, scope, pos):
        super().__init__(*groups)
        self.image = pygame.Surface((scope, scope))
        self.image.fill("red")
        self.rect = self.image.get_frect(center=pos)

    def update(self, pos):
        self.rect.center = pos
        for  Vertex in pygame.sprite.spritecollide(self, Particle.group, False):
            Edge.lines.append(Edge(self.rect.center, Vertex.rect.center))

class Particle(pygame.sprite.Sprite):
    group = pygame.sprite.Group()
    def __init__(self, *groups, pos):
        super().__init__(*groups)
        self.image = pygame.Surface((10,10))
        self.image.fill("white")
        self.rect = self.image.get_frect(center = pos)
        self.range = 200
        self.scope = Scope(scope=self.range, pos=self.rect.center)
        Scope.group.add(self.scope)
        angle = uniform(0, 360)  
        self.vector = pygame.math.Vector2(1, 0).rotate(angle)
        self.speed  = 200
    

    def update(self, dt):

        next_pos = self.rect.center + self.vector * self.speed * dt
        if next_pos[0] >= WIDTH - 5 or next_pos[1] >= HEIGTH - 5 or next_pos[0] <= 5 or next_pos[1] <= 5:
            self.vector.rotate_ip(180)
        self.rect.center += self.vector * self.speed* dt
        self.scope.update(self.rect.center)

class ParticlePlayer(Particle):
     group = pygame.sprite.GroupSingle()
     def __init__(self, *groups, pos):
         super().__init__(*groups, pos=pos)

     def update(self, *args, **kwargs):
        mouse_pos = pygame.mouse.get_pos()
        self.rect.center = mouse_pos
        self.scope.update(mouse_pos)

class Edge():
    lines = []
    @staticmethod
    def draw_lines():
        for line in Edge.lines:
            line.draw()
        Edge.lines.clear()
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.distance = pygame.math.Vector2(self.start_point).distance_to(self.end_point)
        self.color ="#CCCCCC80"
    
    def draw(self):
        if self.distance < 80:
            self.color = "white"
        pygame.draw.aaline(surface,self.color ,self.start_point, end_pos=self.end_point )
        

class Game():

    def __init__(self):
        self.running = True
        self.player = ParticlePlayer(ParticlePlayer.group, pos=(WIDTH/2, HEIGTH/2))
        self.particles = self.create_particle()
        self.clock = pygame.Clock()
        self.dt = self.clock.tick(60) / 1000

    
    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
    def run(self):
        while self.running:
            self.quit()
            self.update()
            surface.fill("black")
            self.draw()

            pygame.display.flip()
        pygame.quit()
    def update(self):
        self.player.update()
        for particle in Particle.group.sprites():
            particle.update(self.dt)
    
    def create_particle(self):
        for i in range(250):
            x,y = randrange(WIDTH), randrange(HEIGTH)
            Particle(Particle.group, pos=(x,y))          
    
    def draw(self):
        #Scope.group.draw(surface)
        Edge.draw_lines()
        for particle in ParticlePlayer.group.sprites():
            pygame.draw.circle(surface,"white",particle.rect.center, 2) 
        
        for particle in Particle.group.sprites():
            pygame.draw.circle(surface,"white",particle.rect.center, 2) 
       
if  __name__ =="__main__":
    game = Game()
    game.run()
