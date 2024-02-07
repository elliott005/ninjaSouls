import pygame, math
from inputs import *

SQRT2 = math.sqrt(2)

class Player():
    def __init__(self, pos, size) -> None:
        self.rect = pygame.Rect(pos, size)
        self.velocity = pygame.math.Vector2(0, 0)
        self.maxSpeed = 250
        self.acceleration = 750
        self.friction = 1250

        self.zoomMin = 0.5
        self.zoomSpeed = 0.25
        self.zoom = 1

        spriteSize = 16
        idleSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/BlueNinja/SeparateAnim/Idle.png")
        walkSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/BlueNinja/SeparateAnim/Walk.png")
        self.animations = {
            "idle": {
                "down": [pygame.transform.scale(idleSpriteSheet.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "up": [pygame.transform.scale(idleSpriteSheet.subsurface(pygame.Rect(spriteSize * 1, spriteSize * 0, spriteSize, spriteSize)), size)],
                "left": [pygame.transform.scale(idleSpriteSheet.subsurface(pygame.Rect(spriteSize * 2, spriteSize * 0, spriteSize, spriteSize)), size)],
                "right": [pygame.transform.scale(idleSpriteSheet.subsurface(pygame.Rect(spriteSize * 3, spriteSize * 0, spriteSize, spriteSize)), size)],
                "max": 1,
                "speed": 0
            },
            "walk": {
                "down": [pygame.transform.scale(walkSpriteSheet.subsurface(pygame.Rect(spriteSize * 0, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "up": [pygame.transform.scale(walkSpriteSheet.subsurface(pygame.Rect(spriteSize * 1, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "left": [pygame.transform.scale(walkSpriteSheet.subsurface(pygame.Rect(spriteSize * 2, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "right": [pygame.transform.scale(walkSpriteSheet.subsurface(pygame.Rect(spriteSize * 3, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "max": 4,
                "speed": 6
            },
        }
        self.animation = "idle"
        self.currentFrame = 0.0
        self.direction = "down"

        self.timers = {
            "zoomOut": Timer(1.0, True)
        }
    
    def update(self, dt, walls):
        keysPressed = pygame.key.get_pressed()
        input = pygame.math.Vector2(checkInput(keysPressed, "moveRight") - checkInput(keysPressed, "moveLeft"), checkInput(keysPressed, "moveDown") - checkInput(keysPressed, "moveUp"))
        self.handleAcceleration(dt, input)
        self.move(dt, walls)
        self.updateAnimations(dt, input)

        self.updateZoom(dt)
        self.updateTimers(dt)
    
    def draw(self, WINDOW):
        windowSize = pygame.display.get_window_size()
        if self.zoom == 1:
            WINDOW.blit(self.animations[self.animation][self.direction][math.floor(self.currentFrame)], (windowSize[0] / 2 - self.rect.width / 2, windowSize[1] / 2 - self.rect.height / 2))
        else:
            WINDOW.blit(pygame.transform.scale(self.animations[self.animation][self.direction][math.floor(self.currentFrame)], (self.rect.width * self.zoom, self.rect.height * self.zoom)), (windowSize[0] / 2 - self.rect.width / 2 + (self.rect.width - self.rect.width * self.zoom) / 2, windowSize[1] / 2 - self.rect.height / 2 + (self.rect.height - self.rect.height * self.zoom) / 2))
    
    def handleAcceleration(self, dt, input):
        if input.y:
            if self.velocity.y != 0 and sign(self.velocity.y) != input.y:
                self.velocity.y = clamp(self.velocity.y + self.friction * dt * input.y, 0, self.velocity.y)
            else:
                self.velocity.y = pygame.math.clamp(self.velocity.y + self.acceleration * dt * input.y, -self.maxSpeed, self.maxSpeed)
        else:
            self.velocity.move_towards_ip(pygame.math.Vector2(self.velocity.x, 0), self.friction * dt)
        
        if input.x:
            if self.velocity.x != 0 and sign(self.velocity.x) != input.x:
                self.velocity.x = clamp(self.velocity.x + self.friction * dt * input.x, 0, self.velocity.x)
            else:
                self.velocity.x = pygame.math.clamp(self.velocity.x + self.acceleration * dt * input.x, -self.maxSpeed, self.maxSpeed)
        else:
            self.velocity.move_towards_ip(pygame.math.Vector2(0, self.velocity.y), self.friction * dt)
        
        if input.x != 0 and input.y != 0 and self.velocity.length():
            self.velocity.scale_to_length(self.velocity.length() - self.acceleration * dt / SQRT2)
    
    def move(self, dt, walls):
        if self.velocity.length() != 0:
            moveBy = self.velocity.normalize() * min(self.velocity.length(), self.maxSpeed) * dt
            movedRect = self.rect.move(moveBy.x, 0)
            if movedRect.collidelist(walls) == -1:
                self.rect = movedRect
            movedRect = self.rect.move(0, moveBy.y)
            if movedRect.collidelist(walls) == -1:
                self.rect = movedRect
    
    def updateAnimations(self, dt, input):
        if input.x or input.y:
            self.changeAnimation("walk")
            if input.x < 0.0:
                self.direction = "left"
            elif input.x > 0.0:
                self.direction = "right"
            if input.y < 0.0:
                self.direction = "up"
            elif input.y > 0.0:
                self.direction = "down"
        else:
            self.changeAnimation("idle")
        self.currentFrame += dt * self.animations[self.animation]["speed"]
        if self.currentFrame >= self.animations[self.animation]["max"]:
            self.currentFrame = 0.0
    
    def updateZoom(self, dt):
        if not self.velocity.length():
            if not self.timers["zoomOut"].active:
                self.zoom = max(self.zoom - dt * self.zoomSpeed, self.zoomMin)
            else:
                self.zoom = min(self.zoom + dt * self.zoomSpeed, 1)
        else:
            self.timers["zoomOut"].start()
            self.zoom = min(self.zoom + dt * self.zoomSpeed, 1)
    
    def updateTimers(self, dt):
        for timer in self.timers:
            self.timers[timer].update(dt)
    
    def changeAnimation(self, anim):
        if anim != self.animation:
            self.animation = anim
            self.currentFrame = 0.0


class Timer:
    def __init__(self, waitTime, active: bool = False, looping: bool = False):
        self.waitTime = waitTime
        self.looping = looping
        self.active = active
        self.time = waitTime
    
    def update(self, dt):
        if self.active:
            self.time -= dt
            if self.time <= 0.0:
                if not self.looping:
                    self.active = False
                self.time = self.waitTime
    
    def start(self, time = -1):
        if time == -1:
            time = self.waitTime
        self.active = True
        self.time = self.waitTime
    def pause(self):
        self.active = False
    def stop(self):
        self.active == False
        self.time = self.waitTime


def clamp(n, p_min, p_max):
    if p_max > p_min:
        return min(max(n, p_min), p_max)
    else:
        return min(max(n, p_max), p_min)

def sign(n):
    if n < 0.0:
        return -1
    elif n > 0.0:
        return 1
    return 0