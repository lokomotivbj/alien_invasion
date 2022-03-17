class Settings:
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_heigth = 600
        self.fps = 120
        self.bg_color = (56, 27, 91)
        self.ship_speed = 6
        self.fullscreen_mode = False
        self.bullet_speed = 4
        self.bullets_allowed = 3
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (224,56,31)
