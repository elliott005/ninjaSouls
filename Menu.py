import pygame
from pytmx.util_pygame import load_pygame
from globals import *
from inputs import *

mainMenuMap = load_pygame("maps/MenuBackground.tmx")

class MainMenu:
    def __init__(self, windowSize):
        self.mainMenuBackground = pygame.Surface(windowSize)
        for layer in mainMenuMap.visible_layers:
            if hasattr(layer, "data"):
                for x, y, surf in layer.tiles():
                    self.mainMenuBackground.blit(pygame.transform.scale(surf, size), (x * size[0], y * size[1]))
        self.buttonImage = pygame.image.load("assets/NinjaAdventure/HUD/Dialog/DialogueBoxSimple.png")
        self.buttonImageHovered = pygame.image.load("assets/NinjaAdventure/HUD/Dialog/DialogBox.png")

        self.buttons = {
            "startGame": {"pos": (0, 0), "size": (1000, 200), "neighborDown": "quitGame", "text": "Start Game!"},
            "quitGame": {"pos": (0, 400), "size": (1000, 200), "neighborUp": "startGame", "text": "Quit Game :("}
        }
        self.moveOnce = False
        self.hovered = "startGame"

        for button in self.buttons:
            self.buttons[button]["sprite"] = pygame.transform.scale(self.buttonImage, self.buttons[button]["size"])
            self.buttons[button]["spriteHovered"] = pygame.transform.scale(self.buttonImageHovered, self.buttons[button]["size"])
    
    def update(self, joystick):
        keysPressed = pygame.key.get_pressed()
        if ((checkInput(keysPressed, "moveUp") and joystick == -1) or (joystick != -1 and checkInputController(joystick, "moveVertical") < 0.0)):
            if not self.moveOnce:
                self.moveOnce = True
                if "neighborUp" in self.buttons[self.hovered]:
                    self.hovered = self.buttons[self.hovered]["neighborUp"]
        elif ((checkInput(keysPressed, "moveDown") and joystick == -1) or (joystick != -1 and checkInputController(joystick, "moveVertical") > 0.0)):
            if not self.moveOnce:
                self.moveOnce = True
                if "neighborDown" in self.buttons[self.hovered]:
                    self.hovered = self.buttons[self.hovered]["neighborDown"]
        else:
            self.moveOnce = False
        if ((checkInput(keysPressed, "talk") and joystick == -1) or (joystick != -1 and checkInputController(joystick, "talk"))):
            return self.hovered
        return False
    
    def draw(self, WINDOW):
        WINDOW.blit(self.mainMenuBackground, (0, 0))
        for button in self.buttons:
            if self.hovered == button:
                WINDOW.blit(self.buttons[button]["spriteHovered"], self.buttons[button]["pos"])
                WINDOW.blit(fontMenu.render(self.buttons[button]["text"], False, (0, 100, 100)), (self.buttons[button]["pos"][0] + 20, self.buttons[button]["pos"][1]))
            else:
                WINDOW.blit(self.buttons[button]["sprite"], self.buttons[button]["pos"])
                WINDOW.blit(fontMenu.render(self.buttons[button]["text"], False, (0, 0, 0)), (self.buttons[button]["pos"][0] + 20, self.buttons[button]["pos"][1]))