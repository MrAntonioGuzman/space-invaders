import random
import time
import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
from text import Text
from high_scores import HighScores
from alien_bullet import AlienBullet
from explosion import Explosion


def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    
    if event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    
    if event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, game_over, alien_explosions, boss):
    game_over.check_score()
    button_clicked = play_button.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats(game_over.get_high_score())
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, aliens, alien_explosions)
        ship.center_ship()
        boss.dead = False


def check_game_over_buttons(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, game_over, alien_explosions, boss):
    game_over.check_score()
    if stats.game_over:
        play_button_clicked = game_over.get_play_again_btn().collidepoint(mouse_x, mouse_y)
        menu_button_clicked = game_over.get_main_menu_btn().collidepoint(mouse_x, mouse_y)

        if play_button_clicked:
            stats.game_over = False
            settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(False)
            stats.reset_stats(game_over.get_high_score())
            stats.game_active = True
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()
            aliens.empty()
            bullets.empty()
            create_fleet(settings, screen, ship, aliens, alien_explosions)
            ship.center_ship()
            

        if menu_button_clicked:
            stats.game_over = False
            stats.game_active = False

        boss.dead = False


def check_events(settings, screen, stats, sb, play_button, high_scores, scores_button, ship, aliens, bullets, game_over, alien_explosions, boss):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, game_over, alien_explosions, boss)
            high_scores_menu(screen, settings, stats, high_scores, scores_button, mouse_x, mouse_y)
            check_game_over_buttons(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y, game_over, alien_explosions, boss)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)


def update_bullets(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt, boss_bullets, boss):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    for bullet in alien_bullets.copy():
        if bullet.rect.bottom >= settings.get_dims()[1]:
            alien_bullets.remove(bullet)
    
    for bullet in boss_bullets.copy():
        if bullet.rect.bottom >= settings.get_dims()[1]:
            boss_bullets.remove(bullet)

    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets, alien_explosions, dt, boss)
    check_alien_bullet_hit_player(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt, boss_bullets, boss)


def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets, alien_explosions, dt, boss):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    if collisions:
        for aliens in collisions.values():
            for a in aliens:
                stats.score += a.get_points()
                a.alien_hit()
            sb.prep_score()
        check_high_score(stats, sb)

    if pygame.sprite.spritecollideany(boss, bullets):
        stats.score += 100
        boss.died()

    if len(aliens) == 0:
        bullets.empty()
        settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(settings, screen, ship, aliens, alien_explosions)
        boss.dead = False
        stats.fleet_level = 0


def get_number_rows(settings, ship_height, alien_height):
    available_space_y = (settings.get_dims()[1] - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_aliens_x(settings, alien_width):
    available_space_x = settings.get_dims()[0] - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def create_alien(settings, screen, aliens, alien_number, row_number, alien_exp_imgs, alien_explosions):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width    
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.change_image()
    aliens.add(alien)

    alien_exp = Explosion(screen, alien_exp_imgs, alien.get_rect())
    alien_explosions.add(alien_exp)


def create_fleet(settings, screen, ship, aliens, alien_explosions):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width

    alien_exp_imgs = [
        pygame.image.load('images/alien_exp_1.png'),
        pygame.image.load('images/alien_exp_2.png'),
        pygame.image.load('images/alien_exp_3.png'),
        pygame.image.load('images/alien_exp_4.png')
    ]

    number_aliens_x = get_number_aliens_x(settings, alien.rect.width)
    number_rows = get_number_rows(settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(settings, screen, aliens, alien_number, row_number, alien_exp_imgs, alien_explosions)


def check_fleet_edges(settings, stats, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            stats.update_fleet_level()
            break


def check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt):
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt)
            break


def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed

    settings.fleet_direction *= -1
    


def shoot_alien_bullets(settings, screen, aliens, alien_bullets, alien):
    for alien in aliens.sprites():
        if random.randrange(101) == 100:
            if len(alien_bullets) < settings.alien_bullets_allowed:
                bullet = AlienBullet(settings, screen, alien)
                alien_bullets.add(bullet)


def shoot_boss_bullets(settings, screen, aliens, boss_bullets, boss):
    if boss.shoot():
        bullet = AlienBullet(settings, screen, boss)
        boss_bullets.add(bullet)


def update_aliens(settings, screen, stats, sb, ship, aliens, bullets, dt, alien_bullets, alien, alien_explosions, boss_bullets, boss):
    check_fleet_edges(settings, stats, aliens)
    aliens.update(dt)
    shoot_alien_bullets(settings, screen, aliens, alien_bullets, alien)
    shoot_boss_bullets(settings, screen, aliens, boss_bullets, boss)
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt)
    check_aliens_bottom(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt)


def check_alien_bullet_hit_player(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt, boss_bullets, boss):
    collisions = pygame.sprite.spritecollideany(ship, alien_bullets)
    if collisions:
        ship.is_hit()

    collisions = pygame.sprite.spritecollideany(ship, boss_bullets)
    if collisions:
        ship.is_hit()


