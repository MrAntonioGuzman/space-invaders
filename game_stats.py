import random


class GameStats:
    def __init__(self, settings, high_scores):
        self.settings = settings
        self.high_scores = high_scores
        self.high_score = self.high_scores.get_high_score()
        #self.reset_stats()
        self.game_active = False
        self.scores_menu = False
        self.game_over = False
        self.score = 0
        self.level = 1

        self.ship_hit = False
        self.ships_left = settings.ship_limit

        self.boss_level = random.randint(4, 7)
        self.fleet_level = 0
        self.spawn_boss = False

    def reset_stats(self, high_score):
        self.spawn_boss = random.randint(4, 7)
        self.fleet_level = 0
        self.ships_left = self.settings.ship_limit
        self.high_score = self.high_scores.get_high_score()
        self.score = 0

    def update_fleet_level(self):
        self.fleet_level += 1

    def boss_ready(self):
        return self.fleet_level >= self.boss_level

    def get_score(self):
        return self.score
    
    

