import random

import pygame

from pygame import Vector2

screen_size = Vector2(800, 600)

class Particle:
    
    cached_images = {}
    
    def __init__(self, pos, vel, size, color):
        self.pos = Vector2(pos)
        self.vel = Vector2(vel)
        
        self.size = size
        self.color = color

        self.update_image()

    def update(self, dt):
        self.pos += self.vel * dt
        
        if self.pos.x < 0:
            self.pos.x = 0
            self.vel.x *= -1
            
        elif self.pos.x > screen_size.x:
            self.pos.x = screen_size.x
            self.vel.x *= -1
            
        if self.pos.y < 0:
            return 1
            # self.pos.y = 0
            # self.vel.y *= -1
            
        elif self.pos.y > screen_size.y:
            return 0
            # self.pos.y = screen_size.y
            # self.vel.y *= -1
        
        return 1
        
    def update_image(self):
        
        cache_lookup = (self.size, self.color)
        
        if not (cached_image := self.cached_images.get(cache_lookup, None)):
            cached_image = pygame.Surface((self.size, 3 * self.size))
            cached_image.fill(self.color)
            
            self.cached_images[cache_lookup] = cached_image
            
        self.image = cached_image

class ParticleManager:
    def __init__(self):
        self.particles = []
        
    def update(self, dt):
        self.particles = [particle for particle in self.particles if particle.update(dt)]
    
    def add(self, particles):
        self.particles.extend(particles)

    def draw(self, surface):
        surface.fblits([(particle.image, particle.pos) for particle in self.particles])
    
    def __len__(self):
        return len(self.particles)

class Game:
    def __init__(self):
        pygame.init()
        
        self.clock = pygame.time.Clock()
        self.running = False
        
        self.pm = ParticleManager()
        
        self.screen = pygame.display.set_mode(screen_size, flags = pygame.SCALED)
        
    def update(self, dt):
        
        if self.fps > 60:
        
            self.pm.add([Particle((random.randint(0, screen_size.x), -10),
                                (0, 300),
                                random.randint(1, 3),
                                random.choice(['darkblue', 'blue', 'darkblue']))
                        for _ in range(10)])
        
        self.pm.update(dt)
    
    def draw(self, surface):
        
        surface.fill('black')
        
        self.pm.draw(surface)
        
        pygame.display.flip()
        
    def run(self):
        
        self.running = True
        
        while self.running:
            
            dt = self.clock.tick() * .001
            self.fps = self.clock.get_fps()
            pygame.display.set_caption(f'Particles: {len(self.pm)} FPS: {self.fps}')
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.update(dt)
            self.draw(self.screen)
        
if __name__ == '__main__':
    Game().run()