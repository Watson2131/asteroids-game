import math
import pygame
import color
import consts
from CollidableObject import CollidableObject
from RenderObject import RenderObject


class Bullet(CollidableObject, RenderObject):
    def __init__(self, x, y, angle):
        self.width = 6
        self.height = 6
        self.x = x
        self.y = y
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        angle_rad = math.radians(angle)
        self.vector_x = math.cos(angle_rad) * consts.bullet_speed
        self.vector_y = math.sin(angle_rad) * consts.bullet_speed
        self.life = 55

    def move(self):
        self.x += self.vector_x
        self.y += self.vector_y
        self.life -= 1
        if self.x < 0:
            self.x = consts.screen_width
        elif self.x > consts.screen_width:
            self.x = 0
        if self.y < 0:
            self.y = consts.screen_height
        elif self.y > consts.screen_height:
            self.y = 0
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, color.yellow,
                           (int(self.x + self.width / 2), int(self.y + self.height / 2)), 3)
