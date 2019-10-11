import random
import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, settings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.settings = settings
        #self.image = pygame.image.load('images/alien.bmp')
        self.exp_1 = pygame.image.load('images/alien_exp_1.png')
        self.exp_1 = pygame.transform.scale(self.exp_1, (60, 58))

        self.exp_2 = pygame.image.load('images/alien_exp_2.png')
        self.exp_2 = pygame.transform.scale(self.exp_2, (60, 58))

        self.exp_3 = pygame.image.load('images/alien_exp_3.png')
        self.exp_3 = pygame.transform.scale(self.exp_3, (60, 58))

        self.exp_4 = pygame.image.load('images/alien_exp_4.png')
        self.exp_4 = pygame.transform.scale(self.exp_4, (60, 58))


        self.explosion_imgs = [
            self.exp_1,    
            self.exp_2,
            self.exp_3,
            self.exp_4
        ]

        self.exp_img_length = 0

        self.alien_1_1 = pygame.image.load('images/alien_1_1.png')
        self.alien_1_2 = pygame.image.load('images/alien_1_2.png')
        self.alien_1_1 = pygame.transform.scale(self.alien_1_1, (60, 58))
        self.alien_1_2 = pygame.transform.scale(self.alien_1_2, (60, 58))

        self.alien_2_1 = pygame.image.load('images/alien_2_1.png')
        self.alien_2_2 = pygame.image.load('images/alien_2_2.png')
        self.alien_2_1 = pygame.transform.scale(self.alien_2_1, (60, 58))
        self.alien_2_2 = pygame.transform.scale(self.alien_2_2, (60, 58))

        self.alien_3_1 = pygame.image.load('images/alien_3_1.png')
        self.alien_3_2 = pygame.image.load('images/alien_3_2.png')
        self.alien_3_1 = pygame.transform.scale(self.alien_3_1, (60, 58))
        self.alien_3_2 = pygame.transform.scale(self.alien_3_2, (60, 58))

        self.alien_list = [(self.alien_1_1, self.alien_1_2), (self.alien_2_1, self.alien_2_2), (self.alien_3_1, self.alien_3_2)]
        self.alien_type = random.choice(self.alien_list)
        self.image = self.alien_type[0]
        self.starting_image = True

        self.ufo = pygame.image.load('images/ufo.png')
        self.ufo = pygame.transform.scale(self.ufo, (100, 58))

        self.rect = self.alien_1_1.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

        self.animation_time = 0.3
        self.current_time = 0

        self.hit = False


    def alien_hit(self):
        self.hit = True
        self.animation_time = 0.07


    def get_points(self):
        if self.alien_type == self.alien_list[0]:
            return 10

        if self.alien_type == self.alien_list[1]:
            return 20

        if self.alien_type == self.alien_list[2]:
            return 40


    def get_rect(self):
        return self.rect


    def get_next_image(self):
        if self.starting_image:
            self.image = self.alien_type[0]
        else:
            self.image = self.alien_type[1]


    def change_image(self):
        self.starting_image = not self.starting_image

    
    def change_exp_image(self):
        self.image = self.explosion_imgs[self.exp_img_length]
        self.exp_img_length += 1


    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True


    def update(self, dt):
        self.x += (self.settings.alien_speed_factor * self.settings.fleet_direction)
        self.rect.x = self.x

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            if self.hit:
                if len(self.explosion_imgs) - 1 > self.exp_img_length:
                    self.change_exp_image()
                else:
                    self.kill()
            else:
                self.change_image()
                self.get_next_image()
    
    def next_image(self):
        self.change_image()
        self.get_next_image()


    def blitme(self):
        self.screen.blit(self.alien_1_1, self.rect)

