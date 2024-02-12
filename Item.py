import pygame
from globals import *

class Item(pygame.sprite.Sprite):
    types = {
        "potionHealth": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Potion/LifePot.png"), (size[0] / 2, size[1] / 2))
    }
    def __init__(self, pos, type, dead, groups):
        super().__init__(groups)
        self.rect = pygame.rect.Rect((pos[0] + size[0] / 2, pos[1] + size[1] / 2), size)
        self.type = type
        self.image = self.types[self.type]
        self.trulyDead = dead