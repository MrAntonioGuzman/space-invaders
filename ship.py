import pygame
from pygame.sprite import Sprite



class Ship(Sprite):
    def __init__(self, settings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.settings = settings
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.center = float(self.rect.centerx)
        self.moving_right = False
        self.moving_left = False

 
        self.img_dims = (60, 48)
        self.animation_time = 0.04
        self.current_time = 0

        self.exp_1 = pygame.image.load('images/ship_exp_1.png').convert_alpha()
        self.exp_2 = pygame.image.load('images/ship_exp_2.png').convert_alpha()
        self.exp_3 = pygame.image.load('images/ship_exp_3.png').convert_alpha()
        self.exp_4 = pygame.image.load('images/ship_exp_4.png').convert_alpha()
        self.exp_5 = pygame.image.load('images/ship_exp_5.png').convert_alpha()
        self.exp_6 = pygame.image.load('images/ship_exp_6.png').convert_alpha()
        self.exp_7 = pygame.image.load('images/ship_exp_7.png').convert_alpha()
        self.exp_8 = pygame.image.load('images/ship_exp_8.png').convert_alpha()

        self.exp_1 = pygame.transform.scale(self.exp_1, self.img_dims)
        self.exp_2 = pygame.transform.scale(self.exp_2, self.img_dims)
        self.exp_3 = pygame.transform.scale(self.exp_3, self.img_dims)
        self.exp_4 = pygame.transform.scale(self.exp_4, self.img_dims)
        self.exp_5 = pygame.transform.scale(self.exp_5, self.img_dims)
        self.exp_6 = pygame.transform.scale(self.exp_6, self.img_dims)
        self.exp_7 = pygame.transform.scale(self.exp_7, self.img_dims)
        self.exp_8 = pygame.transform.scale(self.exp_8, self.img_dims)
        
        self.explosion_imgs = [
            self.exp_1,
            self.exp_2, 
            self.exp_3,
            self.exp_4, 
            self.exp_5,
            self.exp_6,
            self.exp_7,
            self.exp_8            
        ]
        self.exp_img_length = 0
        self.exp_done = False
        self.hit = False
        self.alive = True
        self.i = 0

    def is_hit(self):
        self.hit = True  
        self.alive = False

    def reset_hit(self):
        self.alive = True
        self.exp_done = False
        self.image = pygame.image.load('images/ship.bmp')
        self.exp_img_length = 0

    def is_exp_done(self):
        return self.exp_done

    def center_ship(self):
        self.center = self.screen_rect.centerx
    
    def update(self, dt):
        if self.hit:
            self.current_time += dt
            if self.current_time >= self.animation_time:
                self.current_time = 0
                if len(self.explosion_imgs) - 1 > self.exp_img_length:
                    self.image = self.explosion_imgs[self.exp_img_length]
                    self.exp_img_length += 1
                else:
                    #self.image = pygame.image.load('images/ship.bmp')
                    #self.exp_img_length = 0
                    #self.exp_done = True
                    #self.kill()
                    self.hit = False
    
        elif self.alive:
            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.center += self.settings.ship_speed_factor
            
            if self.moving_left and self.rect.left > 0:
                self.center -= self.settings.ship_speed_factor
            
            self.rect.centerx = self.center


    def blitme(self):
        if self.exp_img_length == 7:
            pygame.draw.rect(self.screen, self.settings.bg_color, self.rect)
        else:
            self.screen.blit(self.image, self.rect)

        