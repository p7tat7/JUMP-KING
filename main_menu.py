import os
import pygame

import global_var
import setting


class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(setting.box_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y


class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, size, positions, no_of_options):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(setting.arrow_path)
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(x, y))
        self.index = 1
        self.positions = positions
        self.options = no_of_options

    # def update(self):
    #     # for event in pygame.event.get():
    #     #     print(event)
    #     #     if event.type == pygame.KEYDOWN:
    #     #         if event.key == pygame.K_DOWN:
    #     #             self.move(1)
    #     #         if event.key == pygame.K_UP:
    #     #             self.move(-1)
    #     key_press = pygame.key.get_pressed()
    #     if key_press[pygame.K_DOWN]:
    #         print('down')
    #         self.move(1)
    #     elif key_press[pygame.K_UP]:
    #         print('up')
    #         self.move(-1)

    def min(self):
        return self.index == 1

    def max(self):
        return self.index == self.options

    def move(self, direction):
        if (direction == 1 and not self.max()) or (direction == -1 and not self.min()):
            self.index += direction
            self.rect.centery = self.positions[self.index - 1]



