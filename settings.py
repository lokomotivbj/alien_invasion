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

        self.bullet_speed = 10
        self.bullets_allowed = 30
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (224, 56, 31)

        self.alien_speed = 10.0
        self.fleet_drop_speed = 10
        # fleet_direction = 1 обозначает движение вправо, а -1 влево
        self.fleet_direction = 1
