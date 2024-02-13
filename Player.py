import pygame, math, random
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
        self.zoomSpeedInCombat = 1
        self.zoom = 1

        spriteSize = mapTileSize.x
        idleSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/GreenNinja/SeparateAnim/Idle.png").convert_alpha()
        walkSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/GreenNinja/SeparateAnim/Walk.png").convert_alpha()
        attackSpriteSheet = pygame.image.load("assets/NinjaAdventure/Actor/Characters/GreenNinja/SeparateAnim/Attack.png").convert_alpha()
        spriteSheetDeath = pygame.image.load("assets/NinjaAdventure/FX/Magic/Circle/SpriteSheetOrange.png").convert_alpha()
        spriteSheetItem = pygame.image.load("assets/NinjaAdventure/FX/Magic/Spirit/SpriteSheetBlue.png").convert_alpha()
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
            "zoomOut": Timer(2.0, True),
            "attack": Timer(0.5),
            "grace": Timer(0.1),
            "attackCooldown": Timer(1),
            "death": Timer(self.animations["dead"]["max"] / self.animations["dead"]["speed"]),
        }

        self.weapon = "Katana"
        self.attacking = False
        self.weaponOffseX = 5

        self.weapons = {
            "Katana": {"sprite": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Weapons/Katana/SpriteInHand.png"), (math.floor(size[0] / 2), math.floor(size[1] / 2))),
                       "spriteMenu": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Weapons/Katana/Sprite.png"), self.heartSize),  
                       "damage": 1, "knockback": 500, "unlocked": True},
            "Axe": {"sprite": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Weapons/Axe/SpriteInHand.png"), (math.floor(size[0] / 2), math.floor(size[1] / 2))),
                    "spriteMenu": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Weapons/Axe/Sprite.png"), self.heartSize), 
                    "damage": 2, "knockback": 700, "unlocked": True}
        }
        self.weaponIndex = 0
        self.weaponIndexMax = 2

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
        self.changeWeaponOnce = False

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

        self.talkRadius = 150
        self.talking = False
        self.talkingIndex = 0
        self.talkSpeed = 15
        self.talkSpeedNormal = self.talkSpeed
        self.talkSpeedFast = 120
        self.talkSounds = [pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/Voice4.wav"), 
                           pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/Voice1.wav"),
                           pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/Voice3.wav"),
                           pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/Voice2.wav")]
        self.dialogueText = ""
        self.talkInputOnce = False
        self.NPCFace = -1
        windowSize = pygame.display.get_window_size()
        self.dialogBox = pygame.image.load("assets/NinjaAdventure/HUD/Dialog/DialogBox.png")
        self.dialogBox = pygame.transform.scale(self.dialogBox, (windowSize[0], self.dialogBox.get_height() + 50))

        plantSpellSpriteSheet = pygame.image.load("assets/NinjaAdventure/FX/Elemental/Plant/SpriteSheet.png")
        self.items = {
            "plantSpell": {"spriteMenu": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Scroll/ScrollPlant.png"), self.heartSize), "sound": pygame.mixer.Sound("assets/swish-2.wav"), "hitbox": pygame.rect.Rect((0, 0), (size[0] * 2.5, size[1] * 2.5)), "damage": 4, "knockback": 800, "amount": 1, "unlocked": True},
            "potionHealth": {"spriteMenu": pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Potion/LifePot.png"), self.heartSize), "healAmount": 4, "amount": 2, "unlocked": True}
        }
        self.equipedItem = "potionHealth"
        self.changeItemOnce = False
        self.itemIndex = 0
        self.itemIndexMax = 2
        self.itemPickupSound = pygame.mixer.Sound("assets/NinjaAdventure/Sounds/Game/PowerUp1.wav")
        self.usingItem = False
        plantSpellSpriteSize = 28
        self.itemAnims = {
            "plantSpell": {
                "frames": [pygame.transform.scale(plantSpellSpriteSheet.subsurface(pygame.Rect(plantSpellSpriteSize * x, plantSpellSpriteSize * 0, plantSpellSpriteSize, plantSpellSpriteSize)), (size[0] * 2, size[1] * 2)) for x in range(0, 8)],
                "max": 8,
                "speed": 7
            },
            "potionHealth": {
                "frames": [pygame.transform.scale(spriteSheetItem.subsurface(pygame.Rect(deathSize * x, deathSize * 0, deathSize, deathSize)), size) for x in range(0, 4)],
                "max": 4,
                "speed": 7
            }
        }
        self.itemAnimCurrentFrame = 0.0
    
    def update(self, dt, joystick, walls, enemiesGroup, NPCs, inCombat, itemsGroup):
        keysPressed = pygame.key.get_pressed()
        if joystick == -1:
            input = pygame.math.Vector2(checkInput(keysPressed, "moveRight") - checkInput(keysPressed, "moveLeft"), checkInput(keysPressed, "moveDown") - checkInput(keysPressed, "moveUp"))
            attackInput = checkInput(keysPressed, "attack")
        else:
            input = pygame.math.Vector2(checkInputController(joystick, "moveHorizontal"), checkInputController(joystick, "moveVertical"))
            attackInput = checkInputController(joystick, "attack")
        if not self.dead:
            self.handleAcceleration(dt, input)
            self.move(dt, walls)
            self.handleAttack(attackInput)
            self.handleUseItem(dt, checkInput(keysPressed, "useItem") if joystick == -1 else checkInputController(joystick, "useItem"), itemsGroup)
        self.updateAnimations(dt, input)

        self.handleDamage(enemiesGroup)

        self.handleTalk(dt, checkInput(keysPressed, "talk") if joystick == -1 else checkInputController(joystick, "talk"), NPCs)

        self.updateZoom(dt, inCombat)
        self.updateTimers(dt)

        if ((checkInput(keysPressed, "changeWeapon") and joystick == -1) or (joystick != -1 and checkInputController(joystick, "changeWeapon"))):
            if not self.changeWeaponOnce and not self.attacking:
                self.changeWeaponOnce = True
                self.weaponIndex += 1
                if self.weaponIndex >= self.weaponIndexMax:
                    self.weaponIndex = 0
                self.weapon = get_nth_key(self.weapons, self.weaponIndex)
        else:
            self.changeWeaponOnce = False
        
        if (checkInput(keysPressed, "changeItem") and joystick == -1) or (joystick != -1 and checkInputController(joystick, "changeItem")):
            if not self.changeItemOnce and not self.usingItem:
                self.changeItemOnce = True
                self.itemIndex += 1
                if self.itemIndex >= self.itemIndexMax:
                    self.itemIndex = 0
                self.equipedItem = get_nth_key(self.items, self.itemIndex)
        else:
            self.changeItemOnce = False

        if self.health < 1:
            self.dead = True
            if not self.startDeathTimerOnce:
                self.sounds["gameOver"].play()
                self.timers["death"].start()
            self.startDeathTimerOnce = True
            if not self.timers["death"].active:
                self.direction = "down"
                self.animation = "idle"
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
        
        if self.usingItem:
            if self.zoom == 1:
                WINDOW.blit(self.itemAnims[self.equipedItem]["frames"][math.floor(self.itemAnimCurrentFrame)], (windowSize[0] / 2 - self.rect.width, windowSize[1] / 2 - self.rect.height))
            else:
                WINDOW.blit(pygame.transform.scale(self.itemAnims[self.equipedItem]["frames"][math.floor(self.itemAnimCurrentFrame)], (self.rect.width * self.zoom * 2, self.rect.height * self.zoom * 2)), (windowSize[0] / 2 - self.rect.width + (self.rect.width - self.rect.width * self.zoom) / 2, windowSize[1] / 2 - self.rect.height + (self.rect.height - self.rect.height * self.zoom) / 2))

    def drawHUD(self, WINDOW):
        self.handleHealth(WINDOW)
        WINDOW.blit(self.items[self.equipedItem]["spriteMenu"], (0, 128))
        WINDOW.blit(fontMenu.render(str(self.items[self.equipedItem]["amount"]), False, (100, 0, 0)), (0, 200))
        WINDOW.blit(self.weapons[self.weapon]["spriteMenu"], (0, 350))
        if self.talking:
            windowSize = pygame.display.get_window_size()
            WINDOW.blit(self.NPCFace, (0, windowSize[1] - self.dialogBox.get_height() - 100))
            WINDOW.blit(self.dialogBox, (self.NPCFace.get_width(), windowSize[1] - self.dialogBox.get_height() - 100))
            WINDOW.blit(fontTalk.render(self.dialogueText[:math.floor(self.talkingIndex)], False, (0, 0, 0)), (192, windowSize[1] - self.dialogBox.get_height() / 2 - 125))

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
        if self.weapon == "none" or self.zoom != 1 or self.usingItem:
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
        
    def handleUseItem(self, dt, input, itemsGroup):
        for item in itemsGroup:
            if not item.trulyDead and self.rect.colliderect(item.rect):
                if item.type == "heart":
                    self.health = min(self.health + item.healAmount, self.maxHealth)
                else:
                    self.items[item.type]["amount"] += 1
                item.trulyDead = True
                self.itemPickupSound.play()
                break
        if input and not self.usingItem:
            if self.items[self.equipedItem]["amount"] > 0:
                self.usingItem = True
                self.items[self.equipedItem]["amount"] -= 1
                if "hitbox" in self.items[self.equipedItem]:
                    self.items[self.equipedItem]["sound"].play()
        if self.usingItem:
            if "hitbox" in self.items[self.equipedItem]:
                self.items[self.equipedItem]["hitbox"].center = self.rect.center
            self.itemAnimCurrentFrame += dt * self.itemAnims[self.equipedItem]["speed"]
            if self.itemAnimCurrentFrame >= self.itemAnims[self.equipedItem]["max"]:
                self.itemAnimCurrentFrame = 0.0
                self.usingItem = False
                if self.equipedItem == "potionHealth":
                    self.health = min(self.health + self.items[self.equipedItem]["healAmount"], self.maxHealth)
    
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
    
    def updateZoom(self, dt, inCombat):
        if not self.velocity.length() and not self.attacking and not inCombat:
            if not self.timers["zoomOut"].active:
                self.zoom = max(self.zoom - dt * self.zoomSpeed, self.zoomMin)
            else:
                self.zoom = min(self.zoom + dt * self.zoomSpeed, 1)
        else:
            self.timers["zoomOut"].start()
            if inCombat:
                self.zoom = min(self.zoom + dt * self.zoomSpeedInCombat, 1)
            else:
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
    
    def handleTalk(self, dt, input, NPCs):
        if not input:
            self.talkInputOnce = False
        if input and self.talkInputOnce:
            input = False
        if input:
            self.talkInputOnce = True
        if input or self.talking:
            self.talking = False
            closest = -1
            for NPC_idx in NPCs:
                dist = pygame.math.Vector2(NPC_idx.rect.topleft).distance_to(pygame.math.Vector2(self.rect.topleft))
                if dist < self.talkRadius:
                    if closest == -1 or dist < closest:
                        NPC = NPC_idx
                        closest = dist
                        self.talking = True
                        self.dialogueText = NPC_idx.dialogue[NPC.numTalk]
                        self.NPCFace = NPC_idx.animations["face"]
                    # break
            if self.talking:
                if self.talkingIndex > 0.0 and input:
                    self.talkSpeed = self.talkSpeedFast
                talkIndexStart = self.talkingIndex
                self.talkingIndex += self.talkSpeed * dt
                if self.talkingIndex >= len(self.dialogueText):
                    self.talkingIndex = len(self.dialogueText)
                    if input:
                        self.talkSpeed = self.talkSpeedNormal
                        self.talkingIndex = 0
                        NPC.numTalk += 1
                        if NPC.numTalk > len(NPC.dialogue) - 1:
                            self.talking = False
                            NPC.numTalk = len(NPC.dialogue) - 1
                elif self.talkingIndex >= math.ceil(talkIndexStart):
                    self.talkSounds[random.randint(0, len(self.talkSounds) - 1)].play()
        else:
            self.talkingIndex = 0
    
    def updateTimers(self, dt):
        for timer in self.timers:
            self.timers[timer].update(dt)
    
    def changeAnimation(self, anim):
        if anim != self.animation:
            self.animation = anim
            self.currentFrame = 0.0