import pygame
import consts


class CollidableObject:
    x = 0
    y = 0
    width = 0
    height = 0
    rect = pygame.Rect(x, y, width, height)

    def collide(self, collide_object):
        return self.rect.colliderect(collide_object.rect)

    def collide_with_right_border(self):
        return self.rect.right > consts.screen_width

    def collide_with_left_border(self):
        return self.rect.left < 0

    def collide_with_bottom_border(self):
        return self.rect.bottom > consts.screen_height

    def collide_with_top_border(self):
        return self.rect.top < 0

    def collide_with_screen_border(self):
        return (self.collide_with_right_border()
                or self.collide_with_left_border()
                or self.collide_with_bottom_border()
                or self.collide_with_top_border())
