class Settings:
    """Класс для хранения всех настроек игры Alien Invasion"""

    def __init__(self):
        """Инициализирует настройки игры"""
        # Параметры экрана
        self.screen_width = 1200
        self.screen_heigth = 600
        self.bg_color = (56, 27, 91)
        self.ship_speed = 1.5
        self.fullscreen_mode = True
