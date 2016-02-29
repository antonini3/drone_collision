import sys, pygame, time, random
from constants import *

class DroneSprite(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(DroneSprite, self).__init__()
        self.image = pygame.image.load('../img/drone.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.dy, self.dx = 0, 0

    def set_movement(self, dx, dy):
        self.dx, self.dy = dx, dy

    def update(self):
        if self.rect.bottom <= SCREEN_HEIGHT and self.rect.top >= 0:
            self.rect.y += self.dy
        if self.rect.right <= SCREEN_WIDTH and self.rect.left >= 0:
            self.rect.x += self.dx


class TargetSprite(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(TargetSprite, self).__init__()
        self.image = pygame.image.load('../img/target.png')
        self.x, self.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


