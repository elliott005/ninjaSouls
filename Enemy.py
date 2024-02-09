from typing import Any
import pygame, math
from globals import *

SQRT2 = math.sqrt(2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, size, type, gid, groups):
        super().__init__(groups)
        self.gid = gid
        self.rect = pygame.Rect(pos, size)
        spriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Monsters/Beast/Beast.png").convert_alpha()
        spriteSheetDeath = pygame.image.load("assets/NinjaAdventure/FX/Magic/Circle/SpriteSheetSpark.png").convert_alpha()
        spriteSize = mapTileSize.x
        deathSize = 32
        self.animations = {
            "idle": {
                "down": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "up": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 1, spriteSize * 0, spriteSize, spriteSize)), size)],
                "left": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 2, spriteSize * 0, spriteSize, spriteSize)), size)],
                "right": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 3, spriteSize * 0, spriteSize, spriteSize)), size)],
                "max": 1,
                "speed": 0
            },
            "walk": {
                "down": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 0, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "up": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 1, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "left": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 2, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "right": [pygame.transform.scale(spriteSheet.subsurface(pygame.Rect(spriteSize * 3, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "max": 4,
                "speed": 6
            },
            "dead": {
                "all": [pygame.transform.scale(spriteSheetDeath.subsurface(pygame.Rect(deathSize * x, deathSize * 0, deathSize, deathSize)), size) for x in range(0, 4)],
                "max": 4,
                "speed": 6
            }
        }


        self.animation = "idle"
        self.currentFrame = 0.0
        self.direction = "down"

        self.image = self.animations[self.animation][self.direction][math.floor(self.currentFrame)]

        self.activeDistance = 300.0

        self.velocity = pygame.math.Vector2(0, 0)
        self.maxSpeed = 200
        self.acceleration = 400
        self.friction = 800

        self.health = 2
        self.dead = False

        self.timers = {
            "death": Timer(self.animations["dead"]["max"] / self.animations["dead"]["speed"]),
            "grace": Timer(0.5)
        }

        self.startTimerOnce = False

        self.knockBack = self.maxSpeed * 2.5
    
    def update(self, dt, playerPos, walls, playerAttackHitbox = -1, *args: Any, **kwargs: Any) -> None:
        super().update(*args, **kwargs)
        input = pygame.math.Vector2(0, 0)
        if not self.dead:
            posVector = pygame.math.Vector2(self.rect.topleft[0], self.rect.topleft[1])
            if playerPos.distance_to(posVector) < self.activeDistance:
                input = pygame.math.Vector2(1, 0).rotate(pygame.math.Vector2(1, 0).angle_to(playerPos - posVector))

            self.handleAcceleration(dt, input)

            self.move(dt, walls)

        self.updateAnimations(dt, input)

        self.image = self.animations[self.animation][self.direction][math.floor(self.currentFrame)]

        self.handleHit(playerAttackHitbox, playerPos)

        for timer in self.timers:
            self.timers[timer].update(dt)

        if self.health < 1:
            self.dead = True
            if not self.startTimerOnce:
                self.timers["death"].start()
            self.startTimerOnce = True
            if not self.timers["death"].active:
                self.kill()
            
    
    def handleAcceleration(self, dt, input):
        if input.y:
            if self.velocity.y != 0 and sign(self.velocity.y) != sign(input.y):
                self.velocity.y = clamp(self.velocity.y + self.friction * dt * input.y, 0, self.velocity.y)
            else:
                self.velocity.y = pygame.math.clamp(self.velocity.y + self.acceleration * dt * input.y, -self.maxSpeed, self.maxSpeed)
        else:
            self.velocity.move_towards_ip(pygame.math.Vector2(self.velocity.x, 0), self.friction * dt)
        
        if input.x:
            if self.velocity.x != 0 and sign(self.velocity.x) != sign(input.x):
                self.velocity.x = clamp(self.velocity.x + self.friction * dt * input.x, 0, self.velocity.x)
            else:
                self.velocity.x = pygame.math.clamp(self.velocity.x + self.acceleration * dt * input.x, -self.maxSpeed, self.maxSpeed)
        else:
            self.velocity.move_towards_ip(pygame.math.Vector2(0, self.velocity.y), self.friction * dt)
        
        if input.x != 0 and input.y != 0 and self.velocity.length():
            self.velocity.scale_to_length(self.velocity.length() - self.acceleration * dt / SQRT2)
    
    def move(self, dt, walls):
        if self.velocity.length() != 0:
            if not self.timers["grace"].active:
                moveBy = self.velocity.normalize() * min(self.velocity.length(), self.maxSpeed) * dt
            else:
                moveBy = self.velocity * dt
            movedRect = self.rect.move(moveBy.x, 0)
            if movedRect.collidelist(walls) == -1:
                self.rect = movedRect
            movedRect = self.rect.move(0, moveBy.y)
            if movedRect.collidelist(walls) == -1:
                self.rect = movedRect

    def updateAnimations(self, dt, input):
        if not self.dead:
            if input.x or input.y:
                self.changeAnimation("walk")
                if input.x < 0.0:
                    self.direction = "left"
                elif input.x > 0.0:
                    self.direction = "right"
                if input.y < -0.5:
                    self.direction = "up"
                elif input.y > 0.5:
                    self.direction = "down"
            else:
                self.changeAnimation("idle")
        else:
            self.changeAnimation("dead")
            self.direction = "all"
        self.currentFrame += dt * self.animations[self.animation]["speed"]
        if self.currentFrame >= self.animations[self.animation]["max"]:
            self.currentFrame = 0.0
    
    def changeAnimation(self, anim):
        if anim != self.animation:
            self.animation = anim
            self.currentFrame = 0.0
    
    def handleHit(self, playerAttackHitbox, playerPos):
        if playerAttackHitbox == -1 or self.timers["grace"].active: return
        if self.rect.colliderect(playerAttackHitbox):
            self.health -= 1
            self.timers["grace"].start()
            self.velocity.rotate_ip(self.velocity.angle_to(pygame.math.Vector2(self.rect.x, self.rect.y) - playerPos))
            self.velocity = self.velocity.normalize() * self.knockBack