import os
import pygame

import setting

stage_map = None
stage_no = 1
GAME_TITLE = 'JUMP KING'

background = pygame.image.load(os.path.join(setting.background_path, f"bg{stage_no}.png"))
background = pygame.transform.scale(background, setting.screen_size)
backdrop = pygame.image.load(os.path.join(setting.stage_images_path, f"{stage_no}.png"))
foreground = pygame.image.load(os.path.join(setting.foreground_path, f"fg{stage_no}.png"))
foreground = pygame.transform.scale(foreground, setting.screen_size)

# font
pygame.init()
font1 = pygame.font.Font(setting.SourceHanSansCN, 25)
font2 = pygame.font.Font(setting.SourceHanSansCN_normal, 2)

# Sound Setting
music_on = True
sfx_on = True
environment_on = True