from pygame.locals import *

inputs = {
    "quit": [K_ESCAPE],
    "moveLeft": [K_LEFT],
    "moveRight": [K_RIGHT],
    "moveUp": [K_UP],
    "moveDown": [K_DOWN],
    "attack": [K_SPACE],
    "changeWeapon": [K_x],
    "talk": [K_RETURN]
}

def checkInput(keysPressed, action):
    for key in inputs[action]:
        if keysPressed[key]:
            return True
    return False

def checkInputKey(p_key, action):
    for key in inputs[action]:
        if key == p_key:
            return True
    return False