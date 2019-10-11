import pygame
from text import Text

class GameOver:
    def __init__(self, screen, settings, stats, high_scores):
        self.screen = screen
        self.settings = settings
        self.stats = stats

        self.BG_COLOR = (0, 0, 0)
        self.TEXT_COLOR = (255, 255, 255)

        self.game_over_text = Text(self.TEXT_COLOR, 82, 'GAME OVER', screen)
        self.play_again_text = Text(self.TEXT_COLOR, 62, 'PLAY AGAIN', screen)
        self.main_menu_text = Text(self.TEXT_COLOR, 62, 'MAIN MENU', screen)

        self.rect_container = pygame.Rect(0, 0, 600, 500)
        self.x, self.y = settings.get_dims()
        self.rect_container.center = (self.x // 2, self.y // 2)

        self.high_scores = high_scores

    def get_play_again_btn(self):
        return self.play_again_text.get_rect()
    
    def get_main_menu_btn(self):
        return self.main_menu_text.get_rect()

    def check_score(self):
        self.high_scores.add(self.stats.get_score())

    def get_high_score(self):
        self.high_scores.get_high_score()
    
    def draw_menu(self):
        pygame.draw.rect(self.screen, self.BG_COLOR, self.rect_container)

        self.game_over_text.get_rect().centerx = self.rect_container.centerx
        self.game_over_text.get_rect().y = self.rect_container.y + 50

        self.main_menu_text.get_rect().centerx = self.rect_container.centerx
        self.main_menu_text.get_rect().y = self.rect_container.bottom - 100

        self.play_again_text.get_rect().centerx = self.rect_container.centerx
        self.play_again_text.get_rect().y = self.main_menu_text.get_rect().top - 50

        self.game_over_text.blit_me()
        self.main_menu_text.blit_me()
        self.play_again_text.blit_me()