def ship_hit(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt): 
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        alien_bullets.empty()
        create_fleet(settings, screen, ship, aliens, alien_explosions)
        ship.center_ship()
        
    else:
        stats.game_over = True
        pygame.mouse.set_visible(True)



def game_menu(settings, screen):
    alien_1_1 = pygame.image.load('images/alien_1_1.png')
    alien_1_1 = pygame.transform.scale(alien_1_1, (60, 58))

    alien_2_1 = pygame.image.load('images/alien_2_1.png')
    alien_2_1 = pygame.transform.scale(alien_2_1, (60, 58))

    alien_3_1 = pygame.image.load('images/alien_3_1.png')
    alien_3_1 = pygame.transform.scale(alien_3_1, (60, 58))

    ufo = pygame.image.load('images/ufo.png')
    ufo = pygame.transform.scale(ufo, (60, 58))

    BLACK = (0, 0, 0)
    SPACE = 'SPACE'
    INVADE = 'INVADERS'
    PLAY = 'PLAY'
    SCORES = 'HIGH SCORES'
    ALIEN_1 = ' = 10 PTS'
    ALIEN_2 = ' = 20 PTS'
    ALIEN_3 = ' = 40 PTS'
    UFO = ' = ?? PTS'
    x, y = settings.get_dims()

    enemy_rect = pygame.Rect(0, 0, 300, 50)
    alien_rect = pygame.Rect(0, 0, 100, 50)
    points_rect = pygame.Rect(0, 0, 200, 50)

    space_text = Text(BLACK, 62, SPACE, screen)
    invade_text = Text(BLACK, 82, INVADE, screen)
    play_text = Text(BLACK, 42, PLAY, screen)
    scores_text = Text(BLACK, 42, SCORES, screen)
    alien_1_text = Text(BLACK, 42, ALIEN_1, screen)
    alien_2_text = Text(BLACK, 42, ALIEN_2, screen)
    alien_3_text = Text(BLACK, 42, ALIEN_3, screen)
    ufo_text = Text(BLACK, 42, UFO, screen)

    space_rect = space_text.get_rect()
    space_rect.center = (x // 2, 50)

    invade_rect = invade_text.get_rect()
    invade_rect.center = (x // 2, (space_rect.bottom + space_rect.height // 2) + 10)

    scores_rect = scores_text.get_rect()
    scores_rect.center = (x // 2, y - 50)

    play_rect = play_text.get_rect()
    play_rect.center = (x // 2, (scores_rect.top - scores_rect.height // 2) - 10)

    enemy_rect.center = (x // 2, invade_rect.bottom + invade_rect.height // 2 + 50)

    screen.fill(settings.get_bg_color())
    space_text.blit_me()
    invade_text.blit_me()
    scores_text.blit_me()
    play_text.blit_me()

    enemies = [alien_1_1, alien_2_1, alien_3_1, ufo]
    points = [alien_1_text, alien_2_text, alien_3_text, ufo_text]

    for i in range(4):
        alien_rect.topleft = (enemy_rect.x + 50, enemy_rect.y)

        enemies[i].get_rect().center = alien_rect.center

        points_rect.topleft = alien_rect.topright
        points_rect.x -= 50
        points[i].get_rect().center = points_rect.center
        
        screen.blit(enemies[i], alien_rect)
        points[i].blit_me()

        enemy_rect.y += 100
    
    pygame.display.flip()

    return scores_rect, play_rect


def high_scores_menu(screen, settings, stats, high_scores, scores_button, mouse_x, mouse_y):
    button_clicked = scores_button.collidepoint(mouse_x, mouse_y)
    back_button_clicked = high_scores.get_back_button().collidepoint(mouse_x, mouse_y)
    if button_clicked:
        stats.scores_menu = True
        screen.fill(settings.get_bg_color())
        high_scores.draw_scores()
        pygame.display.flip()
    
    if back_button_clicked:
        stats.scores_menu = False


def game_over_menu(game_over):
    game_over.draw_menu()


def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button, game_over, alien_bullets, alien_explosions, dt, boss_bullets, boss):

    if not stats.game_active:
        #play_button.draw_button()
        if not stats.scores_menu:
            game_menu(settings, screen)

    elif stats.game_over:
        game_over_menu(game_over)
        pygame.display.flip()

    else:
        
        if not ship.hit and not ship.alive:
            ship.reset_hit()
            ship_hit(settings, screen, stats, sb, ship, aliens, bullets, alien_bullets, alien_explosions, dt)

        screen.fill(settings.get_bg_color())    

        for bullet in bullets.sprites():
            bullet.draw_bullet()

        
        for bullet in alien_bullets.sprites():
            bullet.draw_bullet()
        
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()

        if not boss.dead and stats.boss_ready():
            boss.draw()

        if boss.dead:
            if len(boss_bullets) > 0:
                boss.display_score()
            
            else:
                boss.reset_spawn()


        for bullet in boss_bullets.sprites():
                bullet.draw_bullet()
        pygame.display.flip()
