class Settings:
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_height = 600

        self.bg_color = (56, 27, 91)

        self.fps = 120
        self.fullscreen_mode = True
        # Настройки игры
        self.ship_speed = 6
        self.ship_limit = 3

        self.bullet_speed = 4
        self.bullets_allowed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (224, 56, 31)
        self.weak_bullet = True

        self.alien_speed = 1.0
        self.fleet_drop_speed = 10


        # Темп ускорения игры
        self.speedup_scale = 1.2
        self.difficulty_level = None

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в процессе игры"""
        self.ship_speed_factor = 2.0
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0

        # fleet_direction = 1 обозначает движение вправо, а -1 влево
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
