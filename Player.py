import pygame, math
from inputs import *
from globals import *


SQRT2 = math.sqrt(2)

class Player():
    def __init__(self, pos, size) -> None:
        self.rect = pygame.Rect(pos, size)
        self.velocity = pygame.math.Vector2(0, 0)
        self.maxSpeed = 250
        self.acceleration = 750
        self.friction = 1250

        self.zoomMin = 0.6
        self.zoomSpeed = 0.25
        self.zoom = 1

        spriteSize = mapTileSize.x
        idleSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/BlueNinja/SeparateAnim/Idle.png").convert_alpha()
        walkSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/BlueNinja/SeparateAnim/Walk.png").convert_alpha()
        attackSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/BlueNinja/SeparateAnim/Attack.png").convert_alpha()
        spriteSheetDeath = pygame.image.load("assets/NinjaAdventure/FX/Magic/Circle/SpriteSheetOrange.png").convert_alpha()
        deathSize = 32
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
            "attack": {
                "down": [pygame.transform.scale(attackSpriteSheet.subsurface(pygame.Rect(spriteSize * 0, spriteSize * 0, spriteSize, spriteSize)), size)],
                "up": [pygame.transform.scale(attackSpriteSheet.subsurface(pygame.Rect(spriteSize * 1, spriteSize * 0, spriteSize, spriteSize)), size)],
                "left": [pygame.transform.scale(attackSpriteSheet.subsurface(pygame.Rect(spriteSize * 2, spriteSize * 0, spriteSize, spriteSize)), size)],
                "right": [pygame.transform.scale(attackSpriteSheet.subsurface(pygame.Rect(spriteSize * 3, spriteSize * 0, spriteSize, spriteSize)), size)],
                "max": 1,
                "speed": 0
            },
            "dead": {
                "all": [pygame.transform.scale(spriteSheetDeath.subsurface(pygame.Rect(deathSize * x, deathSize * 0, deathSize, deathSize)), size) for x in range(0, 4)],
                "max": 4,
                "speed": 2
            }
        }

        self.animation = "idle"
        self.currentFrame = 0.0
        self.direction = "down"
        # self.directionVector = pygame.math.Vector2(0, 1)

        heartSpriteSheet = pygame.image.load("assets/NinjaAdventure/HUD/Heart.png").convert_alpha()
        heartSpriteSize = 16
        self.heartSize = (128, 128)
        self.heartSprites = [pygame.transform.scale(heartSpriteSheet.subsurface(pygame.Rect(heartSpriteSize * x, heartSpriteSize * 0, heartSpriteSize, heartSpriteSize)), self.heartSize) for x in range(0, 5)]


        self.timers = {
            "zoomOut": Timer(1.0, True),
            "attack": Timer(0.5),
            "grace": Timer(0.1),
            "attackCooldown": Timer(1),
            "death": Timer(self.animations["dead"]["max"] / self.animations["dead"]["speed"]),
        }

        self.weapon = "Katana"
        self.attacking = False
        self.weaponOffseX = 5

        self.weapons = {
            "Katana": {"sprite": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Weapons/Katana/SpriteInHand.png"), (math.floor(size[0] / 2), math.floor(size[1] / 2))), "damage": 2}
        }

        for weapon in self.weapons:
            self.weapons[weapon]["spriteDirs"] = {
                "down": self.weapons[weapon]["sprite"],
                "up": pygame.transform.rotate(self.weapons[weapon]["sprite"], 180),
                "left": pygame.transform.rotate(self.weapons[weapon]["sprite"], -90),
                "right": pygame.transform.rotate(self.weapons[weapon]["sprite"], 90)
            }
        
        self.weaponHitboxes = {
            "vertical": pygame.Rect(0, 0, size[0], size[1]),
            "horizontal": pygame.Rect(0, 0, size[0], size[1]),
        }
        self.activeWeaponHitbox = "vertical"

        self.knockback = self.maxSpeed * 3

        self.maxHealth = 12
        self.health = self.maxHealth

        self.dead = False
        self.startDeathTimerOnce = False

        self.sounds = {
            "attack": pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/Sword2.wav"),
            "gameOver": pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/GameOver.wav"),
            "hit": pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/Explosion.wav"),
        }
        self.sounds["attack"].set_volume(0.3)
        self.sounds["hit"].set_volume(0.3)
    
    def update(self, dt, walls, enemiesGroup):
        keysPressed = pygame.key.get_pressed()
        input = pygame.math.Vector2(checkInput(keysPressed, "moveRight") - checkInput(keysPressed, "moveLeft"), checkInput(keysPressed, "moveDown") - checkInput(keysPressed, "moveUp"))
        
        attackInput = checkInput(keysPressed, "attack")
        if not self.dead:
            self.handleAcceleration(dt, input)
            self.move(dt, walls)
            self.handleAttack(attackInput)
        self.updateAnimations(dt, input)

        self.handleDamage(enemiesGroup)

        self.updateZoom(dt)
        self.updateTimers(dt)

        if self.health < 1:
            self.dead = True
            if not self.startDeathTimerOnce:
                self.sounds["gameOver"].play()
                self.timers["death"].start()
            self.startDeathTimerOnce = True
            if not self.timers["death"].active:
                return True
        return False

        # if self.direction == "left":
        #     self.directionVector.x = -1
        #     self.directionVector.y = 0
        # elif self.direction == "right":
        #     self.directionVector.x = 1
        #     self.directionVector.y = 0
        # elif self.direction == "up":
        #     self.directionVector.x = 0
        #     self.directionVector.y = -1
        # elif self.direction == "down":
        #     self.directionVector.x = 0
        #     self.directionVector.y = 1
    
    def draw(self, WINDOW):
        windowSize = pygame.display.get_window_size()
        if self.zoom == 1:
            WINDOW.blit(self.animations[self.animation][self.direction][math.floor(self.currentFrame)], (windowSize[0] / 2 - self.rect.width / 2, windowSize[1] / 2 - self.rect.height / 2))
        else:
            WINDOW.blit(pygame.transform.scale(self.animations[self.animation][self.direction][math.floor(self.currentFrame)], (self.rect.width * self.zoom, self.rect.height * self.zoom)), (windowSize[0] / 2 - self.rect.width / 2 + (self.rect.width - self.rect.width * self.zoom) / 2, windowSize[1] / 2 - self.rect.height / 2 + (self.rect.height - self.rect.height * self.zoom) / 2))

        if self.attacking:
            if self.direction == "left":
                WINDOW.blit(self.weapons[self.weapon]["spriteDirs"][self.direction], (windowSize[0] / 2 - self.rect.width, windowSize[1] / 2))
            elif self.direction == "right":
                WINDOW.blit(self.weapons[self.weapon]["spriteDirs"][self.direction], (windowSize[0] / 2 + self.rect.width / 2, windowSize[1] / 2))
            elif self.direction == "up":
                WINDOW.blit(self.weapons[self.weapon]["spriteDirs"][self.direction], (windowSize[0] / 2 - self.weapons[self.weapon]["spriteDirs"][self.direction].get_width() + self.weaponOffseX, windowSize[1] / 2 - self.rect.height))
            elif self.direction == "down":
                WINDOW.blit(self.weapons[self.weapon]["spriteDirs"][self.direction], (windowSize[0] / 2 - self.weapons[self.weapon]["spriteDirs"][self.direction].get_width() + self.weaponOffseX, windowSize[1] / 2 + self.rect.height / 2))
        
    def drawHUD(self, WINDOW):
        self.handleHealth(WINDOW)

    def handleAcceleration(self, dt, input):
        if input.y and not self.attacking:
            if self.velocity.y != 0 and sign(self.velocity.y) != sign(input.y):
                self.velocity.y = clamp(self.velocity.y + self.friction * dt * input.y, 0, self.velocity.y)
            else:
                self.velocity.y = pygame.math.clamp(self.velocity.y + self.acceleration * dt * input.y, -self.maxSpeed, self.maxSpeed)
        else:
            self.velocity.move_towards_ip(pygame.math.Vector2(self.velocity.x, 0), self.friction * dt)
        
        if input.x and not self.attacking:
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
            if self.timers["grace"].active:
                moveBy = self.velocity * dt
            else:
                moveBy = self.velocity.normalize() * min(self.velocity.length(), self.maxSpeed) * dt
            movedRect = self.rect.move(moveBy.x, 0)
            if movedRect.collidelist(walls) == -1:
                self.rect = movedRect
            movedRect = self.rect.move(0, moveBy.y)
            if movedRect.collidelist(walls) == -1:
                self.rect = movedRect
    
    def handleAttack(self, attackInput):
        if self.weapon == "none" or self.zoom != 1:
            return
        if attackInput and not self.timers["attack"].active and not self.timers["attackCooldown"].active:
            self.attacking = True
            self.timers["attack"].start()
            self.timers["attackCooldown"].start()
            self.sounds["attack"].play()
        if self.timers["attack"].active:
            self.changeAnimation("attack")
            if self.direction == "left" or self.direction == "right":
                self.activeWeaponHitbox = "horizontal"
                if self.direction == "left":
                    self.weaponHitboxes[self.activeWeaponHitbox].right = self.rect.x
                    self.weaponHitboxes[self.activeWeaponHitbox].centery = self.rect.centery
                else:
                    self.weaponHitboxes[self.activeWeaponHitbox].x = self.rect.right
                    self.weaponHitboxes[self.activeWeaponHitbox].centery = self.rect.centery
            else:
                self.activeWeaponHitbox = "vertical"
                if self.direction == "up":
                    self.weaponHitboxes[self.activeWeaponHitbox].centerx = self.rect.centerx
                    self.weaponHitboxes[self.activeWeaponHitbox].bottom = self.rect.top
                else:
                    self.weaponHitboxes[self.activeWeaponHitbox].centerx = self.rect.centerx
                    self.weaponHitboxes[self.activeWeaponHitbox].top = self.rect.bottom
        else:
            self.attacking = False
    
    def updateAnimations(self, dt, input):
        if not self.dead:
            if not self.attacking:
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
    
    def updateZoom(self, dt):
        if not self.velocity.length() and not self.attacking:
            if not self.timers["zoomOut"].active:
                self.zoom = max(self.zoom - dt * self.zoomSpeed, self.zoomMin)
            else:
                self.zoom = min(self.zoom + dt * self.zoomSpeed, 1)
        else:
            self.timers["zoomOut"].start()
            self.zoom = min(self.zoom + dt * self.zoomSpeed, 1)
    
    def handleDamage(self, enemiesGroup):
        if self.timers["grace"].active or self.dead: return
        hit_list = pygame.sprite.spritecollide(self, enemiesGroup, False)
        hit = False
        for sprite in hit_list:
            if sprite.dead or sprite.timers["attackCooldown"].active: continue
            if self.velocity.length() < SQRT2:
                self.velocity.x = 1
            self.velocity.rotate_ip(self.velocity.angle_to((self.rect.x - sprite.rect.x, self.rect.y - sprite.rect.y)))
            self.velocity = self.velocity.normalize() * self.knockback
            hit = True
            damage = sprite.damage
            sprite.timers["attackCooldown"].start()
        
        if hit:
            self.sounds["hit"].play()
            self.timers["grace"].start()
            self.health -= damage
    
    def handleHealth(self, WINDOW):
        heartsOver = self.health % 4
        fullHearts = self.health - heartsOver
        fullHearts /= 4
        maxHearts = self.maxHealth // 4
        for i in range(maxHearts):
            if i < fullHearts:
                WINDOW.blit(self.heartSprites[0], (i * self.heartSize[0], 0))
            elif fullHearts == i and heartsOver:
                if heartsOver == 3:
                    WINDOW.blit(self.heartSprites[1], (i * self.heartSize[0], 0))
                elif heartsOver == 2:
                    WINDOW.blit(self.heartSprites[2], (i * self.heartSize[0], 0))
                else:
                    WINDOW.blit(self.heartSprites[3], (i * self.heartSize[0], 0))
            else:
                WINDOW.blit(self.heartSprites[4], (i * self.heartSize[0], 0))

    
    def updateTimers(self, dt):
        for timer in self.timers:
            self.timers[timer].update(dt)
    
    def changeAnimation(self, anim):
        if anim != self.animation:
            self.animation = anim
            self.currentFrame = 0.0