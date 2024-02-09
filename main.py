import pygame, sys
from pygame.locals import *
from pytmx.util_pygame import load_pygame

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((0, 0))
BACKGROUNDCOLOR = (100, 100, 220)

from inputs import *
from mapLoader import *
from Player import *

def main():
    mapPath = "maps/test.tmx"
    mapData = load_pygame(mapPath)
    scaleTo = (64, 64)
    mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas = loadMap(mapData, scaleTo[0], scaleTo[1], mapTileSize)

    # mapSize = (scaleTo[0] * 60, scaleTo[1] * 60)

    music = {
        "adventureBegins": pygame.mixer.Sound("assets/NinjaAdventure/Musics/1 - Adventure Begin.ogg"),
        "theCave": pygame.mixer.Sound("assets/NinjaAdventure/Musics/2 - The Cave.ogg"),
    }
    whichMusic = "none"

    player = Player((100, 100), (64, 64))
    dead = False

    while 1:
        if dead:
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if checkInputKey(event.key, "quit"):
                    pygame.quit()
                    sys.exit()
        
        musicArea = collidedictlist(player.rect, musicAreas)
        # print(musicArea, whichMusic)
        if whichMusic != musicArea:
            if whichMusic == "none":
                whichMusic = musicArea
            else:
                music[whichMusic].fadeout(1000)
                whichMusic = "none"
            if musicArea != "none":
                whichMusic = musicArea
                music[whichMusic].play(loops=-1, fade_ms=1000)

        dt = fpsClock.get_time() / 1000
        dead = player.update(dt, walls, enemiesGroup)
        enemiesGroup.update(dt, pygame.math.Vector2(player.rect.left, player.rect.top), walls, playerAttackHitbox = player.weaponHitboxes[player.activeWeaponHitbox] if player.attacking else -1)
        # mapSprites.update(player.rect.topleft)
        
        WINDOW.fill(BACKGROUNDCOLOR)
        mapSprites.draw(WINDOW, player.rect.center, player.zoom)

        # for wall in walls:
        #     pygame.draw.rect(WINDOW, (100, 100, 100), wall)#pygame.Rect((wall.x - player.rect.x, wall.y - player.rect.y), (wall.width, wall.height)))

        # for k in musicAreas:
        #     for i in musicAreas[k]:
        #         pygame.draw.rect(WINDOW, (100, 100, 100), i)
        # pygame.draw.rect(WINDOW, (100, 200, 200), player.rect)

        player.draw(WINDOW)
        enemiesGroup.draw(WINDOW, player.rect.center, player.zoom)

        mapSpritesFront.draw(WINDOW, player.rect.center, player.zoom)

        player.drawHUD(WINDOW)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()