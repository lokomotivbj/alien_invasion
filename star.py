import pygame
from pygame.sprite import Sprite
from itertools import chain, cycle
from random import randrange

class Star(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/star.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.start_alpha = randrange(1,100)
        self.alpha = cycle(chain(range(self.start_alpha, 101), range(101, 0, -1), range(0, self.start_alpha)))
    def update(self):
            self.image.set_alpha(next(self.alpha))