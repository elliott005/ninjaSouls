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
    overworldMapPath = "maps/test.tmx"
    mapData = load_pygame(overworldMapPath)
    scaleTo = (64, 64)
    k = pygame.math.Vector2(scaleTo[0] / mapTileSize.x, scaleTo[1] / mapTileSize.y)
    mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations = loadMap(mapData, scaleTo[0], scaleTo[1], mapTileSize)

    # mapSize = (scaleTo[0] * 60, scaleTo[1] * 60)

    music = {
        "adventureBegins": pygame.mixer.Sound("assets/NinjaAdventure/Musics/1 - Adventure Begin.ogg"),
        "theCave": pygame.mixer.Sound("assets/NinjaAdventure/Musics/2 - The Cave.ogg"),
        "fight": pygame.mixer.Sound("assets/NinjaAdventure/Musics/17 - Fight.ogg"),
    }
    whichMusic = "none"

    player = Player((100, 100), (64, 64))
    dead = False
    playerInCombat = False

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
        # print(musicArea, whichMusic, whichMusic != musicArea)
        if whichMusic != musicArea and not playerInCombat and not player.dead:
            if whichMusic == "none":
                whichMusic = musicArea
            else:
                music[whichMusic].fadeout(1000)
                whichMusic = "none"
            if musicArea != "none":
                whichMusic = musicArea
                music[whichMusic].play(loops=-1, fade_ms=1000)

        dt = pygame.math.clamp(fpsClock.get_time() / 1000, 0, 0.05)
        
        dead = player.update(dt, walls, enemiesGroup, playerInCombat)

        enemiesGroup.update(dt, pygame.math.Vector2(player.rect.left, player.rect.top), walls, playerAttackHitbox = player.weaponHitboxes[player.activeWeaponHitbox] if player.attacking else -1)
        playerInCombat = False
        if player.dead:
            if whichMusic != "none":
                if music[whichMusic].get_num_channels() != 0:
                    music[whichMusic].fadeout(200)
            if music["fight"].get_num_channels() != 0:
                music["fight"].fadeout(200)
        else:
            for enemy in enemiesGroup.sprites():
                if enemy.aggro:
                    playerInCombat = True
                    break
            if playerInCombat:
                if music["fight"].get_num_channels() == 0:
                    if whichMusic != "none":
                        if music[whichMusic].get_num_channels() != 0:
                            music[whichMusic].fadeout(500)
                    music["fight"].play(-1, fade_ms=500)
            else:
                if music["fight"].get_num_channels() != 0:
                    if whichMusic != "none":
                        if music[whichMusic].get_num_channels() == 0:
                            music[whichMusic].play(-1, fade_ms=500)
                    music["fight"].fadeout(500)
        
        doorEntered = collidedictlist(player.rect, doorAreas)
        if doorEntered != "none":
            transition(WINDOW, fpsClock, BACKGROUNDCOLOR)
            if "Overworld" in doorEntered:
                mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations = changeMap(overworldMapPath, scaleTo[0], scaleTo[1], mapTileSize)
                player.rect.topleft = doorDestinations[doorEntered]
            else:
                mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations = changeMap("maps/subAreas/" + doorEntered + ".tmx", scaleTo[0], scaleTo[1], mapTileSize)
                player.rect.topleft = doorDestinations[doorEntered]
            
            WINDOW.fill(BACKGROUNDCOLOR)
            mapSprites.draw(WINDOW, player.rect.center, player.zoom)
            player.draw(WINDOW)
            enemiesGroup.draw(WINDOW, player.rect.center, player.zoom)
            mapSpritesFront.draw(WINDOW, player.rect.center, player.zoom)
            player.drawHUD(WINDOW)
            transition(WINDOW, fpsClock, BACKGROUNDCOLOR, dir=-1, background=WINDOW.copy())
        # mapSprites.update(player.rect.topleft)
        
        WINDOW.fill(BACKGROUNDCOLOR)

        # for wall in walls:
        #     pygame.draw.rect(WINDOW, (100, 100, 100), wall)#pygame.Rect((wall.x - player.rect.x, wall.y - player.rect.y), (wall.width, wall.height)))

        # for k in musicAreas:
        #     for i in musicAreas[k]:
        #         pygame.draw.rect(WINDOW, (100, 100, 100), i)
        # pygame.draw.rect(WINDOW, (100, 200, 200), player.rect)

        mapSprites.draw(WINDOW, player.rect.center, player.zoom)

        player.draw(WINDOW)
        enemiesGroup.draw(WINDOW, player.rect.center, player.zoom)

        mapSpritesFront.draw(WINDOW, player.rect.center, player.zoom)

        player.drawHUD(WINDOW)

        pygame.display.update()
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()