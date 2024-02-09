import pygame

mapTileSize = pygame.math.Vector2(16, 16)

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