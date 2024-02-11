import pygame, math, random
from globals import *

SQRT2 = math.sqrt(2)

spriteSheetVillager2Idle = pygame.image.load("assets/NinjaAdventure/Actor/Characters/Villager2/SeparateAnim/Idle.png").convert_alpha()
spriteSheetVillager2Walk = pygame.image.load("assets/NinjaAdventure/Actor/Characters/Villager2/SeparateAnim/Walk.png").convert_alpha()
spriteSheetVillager3Idle = pygame.image.load("assets/NinjaAdventure/Actor/Characters/Villager3/SeparateAnim/Idle.png").convert_alpha()
spriteSheetVillager3Walk = pygame.image.load("assets/NinjaAdventure/Actor/Characters/Villager3/SeparateAnim/Walk.png").convert_alpha()
spriteSheetCat = pygame.image.load("assets/NinjaAdventure/Actor/Animals/Cat/SpriteSheet.png").convert_alpha()
spriteSize = mapTileSize.x

class NPC(pygame.sprite.Sprite):
    animationsByName = {
        "Villager2": {
            "idle": {
                "down": [pygame.transform.scale(spriteSheetVillager2Idle.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "up": [pygame.transform.scale(spriteSheetVillager2Idle.subsurface(pygame.Rect(spriteSize * 1, spriteSize * 0, spriteSize, spriteSize)), size)],
                "left": [pygame.transform.scale(spriteSheetVillager2Idle.subsurface(pygame.Rect(spriteSize * 2, spriteSize * 0, spriteSize, spriteSize)), size)],
                "right": [pygame.transform.scale(spriteSheetVillager2Idle.subsurface(pygame.Rect(spriteSize * 3, spriteSize * 0, spriteSize, spriteSize)), size)],
                "max": 1,
                "speed": 0
            },
            "walk": {
                "down": [pygame.transform.scale(spriteSheetVillager2Walk.subsurface(pygame.Rect(spriteSize * 0, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "up": [pygame.transform.scale(spriteSheetVillager2Walk.subsurface(pygame.Rect(spriteSize * 1, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "left": [pygame.transform.scale(spriteSheetVillager2Walk.subsurface(pygame.Rect(spriteSize * 2, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "right": [pygame.transform.scale(spriteSheetVillager2Walk.subsurface(pygame.Rect(spriteSize * 3, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "max": 4,
                "speed": 3
            },
            "face": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Actor/Characters/Villager2/Faceset.png"), (128, 128))
        },
        "Villager3": {
            "idle": {
                "down": [pygame.transform.scale(spriteSheetVillager3Idle.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "up": [pygame.transform.scale(spriteSheetVillager3Idle.subsurface(pygame.Rect(spriteSize * 1, spriteSize * 0, spriteSize, spriteSize)), size)],
                "left": [pygame.transform.scale(spriteSheetVillager3Idle.subsurface(pygame.Rect(spriteSize * 2, spriteSize * 0, spriteSize, spriteSize)), size)],
                "right": [pygame.transform.scale(spriteSheetVillager3Idle.subsurface(pygame.Rect(spriteSize * 3, spriteSize * 0, spriteSize, spriteSize)), size)],
                "max": 1,
                "speed": 0
            },
            "walk": {
                "down": [pygame.transform.scale(spriteSheetVillager3Walk.subsurface(pygame.Rect(spriteSize * 0, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "up": [pygame.transform.scale(spriteSheetVillager3Walk.subsurface(pygame.Rect(spriteSize * 1, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "left": [pygame.transform.scale(spriteSheetVillager3Walk.subsurface(pygame.Rect(spriteSize * 2, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "right": [pygame.transform.scale(spriteSheetVillager3Walk.subsurface(pygame.Rect(spriteSize * 3, spriteSize * y, spriteSize, spriteSize)), size) for y in range(0, 4)],
                "max": 4,
                "speed": 3
            },
            "face": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Actor/Characters/Villager3/Faceset.png"), (128, 128))
        },
        "Cat": {
            "idle": {
                "down": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "up": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "left": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "right": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "max": 1,
                "speed": 0
            },
            "walk": {
                "down": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * x, spriteSize * 0, spriteSize, spriteSize)), size) for x in range(0, 2)],
                "up": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * x, spriteSize * 0, spriteSize, spriteSize)), size) for x in range(0, 2)],
                "left": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * x, spriteSize * 0, spriteSize, spriteSize)), size) for x in range(0, 2)],
                "right": [pygame.transform.scale(spriteSheetCat.subsurface(pygame.Rect(spriteSize * x, spriteSize * 0, spriteSize, spriteSize)), size) for x in range(0, 2)],
                "max": 2,
                "speed": 2
            },
            "face": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Actor/Animals/Cat/Faceset.png"), (128, 128))
        }
    }

    def __init__(self, pos, size, name, groups) -> None:
        super().__init__(groups)
        self.rect = pygame.Rect(pos, size)
        self.name = name
        self.animations = self.animationsByName[self.name]
        self.animation = "idle"
        self.currentFrame = 0.0
        self.direction = "down"

        self.velocity = pygame.math.Vector2(0, 0)
        self.maxSpeed = 100
        self.acceleration = 200
        self.friction = 1000

        self.image = self.animations[self.animation][self.direction][math.floor(self.currentFrame)]

        if self.name == "Villager2":
            self.dialogue = [
                "bla, bla, bla",
                "..."
            ]
        elif self.name == "Villager3":
            self.dialogue = [
                "Hello  adventurer!",
                "It's   dangerous   to  go  alone!",
                "..."
            ]
        elif self.name == "Cat":
            self.dialogue = [
                "meow",
                "meow   meow    meow!",
                "*purr*"
            ]
        else:
            self.dialogue = ["..."]
        
        self.numTalk = 0
        
        self.startPos = pygame.math.Vector2(self.rect.topleft)
        self.targetDistance = 400
        self.target = pygame.math.Vector2(self.startPos.x + random.randint(-self.targetDistance, self.targetDistance), self.startPos.y + random.randint(-self.targetDistance, self.targetDistance))

        self.timers = {
            "walkMax": Timer(3, True),
            "rest": Timer(random.randint(10, 50) / 10)
        }
    
    def update(self, dt, walls, talking):
        if not talking:
            if (pygame.math.Vector2(self.rect.topleft).distance_to(self.target) < self.maxSpeed * dt or not self.timers["walkMax"].active) and not self.timers["rest"].active:
                self.target = pygame.math.Vector2(self.startPos.x + random.randint(-self.targetDistance, self.targetDistance), self.startPos.y + random.randint(-self.targetDistance, self.targetDistance))
                self.timers["rest"].start(random.randint(10, 50) / 10)

            if not self.timers["rest"].active:
                input = pygame.math.Vector2(1, 0).rotate(pygame.math.Vector2(1, 0).angle_to(self.target - pygame.math.Vector2(self.rect.topleft)))
            else:
                input = pygame.math.Vector2(0, 0)
        else:
            input = pygame.math.Vector2(0, 0)

        self.handleAcceleration(dt, input)

        self.move(dt, walls)

        self.updateAnimations(dt, input)

        self.image = self.animations[self.animation][self.direction][math.floor(self.currentFrame)]

        wasActive = self.timers["walkMax"].active
        for timer in self.timers:
            self.timers[timer].update(dt)
        
        if not self.timers["rest"].active and not self.timers["walkMax"].active and not wasActive:
            self.timers["walkMax"].start()
    
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
            if input.y < -0.5:
                self.direction = "up"
            elif input.y > 0.5:
                self.direction = "down"
        else:
            self.changeAnimation("idle")
        self.currentFrame += dt * self.animations[self.animation]["speed"]
        if self.currentFrame >= self.animations[self.animation]["max"]:
            self.currentFrame = 0.0
    
    def changeAnimation(self, anim):
        if anim != self.animation:
            self.animation = anim
            self.currentFrame = 0.0
