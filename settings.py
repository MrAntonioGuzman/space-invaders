import pygame


class Settings:
    def __init__(self):
        self.dims = 1200, 700
        self.bg_color = (230, 230, 230)

        self.ship_speed_factor = 15
        self.ship_limit = 1     # Original value = 3

        self.bullet_speed_factor = 10
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        self.alien_speed_factor = 3    # Original value=1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.alien_bullets_allowed = 10 # 4 Bullets per row
        self.alien_bullet_speed_factor = 2

        self.music = ['level_1.mid', 'level_2.wav', 'level_3.wav']
        self.music_level = 0

        self.initialize_dynamic_settings()

    def play_music(self):
        pygame.mixer.music.load(self.music[self.music_level])
        pygame.mixer.music.play(-1, 0.0)

    
    def update_music(self):
        self.stop_music()
        self.music_level += 1
        self.play_music()

    
    def stop_music(self):
        pygame.mixer.music.stop()
    

    def reset_music(self):
        self.music_level = 0

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 15
        self.bullet_speed_factor = 10
        self.alien_speed_factor = 3     # Original value = 3
        self.fleet_direction = 1
        self.alien_points = 50
        
        self.alien_1_points = 10
        self.alien_2_points = 20
        self.alien_3_points = 40

        self.play_music()
    
    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)


    def get_dims(self):
        return self.dims

    def get_bg_color(self):
        return self.bg_color

