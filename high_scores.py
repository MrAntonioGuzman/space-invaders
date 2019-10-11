import pygame
from collections import OrderedDict
from text import Text

# Size should be 62
class HighScores:
    def __init__(self, screen, settings, color, size):
        self.screen = screen
        self.settings = settings
        self.color = color
        self.size = size

        self.back_text = Text(self.color, self.size, 'BACK', self.screen)
        self.back_button = pygame.Rect(0, 0, 200, self.back_text.get_rect().height + 50)
        self.back_text.get_rect().center = self.back_button.center

        # {score: name}
        self.scores_dict = {
            10: 'Name1',
            11: 'Name1',
            12: 'Name1',
            13: 'Name1',
            14: 'Name1',
            15: 'Name1',
            16: 'Name1',
            17: 'Name1',
            18: 'Name1',
            19: 'Name1',
        }

        '''
            900 : 'Name1',
            400 : 'Name2',
            300 : 'Name3',
            200 : 'Name4',
            500: 'Name5',
            1000: 'Name6',
            700: 'Name7',
            800: 'Name8',
            100: 'Name9',
            600: 'Name10',
        '''

    def add(self, score):
        if len(self.scores_dict) > 10:
            self.scores_dict[score] = 'Name'
            
        else:
            scores_list = sorted(self.scores_dict.keys())
            scores_list = scores_list[::-1]
            for s in scores_list:
                if score > s:
                    #del self.scores_dict[s]
                    k = self.scores_dict.pop(scores_list[-1], None)
                    self.scores_dict[score] = 'Name'
                    return

                if score == s:
                    return
    
    def get_back_button(self):
        return self.back_button

    def get_high_score(self):
        l = sorted(self.scores_dict.keys())
        return l[-1]
    
    def draw_scores(self):
        TOMATO = (255,99,71)
        pygame.draw.rect(self.screen, TOMATO, self.back_button)
        self.back_text.blit_me()

        x, y = self.settings.get_dims()
        rect = pygame.Rect(0, 50, 600, 60)
        rect.centerx = x // 2
        i = 1
        l = sorted(self.scores_dict.keys())
        l = l[::-1]
        print(len(l))
        for k in l:
            rank_text = Text(self.color, self.size, str(i), self.screen)
            score_text = Text(self.color, self.size, str(k), self.screen)
            name_text = Text(self.color, self.size, self.scores_dict[k], self.screen)

            rank_text.get_rect().topleft = (rect.x, rect.y)
            score_text.get_rect().topleft = (rect.x + 200, rect.y)
            name_text.get_rect().topleft = (rect.x + 400, rect. y)
            
            rank_text.blit_me()
            score_text.blit_me()
            name_text.blit_me()

            rect.y += 60
            i += 1
            

            

    

