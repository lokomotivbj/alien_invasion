import sys
import pygame


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()

        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption('Alien Invasion')

        # назначение цвета фона
        self.bg_color = (56,27,91)

    def run_game(self):
        """Запуск основного цикла игры."""
        while True:
            # Отслеживание событий клавиатуры и мыши.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # при каждом проходе цикла перерисовывается экран
            self.screen.fill(self.bg_color)

            # отображение последнего прорисованного экрана.
            pygame.display.flip()


if __name__ == '__main__':
    # создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
