import pygame
from pygame.sprite import Sprite


class AlienBullet(Sprite):
    def __init__(self, settings, screen, alien):
        super(AlienBullet, self).__init__()
        self.color = (255, 69, 0)
        self.screen = screen
        self.rect = pygame.Rect(0, 0, settings.bullet_width+2, settings.bullet_height+10)
        self.rect.centerx = alien.get_rect().centerx
        self.rect.top = alien.get_rect().bottom
        self.y = float(self.rect.y)
        self.speed_factor = settings.alien_bullet_speed_factor

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y
    
    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
