import math
import random
import pygame
import color
import consts
from CollidableObject import CollidableObject
from RenderObject import RenderObject


class Asteroid(CollidableObject, RenderObject):
    def __init__(self, size=3, x=None, y=None):
        self.size = size
        self.width = 48 if size == 3 else 29 if size == 2 else 16
        self.height = self.width
        if x is None:
            side = random.randint(0, 3)
            if side == 0:
                x, y = random.randint(0, consts.screen_width), 0
            elif side == 1:
                x, y = consts.screen_width, random.randint(0, consts.screen_height)
            elif side == 2:
                x, y = random.randint(0, consts.screen_width), consts.screen_height
            else:
                x, y = 0, random.randint(0, consts.screen_height)
        self.x = x
        self.y = y
        self.rect = pygame.Rect(int(x), int(y), self.width, self.height)
        self.speed_x = random.choice([-1, 1]) * random.uniform(
            consts.asteroid_min_speed, consts.asteroid_max_speed)
        self.speed_y = random.choice([-1, 1]) * random.uniform(
            consts.asteroid_min_speed, consts.asteroid_max_speed)
        self.angle = random.randint(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        self.points = []
        for i in range(10):
            point_angle = math.pi * 2 * i / 10
            radius = self.width * random.uniform(0.36, 0.5)
            self.points.append((math.cos(point_angle) * radius,
                                math.sin(point_angle) * radius))

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.angle += self.rotation_speed
        if self.x < -self.width:
            self.x = consts.screen_width
        elif self.x > consts.screen_width:
            self.x = -self.width
        if self.y < -self.height:
            self.y = consts.screen_height
        elif self.y > consts.screen_height:
            self.y = -self.height
        self.rect.topleft = (int(self.x), int(self.y))

    def split(self):
        if self.size == 1:
            return []
        return [
            Asteroid(self.size - 1, self.x, self.y),
            Asteroid(self.size - 1, self.x + 5, self.y + 5)
        ]

    def draw(self, surface):
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        angle_rad = math.radians(self.angle)
        rotated_points = []
        for px, py in self.points:
            rx = px * math.cos(angle_rad) - py * math.sin(angle_rad)
            ry = px * math.sin(angle_rad) + py * math.cos(angle_rad)
            rotated_points.append((int(center_x + rx), int(center_y + ry)))
        pygame.draw.polygon(surface, color.dark_gray, rotated_points)
        pygame.draw.polygon(surface, color.gray, rotated_points, 2)
