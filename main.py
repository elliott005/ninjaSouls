import pygame, sys
from pygame.locals import *
from pytmx.util_pygame import load_pygame

from inputs import *
from mapLoader import *
from Player import *

pygame.init()

FPS = 60
fpsClock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((0, 0))
BACKGROUNDCOLOR = (100, 100, 220)

def main():
    mapTileSize = pygame.math.Vector2(16, 16)
    mapPath = "maps/test.tmx"
    mapData = load_pygame(mapPath)
    scaleTo = (64, 64)
    mapSprites, mapSpritesFront, walls = loadMap(mapData, scaleTo[0], scaleTo[1], mapTileSize)

    # mapSize = (scaleTo[0] * 60, scaleTo[1] * 60)

    player = Player((100, 100), (64, 64))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if checkInputKey(event.key, "quit"):
                    pygame.quit()
                    sys.exit()
        
        dt = fpsClock.get_time() / 1000
        player.update(dt, walls)
        mapSprites.update(player.rect.topleft)
        
        WINDOW.fill(BACKGROUNDCOLOR)
        mapSprites.draw(WINDOW, player.rect.center, player.zoom)

        # for wall in walls:
        #     pygame.draw.rect(WINDOW, (100, 100, 100), wall)#pygame.Rect((wall.x - player.rect.x, wall.y - player.rect.y), (wall.width, wall.height)))

        # pygame.draw.rect(WINDOW, (100, 200, 200), player.rect)

        player.draw(WINDOW)

        mapSpritesFront.draw(WINDOW, player.rect.center, player.zoom)

        print(fpsClock.get_fps())

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()