import os
import pygame

import setting
import saving
import global_var
import main_menu


class MenuBox:
    def __init__(self, x, y, size, options):
        # pygame.sprite.Sprite.__init__(self)
        self.box = main_menu.Box(x, y, size)
        self.box_group = pygame.sprite.Group()
        self.box_group.add(self.box)

        self.options = options
        self.positions = [self.box.rect.y + size[1] / len(options) / 2 + size[1] / len(options) * index for index in range(len(options))]
        self.arrow = main_menu.Arrow(self.box.rect.x + 50, self.positions[0], (30, 30), self.positions, len(options))
        self.box_group.add(self.arrow)
        # print(f'{self.positions=}')

    def update(self, screen):
        self.display(screen)


    def display(self, screen):
        self.box_group.draw(screen)
        font = global_var.font1
        for option_index, option in enumerate(self.options):
            text = font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(0, self.positions[option_index]))
            text_rect.x = self.box.rect.x + 50
            if self.arrow.index - 1 == option_index:
                text_rect.x += self.arrow.image.get_size()[0]

            screen.blit(text, text_rect)
