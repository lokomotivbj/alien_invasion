import pygame
from random import randint

class Sound:
    def __init__(self):
        self.expl_num = 3
        self.laser_num = 6
        self.explosions = [pygame.mixer.Sound(f'explosion{num}.wav') for num in range(1, self.expl_num+1)]
        self.lasers = [pygame.mixer.Sound(f'laser{num}.wav') for num in range(1, self.laser_num+1)]

    def laser(self):
        self.lasers[randint(0, self.laser_num-1)].play()

    def explosion(self):
        self.explosions[randint(0, self.expl_num-1)].play()
