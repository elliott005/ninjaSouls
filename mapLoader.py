import pygame, math
from pygame.surface import Surface
from Enemy import Enemy
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, surf, gid, groups):
        super().__init__(groups)
        self.rect = pygame.Rect(pos, size)
        self.image = pygame.transform.scale(surf, size)
        self.gid = gid

class extendedGroup(pygame.sprite.Group):
    def draw(self, surface: Surface, playerPos, p_zoom):
        sprites = self.sprites()
        surface_blit = surface.blit
        windowSize = pygame.display.get_window_size()
        zoom = round(p_zoom, 2)
        if zoom == 1:
            for spr in sprites:
                topleft = spr.rect.topleft
                pos = (topleft[0] - playerPos[0] + windowSize[0] / 2, topleft[1] - playerPos[1] + windowSize[1] / 2)
                if -spr.rect.width < pos[0] < windowSize[0] and -spr.rect.height < pos[1] < windowSize[1]:
                    self.spritedict[spr] = surface_blit(spr.image, pos)
        else:
            scaledImgs = {}
            for spr in sprites:
                topleft = spr.rect.topleft
                pos = (math.floor((topleft[0] - playerPos[0]) * zoom + windowSize[0] / 2), math.floor((topleft[1] - playerPos[1]) * zoom + windowSize[1] / 2))
                if -spr.rect.width < pos[0] < windowSize[0] and -spr.rect.height < pos[1] < windowSize[1]:
                    if spr.gid in scaledImgs:
                        self.spritedict[spr] = surface_blit(scaledImgs[spr.gid], pos)
                    else:
                        scaledImgs[spr.gid] = pygame.transform.scale(spr.image, (math.ceil(spr.rect.width * zoom), math.ceil(spr.rect.height * zoom)))
                        self.spritedict[spr] = surface_blit(scaledImgs[spr.gid], pos)
        self.lostsprites = []

def changeMap(whichMap, sizeX, sizeY, mapTileSize):
    data = load_pygame(whichMap)
    mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations = loadMap(data, sizeX, sizeY, mapTileSize)
    return mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations

def loadMap(data, sizeX, sizeY, mapTileSize):
    sprite_group = extendedGroup()
    sprite_group_front = extendedGroup()
    walls = []
    musicAreas = {}
    doorAreas = {}
    doorDestinations = {}
    enemiesGroup = extendedGroup()
    tilesets = {}
    k = pygame.math.Vector2(sizeX / mapTileSize.x, sizeY / mapTileSize.y)
    for idx, layer in enumerate(data.visible_layers):
        # print(layer.__dict__)
        if hasattr(layer, "data"):
            if layer.name == "ObjectsFront":
                for x, y, surf in layer.tiles():
                    Tile((x * sizeX, y * sizeY), (sizeX, sizeY), surf, data.get_tile_gid(x, y, idx), sprite_group_front)
            elif layer.name == "Enemies":
                for x, y, surf in layer.tiles():
                    gid = data.get_tile_gid(x, y, idx)
                    if not gid in tilesets:
                        tilesets[gid] = data.get_tileset_from_gid(gid)
                    Enemy((x * sizeX, y * sizeY), (sizeX, sizeY), tilesets[gid].name, gid, enemiesGroup)
            else:
                for x, y, surf in layer.tiles():
                    # print(data.get_tile_gid(x, y, idx))
                    Tile((x * sizeX, y * sizeY), (sizeX, sizeY), surf, data.get_tile_gid(x, y, idx), sprite_group)
        elif layer.name == "Walls":
            for obj in layer:
                walls.append(pygame.Rect(obj.x * k.x, obj.y * k.y, obj.width * k.x, obj.height * k.y))
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
    return sprite_group, sprite_group_front, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations