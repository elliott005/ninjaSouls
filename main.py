import pygame, sys
from pygame.locals import *
from pytmx.util_pygame import load_pygame

pygame.init()

FPS = 30
fpsClock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((0, 0))
pygame.display.set_caption("Ninja Souls")
BACKGROUNDCOLOR = (100, 100, 220)

from inputs import *
from mapLoader import *
from Player import *
from Enemy import *
from Item import *
from Menu import *

def main():
    overworldMapPath = "maps/test.tmx"
    # mapData = load_pygame(overworldMapPath)
    scaleTo = (64, 64)
    k = pygame.math.Vector2(scaleTo[0] / mapTileSize.x, scaleTo[1] / mapTileSize.y)

    # mapSize = (scaleTo[0] * 60, scaleTo[1] * 60)

    music = {
        "adventureBegins": pygame.mixer.Sound("assets/NinjaAdventure/Musics/1 - Adventure Begin.ogg"),
        "theCave": pygame.mixer.Sound("assets/NinjaAdventure/Musics/2 - The Cave.ogg"),
        "fight": pygame.mixer.Sound("assets/NinjaAdventure/Musics/17 - Fight.ogg"),
        "goodTime": pygame.mixer.Sound("assets/NinjaAdventure/Musics/20 - Good Time.ogg"),
    }
    whichMusic = "none"

    player = Player((100, 100), (64, 64))
    dead = False
    playerInCombat = False
    # print()
    # for enemy in enemiesGroup.sprites():
    #     print(enemy.trulyDead)
    
    numJoysticksStart = pygame.joystick.get_count()
    numJoysticks = numJoysticksStart
    if numJoysticksStart != 0:
        joystick = pygame.joystick.Joystick(numJoysticksStart - 1)
        joystick.init()
    else:
        joystick = -1
    
    inMenu = True
    mainMenu = MainMenu(pygame.display.get_window_size())
    menuMusic = "goodTime"
    music[menuMusic].play(-1, fade_ms=500)
    pressedQuitButtonOnce = True
    mainMenu.draw(WINDOW)
    transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="circle", background=WINDOW.copy(), dir=-1)
    
    while 1:
        if inMenu:
            numJoysticksStart = numJoysticks
            numJoysticks = pygame.joystick.get_count()
            if numJoysticks != numJoysticksStart and numJoysticks != 0:
                joystick = pygame.joystick.Joystick(numJoysticks - 1)
                joystick.init()
            elif numJoysticks == 0:
                joystick = -1
            action = mainMenu.update(joystick)
            if action:
                match action:
                    case "startGame":
                        music[menuMusic].fadeout(500)
                        whichMusic = "none"
                        inMenu = False
                        transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="fadeToBlack", background=WINDOW.copy())
                        enemies, items, breakableRocksLoad, area, worldSave = loadGame(player, Enemy, Item)
                        if area == "Overworld":
                            mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations, NPCsGroup, itemsGroup, cuttableGrass, breakableRocks = changeMap(overworldMapPath, scaleTo[0], scaleTo[1], mapTileSize)
                        else:
                            mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations, NPCsGroup, itemsGroup, cuttableGrass, breakableRocks = changeMap("maps/subAreas/" + area + ".tmx", scaleTo[0], scaleTo[1], mapTileSize)

                        if enemies != -1:
                            enemiesGroup = enemies
                        if items != -1:
                            itemsGroup = items
                        if breakableRocksLoad != -1:
                            breakableRocks = breakableRocksLoad
                        drawWorld(player, mapSprites, mapSpritesFront, NPCsGroup, itemsGroup, enemiesGroup, cuttableGrass)
                        transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="fadeFromBlack", background=WINDOW.copy())
                    case "quitGame":
                        pygame.quit()
                        sys.exit()
            if joystick != -1 and checkInputController(joystick, "quit"):
                if not pressedQuitButtonOnce:
                    pygame.quit()
                    sys.exit()
            else:
                pressedQuitButtonOnce = False
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if checkInputKey(event.key, "quit"):
                        pygame.quit()
                        sys.exit()
            if not action:
                WINDOW.fill(BACKGROUNDCOLOR)
                mainMenu.draw(WINDOW)
            pygame.display.update()
            fpsClock.tick(FPS)
            continue
        if dead:
            dead = False
            player.dead = False
            player.health = player.maxHealth
            quitgame(player, enemiesGroup.sprites(), itemsGroup.sprites(), breakableRocks, area, worldSave)
            inMenu = True
        if joystick != -1 and checkInputController(joystick, "quit"):
            quitgame(player, enemiesGroup.sprites(), itemsGroup.sprites(), breakableRocks, area, worldSave)
            inMenu = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if checkInputKey(event.key, "quit"):
                    quitgame(player, enemiesGroup.sprites(), itemsGroup.sprites(), breakableRocks, area, worldSave)
                    inMenu = True
        if inMenu:
            if whichMusic != "none":
                music[whichMusic].fadeout(500)
            music[menuMusic].play(-1, fade_ms=500)
            pressedQuitButtonOnce = True
            transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="circle", background=WINDOW.copy(), dir=1)
            mainMenu.draw(WINDOW)
            transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="fadeFromBlack", background=WINDOW.copy())
            continue
        
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

        numJoysticksStart = numJoysticks
        numJoysticks = pygame.joystick.get_count()
        if numJoysticks != numJoysticksStart and numJoysticks != 0:
            joystick = pygame.joystick.Joystick(numJoysticks - 1)
            joystick.init()
        elif numJoysticks == 0:
            joystick = -1
        
        dead = player.update(dt, joystick, walls, enemiesGroup, NPCsGroup.sprites(), playerInCombat, itemsGroup, breakableRocks)

        itemsGroup.update(dt)

        NPCsGroup.update(dt, walls, player.talking)
        drops = []
        for grass in cuttableGrass.sprites():
            dropPos, dropType = grass.update(dt, playerAttackHitbox = player.weaponHitboxes[player.activeWeaponHitbox] if player.attacking else -1)
            if dropType != -1:
                drops.append((dropPos, dropType))
        for drop in drops:
            Item(drop[0], drop[1], False, itemsGroup)

        drops = []
        if "hitbox" in player.items[player.equipedItem]:
            for enemy in enemiesGroup.sprites():
                dropPos, dropType = enemy.update(dt, pygame.math.Vector2(player.rect.left, player.rect.top), walls, player.weapons[player.weapon], playerAttackHitbox = player.weaponHitboxes[player.activeWeaponHitbox] if player.attacking else -1, playerSpell = player.items[player.equipedItem] if player.usingItem else -1)
                if dropType != -1:
                    drops.append((dropPos, dropType))
        else:
            for enemy in enemiesGroup.sprites():
                dropPos, dropType = enemy.update(dt, pygame.math.Vector2(player.rect.left, player.rect.top), walls, player.weapons[player.weapon], playerAttackHitbox = player.weaponHitboxes[player.activeWeaponHitbox] if player.attacking else -1, playerSpell = -1)
                if dropType != -1:
                    drops.append((dropPos, dropType))
        for drop in drops:
            Item(drop[0], drop[1], False, itemsGroup)
        playerInCombat = False
        if player.dead:
            if whichMusic != "none":
                if music[whichMusic].get_num_channels() != 0:
                    music[whichMusic].fadeout(200)
            if music["fight"].get_num_channels() != 0:
                music["fight"].fadeout(200)
        else:
            for enemy in enemiesGroup.sprites():
                if enemy.aggro and not enemy.trulyDead:
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
            if not "Overworld" in doorEntered:
                transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="circle", background=WINDOW.copy(), dir=1)
            else:
                transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="fadeToBlack", background=WINDOW.copy())
            # print("area: ", area)
            saveGame(player, enemiesGroup.sprites(), itemsGroup.sprites(), breakableRocks, area, worldSave)
            if "Overworld" in doorEntered:
                mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations, NPCsGroup, itemsGroup, cuttableGrass, breakableRocks = changeMap(overworldMapPath, scaleTo[0], scaleTo[1], mapTileSize)
                player.rect.topleft = doorDestinations[doorEntered]
                enemies, items, breakableRocksload, area, worldSave = loadGame(player, Enemy, Item, "Overworld")
            else:
                mapSprites, mapSpritesFront, enemiesGroup, walls, musicAreas, doorAreas, doorDestinations, NPCsGroup, itemsGroup, cuttableGrass, breakableRocks = changeMap("maps/subAreas/" + doorEntered + ".tmx", scaleTo[0], scaleTo[1], mapTileSize)
                player.rect.topleft = doorDestinations[doorEntered]
                enemies, items, breakableRocksLoad, area, worldSave = loadGame(player, Enemy, Item, doorEntered)
            
            if enemies != -1:
                enemiesGroup = enemies
            if items != -1:
                itemsGroup = items
            if breakableRocksLoad != -1:
                breakableRocks = breakableRocksLoad

            drawWorld(player, mapSprites, mapSpritesFront, NPCsGroup, itemsGroup, enemiesGroup, cuttableGrass)
            if "Overworld" in doorEntered:
                transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="circle", background=WINDOW.copy(), dir=-1)
            else:
                transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="fadeFromBlack", background=WINDOW.copy())
            # transition(WINDOW, fpsClock, BACKGROUNDCOLOR, type="circle", dir=-1, background=WINDOW.copy())
        # mapSprites.update(player.rect.topleft)
        
        WINDOW.fill(BACKGROUNDCOLOR)

        # for wall in walls:
        #     pygame.draw.rect(WINDOW, (100, 100, 100), wall)#pygame.Rect((wall.x - player.rect.x, wall.y - player.rect.y), (wall.width, wall.height)))

        # for k in musicAreas:
        #     for i in musicAreas[k]:
        #         pygame.draw.rect(WINDOW, (100, 100, 100), i)
        # pygame.draw.rect(WINDOW, (100, 200, 200), player.rect)

        drawWorld(player, mapSprites, mapSpritesFront, NPCsGroup, itemsGroup, enemiesGroup, cuttableGrass)

        pygame.display.update()
        fpsClock.tick(FPS)

def drawWorld(player, mapSprites, mapSpritesFront, NPCsGroup, itemsGroup, enemiesGroup, cuttableGrass):
    WINDOW.fill(BACKGROUNDCOLOR)
    mapSprites.draw(WINDOW, player.rect.center, player.zoom)
    cuttableGrass.draw(WINDOW, player.rect.center, player.zoom)
    NPCsGroup.draw(WINDOW, player.rect.center, player.zoom)
    itemsGroup.draw(WINDOW, player.rect.center, player.zoom)
    player.draw(WINDOW)
    enemiesGroup.draw(WINDOW, player.rect.center, player.zoom)
    mapSpritesFront.draw(WINDOW, player.rect.center, player.zoom)
    player.drawHUD(WINDOW)

def quitgame(player, enemies, items, breakableRocks, area, worldSave):
    saveGame(player, enemies, items, breakableRocks, area, worldSave)

if __name__ == "__main__":
    main()