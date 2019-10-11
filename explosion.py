import time
import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    def __init__(self, screen, explosions, rect):
        super(Explosion, self).__init__()
        self.screen = screen
        self.explosions = explosions
        self.current_image = 0
        self.rect = rect

        self.animation_time = 0.1
        self.current_time = 0
    
    def update(self, dt):
        if current_image > len(self.explosions) - 1:
            self.current_time += dt        
            if self.current_time >= self.animation_time:
                print('inside: {}'.format(str(self.current_image)))
                self.current_time = 0
                self.draw_exp()
                self.current_image += 1
            
    
    def draw_exp(self):
        self.screen.blit(self.explosions[self.current_image], self.rect)

    def reset(self):
        self.current_image = 0
