import random
import pygame
from pygame.sprite import Sprite
from text import Text


class BossAlien(Sprite):
    def __init__(self, settings, screen):
        super(BossAlien, self).__init__()
        self.settings = settings
        self.screen = screen
        self.image = pygame.transform.scale(pygame.image.load('images/ufo.png'), (80, 58))
        self.rect = self.image.get_rect()
        self.original_rect = self.image.get_rect()
        self.rect.x = 101
        self.rect.y = 0
        self.speed = 8
        self.y = 1
        self.dead = None
        self.bullets = 5
        self.trigger_shoot = [205, 405, 605, 805, 1005]
        self.score = 0

        self.color = (255, 0, 0)
        self.size = 50


    def display_score(self):
        self.score = str(self.generate_score())
        self.score = '+100'
        font = Text(self.color, self.size, self.score, self.screen)
        font_rect = font.get_rect()
        font_rect.center = self.rect.center
        font.blit_me()


    def get_rect(self):
        return self.rect 


    def get_bullets(self):
        return self.bullets


    def generate_score(self):
        return random.randint(100, 125)


    def update(self):
        
        if self.rect.y == 455:
            self.y *= -1
        
        if self.rect.y == 113 and self.y < 0:
            self.y *= -1

        if self.rect.x <= 100:
            self.speed *= -1
           
        if self.rect.x >= 1000:
            self.speed *= -1
            
        self.rect.x += self.speed
        self.rect.y += self.y


    def draw(self):
        self.update()
        self.screen.blit(self.image, self.rect)
        

    def shoot(self):
        return self.rect.x in self.trigger_shoot


    def reset_spawn(self):
        self.rect = self.original_rect
        self.rect.x = 101
        self.rect.y = 0


    def died(self):
        #self.display_score()
        self.dead = True
