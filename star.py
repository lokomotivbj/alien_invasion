import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('images/star.png')
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()