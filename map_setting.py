import setting
import pygame
import os
# pip install Pillow
from PIL import Image
import pprint

class Map:
    def __init__(self, map_number):
        self.map_display = pygame.image.load(os.path.join(setting.stage_images_path, f'{map_number}.png'))
        self.map_layout = Image.open(os.path.join(setting.stage_images_path, f'{map_number}.png'))
        self.map_sprite = Image.open(os.path.join(setting.stage_images_path, f'{map_number}s.png'))

        self.map_data = []
        pix_ms = self.map_sprite.load()
        for x in range(setting.screen_size[1]):
            row_data = []
            for y in range(setting.screen_size[0]):
                #print(pix_ms[x, y])
                if (pix_ms[y, x] == (251, 3, 3, 255)):
                    row_data.append("X")
                else:
                    row_data.append(" ")
            self.map_data.append(row_data)

        # print(self.map_data)
        # self.debugMap()

    def get_map_data(self):
        return self.map_data

    def debugMap(self):
        for i in range(len(self.map_data)):
            if i % 50 != 0:
                continue
            for j in range(len(self.map_data[i])):
                if j % 20 != 0 and j != len(self.map_data[i])-1:
                    continue
                print(self.map_data[i][j], end='')
            print()