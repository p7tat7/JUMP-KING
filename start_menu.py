import os
import pygame
from pygame import mixer

import setting

class Logo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(setting.logo_path).convert()
        self.image =  pygame.transform.scale(self.image, (700, 200))

        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()

        # init coordinates
        self.rect.center = (setting.screen_size[0] // 2, setting.screen_size[1] // 2)

        self.goal_y = setting.screen_size[1] // 4
        self.meet_goal_y = False
        self.last_update = pygame.time.get_ticks()
        self.shake_count = 0
        self.shake_frame = 5
        self.shake_frame_delay = self.shake_frame // setting.frame_rate
        self.alpha = 1
        self.shake_time = 3
        self.shaked = 0

        # Speed
        self.shake_speed = 10
        self.move_speed = 5

        # Finishing
        self.completed = False

        # mixer.init()
        self.title_hit_sound = mixer.Sound(setting.title_hit_path)

    def update(self):
        if self.alpha <= 255:
            self.image.set_alpha(self.alpha)
            self.alpha += 5
        if not self.meet_goal_y:
            self.logo_animation()
        elif not self.completed:
            self.logo_shake()

            if self.shaked == self.shake_time:
                self.completed = True

    def logo_animation(self):
        if self.rect.centery >= self.goal_y:
            self.rect.centery -= self.move_speed
        elif self.rect.centery <= self.goal_y:
            self.meet_goal_y = True

    def logo_shake(self):
        if self.shake_count <= self.shake_frame // 2:
            self.rect.y -= self.shake_speed
        elif self.shake_frame // 2 <= self.shake_count <= self.shake_frame:
            self.rect.y += self.shake_speed
        self.shake_count += 1

        if self.shake_count == self.shake_frame:
            self.shake_count = 0
            self.shaked += 1
            if self.shaked == 1:
                mixer.Sound.play(self.title_hit_sound)

class PressStart(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.pic = pygame.image.load(setting.press_space_path)
        self.blank = pygame.Surface((0, 0))
        self.image = self.pic

        self.rect = self.image.get_rect()
        self.rect.center = (setting.screen_size[0] // 2, 600)
        self.flash_rate = 0.5
        self.show = True
        self.frame_count = 0

        self.clicked = False
        self.hold_frame_count = 0
        self.hold_frame = 30

        self.complete = False

        self.click_sound = mixer.Sound(setting.press_start_path)
        self.click_sound.set_volume(0.3)

    def update(self):
        if self.frame_count > setting.FPS:
            self.frame_count = 0
        self.flash()
        self.frame_count += 1
        if self.clicked:
            self.hold_frame_count += 1
            if self.hold_frame_count > self.hold_frame:
                self.complete = True
            self.click_effect()
        else:
            self.flash()

    def flash(self):
        if self.frame_count == 0:
            self.show = not self.show

    def click_effect(self):
        if self.frame_count % 4 == 0:
            self.show = not self.show

