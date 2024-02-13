import pygame, math
from globals import *

leafSpriteSheet = pygame.image.load("assets/NinjaAdventure/FX/Particle/Grass.png")
leafSpriteSize = (12, 13)
leafSprites = [pygame.transform.scale(leafSpriteSheet.subsurface(pygame.Rect(leafSpriteSize[0] * x, leafSpriteSize[1] * 0, leafSpriteSize[0], leafSpriteSize[1])), (size[0], size[1])) for x in range(0, 6)]

class CuttableGrass(pygame.sprite.Sprite):
    def __init__(self, pos, size, surf, groups):
        super().__init__(groups)
        self.rect = pygame.rect.Rect(pos, size)
        self.image = pygame.transform.scale(surf, size)
        self.cut = False
        self.currentFrame = 0
        self.maxFrame = 6
        self.animSpeed = 10
        self.angle = 0
        self.turnSpeed = 450
        self.velocity = pygame.math.Vector2(0, -100)
    
    def update(self, dt, playerAttackHitbox=-1):
        if playerAttackHitbox != -1 and not self.cut:
            if self.rect.colliderect(playerAttackHitbox):
                self.cut = True
        if self.cut:
            if self.velocity.x >= 0.0:
                self.angle += dt * self.turnSpeed
                self.velocity.rotate_ip(self.angle * dt)
            self.rect.move_ip(self.velocity * dt)
            self.currentFrame += dt * self.animSpeed
            if self.currentFrame >= self.maxFrame:
                self.currentFrame = 0.0
                self.kill()
            self.image = leafSprites[math.floor(self.currentFrame)]
        
