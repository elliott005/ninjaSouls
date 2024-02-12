import pygame, pickle
import mapLoader
from os.path import isfile

mapTileSize = pygame.math.Vector2(16, 16)
size = (64, 64)

fontTalk = pygame.font.Font("assets/NinjaAdventure/HUD/Font/NormalFont.ttf", 32)
fontMenu = pygame.font.Font("assets/NinjaAdventure/HUD/Font/NormalFont.ttf", 128)

savePathPlayer = "saves/player.save"
savePathWorld = "saves/world.save"

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

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range") 

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
    def unpause(self):
        self.active = True
    def stop(self):
        self.active == False
        self.time = self.waitTime

def collidedictlist(p_rect, p_dict):
    for k in p_dict:
        if p_rect.collidelist(p_dict[k]) != -1:
            return k
    return "none"

def collideClassList(p_rect, p_list):
    for i in p_list:
        if p_rect.colliderect(i.rect):
            return i
    return -1

def loadGame(player, Enemy, Item, area=-1):
    if isfile(savePathPlayer) and isfile(savePathWorld):
        area = loadPlayerState(player, area)
        enemies, items, worldSave = loadWorldState(Enemy, Item, area)
        return enemies, items, area, worldSave
    else:
        if area == -1:
            return -1, -1, "Overworld", {}
        return -1, -1, area, {}

def loadPlayerState(player, area=-1):
    with open(savePathPlayer, "rb") as f:
        playerSave = pickle.load(f)
    # print("player: ", area, playerSave["area"])
    if area == playerSave["area"] or area == -1:
        player.rect.topleft = playerSave["pos"]
    player.health = playerSave["health"]
    player.maxHealth = playerSave["maxHealth"]
    player.weapon = playerSave["weapon"]
    player.equipedItem = playerSave["item"]
    for weapon in playerSave["weapons"]:
        player.weapons[weapon]["unlocked"] = playerSave["weapons"][weapon]["unlocked"]
    for item in playerSave["items"]:
        player.items[item]["unlocked"] =  playerSave["items"][item]["unlocked"]
        player.items[item]["amount"] =  playerSave["items"][item]["amount"]
    if area == -1:
        return playerSave["area"]
    else:
        return area

def loadWorldState(Enemy, Item, area):
    with open(savePathWorld, "rb") as f:
        worldSave = pickle.load(f)
    # print("world: ", area, worldSave)
    if area in worldSave:
        enemies = mapLoader.extendedGroup()
        items = mapLoader.extendedGroup()
        for enemy in worldSave[area]["enemies"]:
            Enemy(enemy["pos"], size, enemy["type"], enemy["dead"], enemies)
        for item in worldSave[area]["items"]:
            Item(item["pos"], item["type"], item["dead"], items)
        return enemies, items, worldSave
    else:
        return -1, -1, worldSave

def saveGame(player, enemies, itemsGroup, area, worldSave):
    savePlayerState(player, area)
    return saveWorldState(enemies, itemsGroup, area, worldSave)

def saveWorldState(enemies, itemsGroup, area, worldSave):
    worldSave[area] = {}
    worldSave[area]["enemies"] = []
    worldSave[area]["items"] = []
    # print("world before: ", area, worldSave)
    for enemy in enemies:
        worldSave[area]["enemies"].append({"pos": enemy.rect.topleft, "type": enemy.type, "dead": enemy.dead})
    for item in itemsGroup:
        worldSave[area]["items"].append({"pos": item.rect.topleft, "type": item.type, "dead": item.trulyDead})
    # print("world after: ", area, worldSave)
    
    with open(savePathWorld, "wb") as f:
        pickle.dump(worldSave, f)
    
    return worldSave

def savePlayerState(player, area):
    playerSave = {
        "pos": player.rect.topleft,
        "health": player.health,
        "maxHealth": player.maxHealth,
        "weapon": player.weapon,
        "weapons": {},
        "area": area,
        "items": {} ,
        "item": player.equipedItem
        }
    for weapon in player.weapons:
        playerSave["weapons"][weapon] = {"unlocked": player.weapons[weapon]["unlocked"]}
    for item in player.items:
        playerSave["items"][item] = {"unlocked": player.items[item]["unlocked"], "amount": player.items[item]["amount"]}
    with open(savePathPlayer, "wb") as f:
        pickle.dump(playerSave, f)

def transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="rect", dir=1, background=None):
    windowSize = pygame.display.get_window_size()
    if type == "rect":
        rect = pygame.Rect(-windowSize[0], 0, windowSize[0], windowSize[1])
        if dir < 0:
            rect.x = 0
        while 1:
            if rect.x > 0 and dir == 1:
                break
            elif rect.x > windowSize[0] and dir == -1:
                break
            dt = fpsClock.get_time() / 1000
            rect.x += dt * 900
            if not background is None:
                WINDOW.fill(BACKGROUNDCOLOR)
                WINDOW.blit(background, (0, 0))
            pygame.draw.rect(WINDOW, (0, 0, 0), rect)
            pygame.display.update()
            fpsClock.tick(30)
    elif type == "circle":
        dist = pygame.math.Vector2(windowSize[0] / 2, windowSize[1] / 2).distance_to(pygame.math.Vector2(0, 0)) + 200
        radius = 1
        if dir < 0:
            radius = dist
        alpha = 255
        while 1:
            dt = fpsClock.get_time() / 1000
            if radius <= 0 and dir == -1:
                alpha -= 300 * dt
            elif radius >= dist and dir == 1:
                alpha -= 300 * dt
            else:
                radius += dt * 900 * dir
            if not background is None:
                WINDOW.fill(BACKGROUNDCOLOR)
                WINDOW.blit(background, (0, 0))
            if alpha <= 0.0:
                break
            pygame.draw.circle(WINDOW, (0, 0, 0, alpha), (windowSize[0] / 2, windowSize[1] / 2), radius)
            pygame.display.update()
            fpsClock.tick(30)
    elif type == "fadeToBlack":
        alpha = 0
        rect = pygame.Surface(windowSize, pygame.SRCALPHA)
        while 1:
            dt = fpsClock.get_time() / 1000
            alpha += 300 * dt
            if not background is None:
                WINDOW.fill(BACKGROUNDCOLOR)
                WINDOW.blit(background, (0, 0))
            if alpha >= 255.0:
                break
            rect.fill((0, 0, 0, alpha))
            WINDOW.blit(rect, (0, 0))
            pygame.display.update()
            fpsClock.tick(30)
    elif type == "fadeFromBlack":
        alpha = 255
        rect = pygame.Surface(windowSize, pygame.SRCALPHA)
        while 1:
            dt = fpsClock.get_time() / 1000
            alpha -= 300 * dt
            if not background is None:
                WINDOW.fill(BACKGROUNDCOLOR)
                WINDOW.blit(background, (0, 0))
            if alpha <= 0.0:
                break
            rect.fill((0, 0, 0, alpha))
            WINDOW.blit(rect, (0, 0))
            pygame.display.update()
            fpsClock.tick(30)