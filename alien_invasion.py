import sys
from random import randrange
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sounds import Sound


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()

        if self.settings.fullscreen_mode:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height)
            )

        pygame.display.set_caption('Alien Invasion')
        self.clock = pygame.time.Clock()
        # Создание экземпляра для хранения игровой статистики.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()

        self._create_stars()
        self._create_fleet()

        # Создание кнопки Play
        self.play_button = Button(self, 'Play')
        self.easy_button = Button(self, 'Цыпленок')
        self.normal_button = Button(self, 'Петух')
        self.hard_button = Button(self, 'Петушара!!!')
        self.easy_button.rect.centerx = self.screen.get_rect().centerx - 300
        self.easy_button.msg_image_rect.centerx = self.easy_button.rect.centerx
        self.normal_button.rect.centerx = self.screen.get_rect().centerx
        self.normal_button.msg_image_rect.centerx = self.normal_button.rect.centerx
        self.hard_button.rect.centerx = self.screen.get_rect().centerx + 300
        self.hard_button.msg_image_rect.centerx = self.hard_button.rect.centerx
        self.easy_button.rect.centery = 200
        self.normal_button.rect.centery = 200
        self.hard_button.rect.centery = 200
        self.easy_button.msg_image_rect.centery = 200
        self.normal_button.msg_image_rect.centery = 200
        self.hard_button.msg_image_rect.centery = 200


        self.start_screen_music = True
        self.start_music_active = False
        self.game_screen_music = False
        self.game_music_active = False

        self.sound = Sound()

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            if self.start_screen_music and not self.start_music_active:
                pygame.mixer.music.load('start_screen.wav')
                pygame.mixer.music.play(loops=-1, fade_ms=1000)
                self.start_music_active = True

            if self.game_screen_music and not self.game_music_active:
                pygame.mixer.music.load('game_screen.flac')
                pygame.mixer.music.play(loops=-1, fade_ms=1000)
                self.game_music_active = True

            self._check_events()
            if self.stats.game_active and self.settings.difficulty_level:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

            self.clock.tick(self.settings.fps)

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                self._check_easy_button(mouse_pos)
                self._check_normal_button(mouse_pos)
                self._check_hard_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатия клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            self.sound.laser()
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды"""
        #  Обновление позиций снарядов
        self.bullets.update()

        # Удаление снарядов вылетевших за верхний край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom < 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами"""
        # Удаление снарядов и пришельцев, участвующих в коллизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, \
                                                self.settings.weak_bullet, True)
        if collisions:
            self.sound.explosion()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            #  Уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Увеличение уровня
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте"""
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем"""
        if self.stats.ships_left > 0:
            # Уменьшение ships_left
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Пауза
            sleep(1)

        else:
            self.stats.game_active = False
            self.settings.difficulty_level = None
            pygame.mouse.set_visible(True)
            self.game_screen_music = False
            self.start_screen_music = True
            self.start_music_active = False
            self.game_music_active = False


    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же что и при столкновении с кораблем.
                self._ship_hit()
                break

    def _create_alien(self, alien_number, row_number):

        # Создание пришельца и размещение его в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + alien_width * 2 * alien_number
        alien.y = alien_height + alien_height * 2 * row_number
        alien.rect.x = alien.x
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на приближение пришельца к краю экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет его направление"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_fleet(self):
        """Создание флота вторжения"""

        # Расчет количества пришельцев в ряду
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_width * 2)
        available_space_y = self.settings.screen_height - (alien_height * 3) - self.ship.rect.height
        number_rows = available_space_y // (alien_height * 2)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Создание флота пришельцев
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

        self.aliens.add(alien)

    def _create_stars(self):
        avrg_dist = 50
        number_rows = (self.settings.screen_height - avrg_dist * 2) // avrg_dist
        number_in_row = (self.settings.screen_width - avrg_dist * 2) // avrg_dist

        for row_number in range(number_rows):
            for num_in_cur_row in range(number_in_row):
                star = Star()
                star.rect.x = randrange(0, avrg_dist) + num_in_cur_row * (avrg_dist + star.rect.width)
                star.rect.y = randrange(0, avrg_dist) + row_number * (avrg_dist + star.rect.height)
                self.stars.add(star)

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.stars.update()
        self.stars.draw(self.screen)
        self.ship.blitme()
        if self.stats.game_active and self.settings.difficulty_level:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)
            self.sb.show_score()
        # Кнопка Play отображается в том случае, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()
        # Кнопки сложности отображаются если сложность не выбрана
        if not self.settings.difficulty_level and self.stats.game_active:
            self.difficulty_level_choice()

        pygame.display.flip()

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.start_new_game()

    def start_new_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_ships()

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()



    def difficulty_level_choice(self):
        """Отображение кнопок выбора сложности и изменение стартовых настроек"""

        # Создать три кнопки для выбора уровней сложности

        self.easy_button.draw_button()
        self.normal_button.draw_button()
        self.hard_button.draw_button()




    def _check_easy_button(self, mouse_pos):
        if self.stats.game_active:
            if self.easy_button.rect.collidepoint(mouse_pos):
                self.settings.difficulty_level = 0.7
                self.settings.alien_speed_factor *= self.settings.difficulty_level
                pygame.mouse.set_visible(False)
                self.game_screen_music = True
                self.start_screen_music = False
                self.start_music_active = False


    def _check_normal_button(self, mouse_pos):
        if self.stats.game_active:
            if self.normal_button.rect.collidepoint(mouse_pos):
                self.settings.difficulty_level = 1.0
                self.settings.alien_speed_factor *= self.settings.difficulty_level
                pygame.mouse.set_visible(False)
                self.game_screen_music = True
                self.start_screen_music = False
                self.start_music_active = False


    def _check_hard_button(self, mouse_pos):
        if self.stats.game_active:
            if self.hard_button.rect.collidepoint(mouse_pos):
                self.settings.difficulty_level = 1.7
                self.settings.alien_speed_factor *= self.settings.difficulty_level
                pygame.mouse.set_visible(False)
                self.game_screen_music = True
                self.start_screen_music = False
                self.start_music_active = False


if __name__ == '__main__':
    # создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
