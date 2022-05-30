import os
import pygame

import setting
import saving
import global_var
import main_menu


class MenuBox(pygame.sprite.Sprite):
    def __init__(self, x, y, size, options):
        pygame.sprite.Sprite.__init__(self)
        self.box = main_menu.Box(x, y, size)
        self.arrow = main_menu.Arrow(0, 0, (30, 30), [], len(options))

    def update(self):
        pass

    def display(self):

