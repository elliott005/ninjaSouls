import pygame, math
from pygame.surface import Surface
from Enemy import Enemy
from NPC import NPC
from Item import Item
from CuttableGrass import CuttableGrass
from pytmx.util_pygame import load_pygame

coinSprite = pygame.transform.scale(pygame.image.load("assets/NinjaAdventure/Items/Treasure/GoldCoin.png"), (16, 16))
coinHeight = coinSprite.get_height()
fontPrice = pygame.font.Font("assets/NinjaAdventure/HUD/Font/NormalFont.ttf", 32)
priceOffsetY = 32
priceOffsetX = 8

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, surf, groups):
        super().__init__(groups)
        self.rect = pygame.Rect(pos, size)
        self.image = pygame.transform.scale(surf, size)

class extendedGroup(pygame.sprite.Group):
    def draw(self, surface: Surface, playerPos, p_zoom):
        sprites = self.sprites()
        surface_blit = surface.blit
        windowSize = pygame.display.get_window_size()
        zoom = round(p_zoom, 2)
        if zoom == 1:
            for spr in sprites:
                if hasattr(spr, "trulyDead") and spr.trulyDead: continue
                topleft = spr.rect.topleft
                pos = (topleft[0] - playerPos[0] + windowSize[0] / 2, topleft[1] - playerPos[1] + windowSize[1] / 2)
                if hasattr(spr, "price") and spr.price != -1:
                    surface_blit(coinSprite, (pos[0] + priceOffsetX, pos[1] + priceOffsetY))
                    surface_blit(fontPrice.render(str(spr.price), False, (0, 0, 0)), (pos[0] + priceOffsetX, pos[1] + priceOffsetY + coinHeight))
                if -spr.rect.width < pos[0] < windowSize[0] and -spr.rect.height < pos[1] < windowSize[1]:
                    self.spritedict[spr] = surface_blit(spr.image, pos)
        else:
            scaledImgs = {}
            for spr in sprites:
                if hasattr(spr, "trulyDead") and spr.trulyDead: continue
                topleft = spr.rect.topleft
                pos = (math.floor((topleft[0] - playerPos[0]) * zoom + windowSize[0] / 2), math.floor((topleft[1] - playerPos[1]) * zoom + windowSize[1] / 2))
                if hasattr(spr, "price") and spr.price != -1:
                    posCoin = (math.floor((topleft[0] - playerPos[0] + priceOffsetX) * zoom + windowSize[0] / 2), math.floor((topleft[1] - playerPos[1] + priceOffsetY) * zoom + windowSize[1] / 2))
                    surface_blit(pygame.transform.scale(coinSprite, (math.ceil(coinSprite.get_width() * zoom), math.ceil(coinHeight * zoom))), posCoin)
                    price = fontPrice.render(str(spr.price), False, (0, 0, 0))
                    posPrice = (math.floor((topleft[0] - playerPos[0] + priceOffsetX) * zoom + windowSize[0] / 2), math.floor((topleft[1] - playerPos[1] + priceOffsetY + coinHeight) * zoom + windowSize[1] / 2))
                    surface_blit(pygame.transform.scale(price, (math.ceil(price.get_width() * zoom), math.ceil(price.get_height() * zoom))), posPrice)
                if -spr.rect.width < pos[0] < windowSize[0] and -spr.rect.height < pos[1] < windowSize[1]:
                    bytesStr = pygame.image.tobytes(spr.image, "RGB")
                    if bytesStr in scaledImgs:
                        self.spritedict[spr] = surface_blit(scaledImgs[bytesStr], pos)
                    else:
                        scaledImgs[bytesStr] = pygame.transform.scale(spr.image, (math.ceil(spr.image.get_width() * zoom), math.ceil(spr.image.get_width() * zoom)))
                        self.spritedict[spr] = surface_blit(scaledImgs[bytesStr], pos)
        self.lostsprites = []

def changeMap(whichMap, sizeX, sizeY, mapTileSize):
    data = load_pygame(whichMap)
    mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations, NPCsGroup, itemsGroup, cuttableGrass, breakableRocks, treasureChests = loadMap(data, sizeX, sizeY, mapTileSize)
    return mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations, NPCsGroup, itemsGroup, cuttableGrass, breakableRocks, treasureChests

