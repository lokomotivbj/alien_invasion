import os

class GameStats:
    """Отслеживание статистики для игры Alien Invasion"""

    def __init__(self, ai_game):
        """Инициализирует статистику"""
        self.ships_left = None
        self.score = 0
        self.hscore_fname = 'high_score.txt'
        self.high_score = self.load_high_score()
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1


    def load_high_score(self):
        if os.path.exists(self.hscore_fname):
            with open(self.hscore_fname) as hs:
                score = int(hs.read())
            return score
        return 0

    def save_high_score(self):
        cur_hscore = self.load_high_score()
        if self.high_score > cur_hscore:
            with open(self.hscore_fname, 'w') as hs:
                hs.write(str(self.high_score))
