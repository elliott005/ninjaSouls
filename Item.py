import pygame
from globals import *

class Item(pygame.sprite.Sprite):
    types = {
        "potionHealth": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Potion/LifePot.png"), (size[0] / 2, size[1] / 2)),
        "plantSpell": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Scroll/ScrollPlant.png"), (size[0] / 2, size[1] / 2)),
        "heart": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/HUD/Heart.png").subsurface(pygame.rect.Rect(0, 0, 16, 16)), (size[0] / 2, size[1] / 2))
    }
    def __init__(self, pos, type, dead, groups, alreadyCentered=False):
        super().__init__(groups)
        if not alreadyCentered:
            self.rect = pygame.rect.Rect((pos[0] + size[0] / 2, pos[1] + size[1] / 2), size)
        else:
            self.rect = pygame.rect.Rect((pos[0], pos[1]), size)
        self.type = type
        self.image = self.types[self.type]
        self.trulyDead = dead
        if self.type == "heart":
            self.healAmount = 2