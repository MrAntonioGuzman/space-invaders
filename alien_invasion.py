import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from pygame.sprite import GroupSingle
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from high_scores import HighScores
from game_over import GameOver
from alien import Alien
from explosion import Explosion
from high_scores import HighScores
from boss_alien import BossAlien


def run_game():
    BLACK = (0, 0, 0)
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.get_dims()))
    pygame.display.set_caption('Alien Invasion')

    #play_button = Button(screen, 'Play')
    play_button = pygame.Rect(564, 598, 72, 29)
    scores_button = pygame.Rect(502, 636, 197, 29)
    high_scores = HighScores(screen, settings, BLACK, 62)

    stats = GameStats(settings, high_scores)
    sb = Scoreboard(settings, screen, stats)
    ship = Ship(settings, screen)
    alien = Alien(settings, screen)
    boss = BossAlien(settings, screen)
    #boss = GroupSingle()
    game_over = GameOver(screen, settings, stats, high_scores)
    bullets = Group()
    aliens = Group()
    alien_explosions = Group()
    alien_bullets = Group()
    boss_bullets = Group()
    gf.create_fleet(settings, screen, ship, aliens, alien_explosions)

    FPS = 60
    clock = pygame.time.Clock()
    settings.play_music()

    


    while True:
        dt = clock.tick(FPS) / 1000
        gf.check_events(settings, screen, stats, sb, play_button, high_scores, scores_button, ship, aliens, bullets, game_over, alien_explosions, boss)
        if stats.game_active:
            if not stats.game_over:
                ship.update(dt)
                gf.update_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt, boss_bullets, boss)
                gf.update_aliens(settings, screen, stats, sb, ship, aliens, bullets, dt, alien_bullets, alien, alien_explosions, boss_bullets, boss)
                bullets.update()
                alien_bullets.update()
                boss_bullets.update()
        gf.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button, game_over, alien_bullets, alien_explosions, dt, boss_bullets, boss)
        


run_game()
