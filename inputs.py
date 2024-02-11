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
inputsController = {
    "quit": [9],
    "moveHorizontal": [0],
    "moveVertical": [1],
    "attack": [1],
    "changeWeapon": [6],
    "talk": [0]
}

deadZone = 0.1

def checkInputController(joystick, action):
    if "move" in action:
        for key in inputsController[action]:
            if abs(joystick.get_axis(key)) > deadZone:
                return joystick.get_axis(key)
        return 0
    else:
        for key in inputsController[action]:
            if joystick.get_button(key):
                return True
        return False

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