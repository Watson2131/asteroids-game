import math
import pygame
import color
import consts
from CollidableObject import CollidableObject
from RenderObject import RenderObject


class Player(CollidableObject, RenderObject):
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = consts.screen_width / 2 - self.width / 2
        self.y = consts.screen_height / 2 - self.height / 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.angle = -90
        self.speed = consts.player_speed
        self.lives = consts.starting_lives
        self.invulnerable = 0

    def move_left(self):
        self.angle -= consts.player_turn_speed

    def move_right(self):
        self.angle += consts.player_turn_speed

    def move_forward(self):
        angle_rad = math.radians(self.angle)
        self.x += math.cos(angle_rad) * self.speed
        self.y += math.sin(angle_rad) * self.speed
        self._wrap_position()

    def _wrap_position(self):
        if self.x < -self.width:
            self.x = consts.screen_width
        elif self.x > consts.screen_width:
            self.x = -self.width
        if self.y < -self.height:
            self.y = consts.screen_height
        elif self.y > consts.screen_height:
            self.y = -self.height
        self.rect.topleft = (int(self.x), int(self.y))

    def update(self):
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def get_points(self):
        angle_rad = math.radians(self.angle)
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2
        points = []
        for forward, side in ((19, 0), (-12, 11), (-7, 0), (-12, -11)):
            px = center_x + math.cos(angle_rad) * forward - math.sin(angle_rad) * side
            py = center_y + math.sin(angle_rad) * forward + math.cos(angle_rad) * side
            points.append((int(px), int(py)))
        return points

    def draw(self, surface):
        if self.invulnerable > 0 and self.invulnerable % 8 < 4:
            return
        pygame.draw.polygon(surface, color.green, self.get_points(), 2)