def loadMap(data, sizeX, sizeY, mapTileSize):
    sprite_group = extendedGroup()
    sprite_group_front = extendedGroup()
    walls = []
    breakableRocks = []
    treasureChests = []
    musicAreas = {}
    doorAreas = {}
    doorDestinations = {}
    enemiesGroup = extendedGroup()
    NPCsGroup = extendedGroup()
    tilesets = {}
    itemsGroup = extendedGroup()
    cuttableGrass = extendedGroup()
    k = pygame.math.Vector2(sizeX / mapTileSize.x, sizeY / mapTileSize.y)
    for idx, layer in enumerate(data.visible_layers):
        # print(layer.__dict__)
        if hasattr(layer, "data"):
            if layer.name == "ObjectsFront":
                for x, y, surf in layer.tiles():
                    Tile((x * sizeX, y * sizeY), (sizeX, sizeY), surf, sprite_group_front)
            elif layer.name == "Enemies":
                for x, y, surf in layer.tiles():
                    gid = data.get_tile_gid(x, y, idx)
                    if not gid in tilesets:
                        tilesets[gid] = data.get_tileset_from_gid(gid)
                    Enemy((x * sizeX, y * sizeY), (sizeX, sizeY), tilesets[gid].name, False, enemiesGroup)
            elif layer.name == "NPCs":
                for x, y, surf in layer.tiles():
                    gid = data.get_tile_gid(x, y, idx)
                    if not gid in tilesets:
                        tilesets[gid] = data.get_tileset_from_gid(gid)
                    NPC((x * sizeX, y * sizeY), (sizeX, sizeY), tilesets[gid].name, NPCsGroup)
            elif layer.name == "CuttableGrass":
                for x, y, surf in layer.tiles():
                    # print((x * sizeX, y * sizeY))
                    CuttableGrass((x * sizeX, y * sizeY), (sizeX, sizeY), surf, cuttableGrass)
            else:
                for x, y, surf in layer.tiles():
                    # print(data.get_tile_gid(x, y, idx))
                    Tile((x * sizeX, y * sizeY), (sizeX, sizeY), surf, sprite_group)
        elif layer.name == "Walls":
            for obj in layer:
                walls.append(pygame.Rect(obj.x * k.x, obj.y * k.y, obj.width * k.x, obj.height * k.y))
        elif layer.name == "BreakableRocks":
            for obj in layer:
                breakableRocks.append({"rect": pygame.Rect(obj.x * k.x, obj.y * k.y, obj.width * k.x, obj.height * k.y), "resources": 0})
        elif layer.name == "Chests":
            for obj in layer:
                treasureChests.append({"rect": pygame.Rect(obj.x * k.x, obj.y * k.y, obj.width * k.x, obj.height * k.y),
                                       "little": "little" in obj.name, "open": False,
                                       "loot": obj.type.split("_")})
        elif layer.name == "Music":
            for obj in layer:
                if not obj.name in musicAreas:
                    musicAreas[obj.name] = []
                musicAreas[obj.name].append(pygame.Rect(obj.x * k.x, obj.y * k.y, obj.width * k.x, obj.height * k.y))
        elif layer.name == "Doors":
            for obj in layer:
                if not obj.name in doorAreas:
                    doorAreas[obj.name] = []
                doorAreas[obj.name].append(pygame.Rect(obj.x * k.x, obj.y * k.y, obj.width * k.x, obj.height * k.y))
        elif layer.name == "DoorDestinations":
            for obj in layer:
                doorDestinations[obj.name] = (obj.x * k.x, obj.y * k.y)
        elif layer.name == "Items":
            for obj in layer:
                Item((obj.x * k.x, obj.y * k.y), obj.name, False, itemsGroup)
        elif layer.name == "ItemsPurchase":
            for obj in layer:
                Item((obj.x * k.x, obj.y * k.y), obj.name, False, itemsGroup, price=int(obj.type))
    return sprite_group, sprite_group_front, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations, NPCsGroup, itemsGroup, cuttableGrass, breakableRocks, treasureChests