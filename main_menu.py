import os
import pygame

import global_var
import setting


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(setting.box_path)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.image = pygame.transform.scale(self.image, size)

