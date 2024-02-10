import pygame

mapTileSize = pygame.math.Vector2(16, 16)
size = (64, 64)

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
            rect.x += dt * 500
            if not background is None:
                WINDOW.fill(BACKGROUNDCOLOR)
                WINDOW.blit(background, (0, 0))
            pygame.draw.rect(WINDOW, (0, 0, 0), rect)
            pygame.display.update()