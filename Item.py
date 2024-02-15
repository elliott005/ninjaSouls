import pygame
from globals import *

class Item(pygame.sprite.Sprite):
    types = {
        "potionHealth": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Potion/LifePot.png"), (size[0] / 2, size[1] / 2)),
        "plantSpell": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Scroll/ScrollPlant.png"), (size[0] / 2, size[1] / 2)),
        "heart": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/HUD/Heart.png").subsurface(pygame.rect.Rect(0, 0, 16, 16)), (size[0] / 2, size[1] / 2)),
        "pickaxe": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Weapons/Pickaxe/Sprite.png"), (size[0] / 2, size[1] / 2)),
        "axe": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Weapons/Axe/Sprite.png"), (size[0] / 2, size[1] / 2)),
        "coin": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Treasure/GoldCoin.png"), (size[0] / 2, size[1] / 2)),
    }
    def __init__(self, pos, type, dead, groups, alreadyCentered=False, price=-1, amount=1, category=-1, initialVelocity=-1, rotation=-1):
        super().__init__(groups)
        if not alreadyCentered:
            self.rect = pygame.rect.Rect((pos[0] + size[0] / 2, pos[1] + size[1] / 2), size)
        else:
            self.rect = pygame.rect.Rect((pos[0], pos[1]), size)
        self.type = type
        if category == -1:
            if "weapon" in self.type:
                self.category = "weapon"
                self.type = self.type.split("-")[0]
            else:
                self.category = "item"
        else:
            self.category = category
        self.image = self.types[self.type]
        self.trulyDead = dead
        if self.type == "heart":
            self.healAmount = 2
        self.price = price
        self.amount = amount
        self.velocity = initialVelocity
        self.turnSpeed = 360
        self.pickupable = initialVelocity == -1
        self.rotation = rotation
    
    def update(self, dt):
        if self.velocity != -1 and not self.pickupable:
            self.velocity.rotate_ip(self.turnSpeed * dt * self.rotation)
            self.rect.move_ip(self.velocity * dt)
            if (self.velocity.angle_to(pygame.math.Vector2(0, -1)) < -180.0 and self.rotation > 0.0) or (abs(self.velocity.angle_to(pygame.math.Vector2(0, -1))) > 180.0 and self.rotation < 0.0):
                self.pickupable = True