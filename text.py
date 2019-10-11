import pygame


class Text:
    def __init__(self, color, size, text, screen, background=None):
        self.screen = screen
        self.font = pygame.font.Font(None, size)
        self.text = self.font.render(text, True, color, background)
        self.rect = self.text.get_rect()


    def get_rect(self):
        return self.rect


    def update(self, rect):
        self.rect = rect


    def blit_me(self):
        self.screen.blit(self.text, self.rect)
