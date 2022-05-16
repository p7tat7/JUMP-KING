import pygame
import os
import setting

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, size, jump_h, walk_s):
        pygame.sprite.Sprite.__init__(self)

        # index 0 = last frame, index 1 = current frame
        # The number inside means hold for how many frames
        self.hold_keys = {
            pygame.K_SPACE: [0, 0],
            pygame.K_a: [0, 0],
            pygame.K_d: [0, 0]
        }

        self.idle_images = []
        self.move_images = []
        self.jump_images = []
        self.drop_images = []
        self.move_frame = 0
        for file_index, file in enumerate(os.listdir(setting.character_images_path)):
            ori_path = os.path.join(setting.character_images_path, file)
            if os.path.isfile(ori_path):
                img = pygame.image.load(ori_path).convert()
                img = pygame.transform.scale(img, (size[0], size[1]))
                img.set_colorkey((0, 0, 0))
                self.idle_images.append(img)
            if os.path.isdir(ori_path):
                for image in os.listdir(ori_path):
                    path = os.path.join(ori_path, image)
                    img = pygame.image.load(path).convert()
                    img = pygame.transform.scale(img, (size[0], size[1]))
                    img.set_colorkey((0, 0, 0))

                    if ori_path == setting.character_move_ani:
                        self.move_images.append(img)
                    elif ori_path == setting.character_jump_ani:
                        self.jump_images.append(img)
                    elif ori_path == setting.character_drop_ani:
                        self.drop_images.append(img)

        self.image = self.idle_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = walk_s
        self.jump = jump_h

        self.left = False
        self.right = True
        self.moving = False
        self.in_ground = True
        self.charging = False

        # for jumping
        vel = 5
        self.jump = False
        self.jumpCount = 0
        self.jumpMax = 20
        self.space_pressed = 0

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = setting.frame_rate

    def update(self):
        key_press = pygame.key.get_pressed()

        if not self.in_ground:
            # TODO: jumping, find next position
            pass

        if not key_press[pygame.K_a] and not key_press[pygame.K_d] and self.in_ground and not self.charging:
            self.image = pygame.transform.flip(self.idle_images[0], self.left, False)

        if key_press[pygame.K_SPACE] and self.in_ground:
            self.hold_keys[pygame.K_SPACE][1] += 1
            self.charging = True
            self.image = pygame.transform.flip(self.jump_images[0], self.left, False)

        if key_press[pygame.K_a] and self.in_ground:
            self.hold_keys[pygame.K_a][1] += 1
            self.left = True
            self.right = False
            if not self.charging:
                self.rect.x -= self.speed

                self.moving_animation()

        if key_press[pygame.K_d] and self.in_ground:
            self.hold_keys[pygame.K_d][1] += 1
            self.left = False
            self.right = True
            if not self.charging:
                self.rect.x += self.speed

                self.moving_animation()

        # print(self.hold_keys)  # DEBUG
        for key, hold_key in self.hold_keys.items():
            if hold_key[0] == hold_key[1] and hold_key[0] != 0:
                # just release the key
                if key == pygame.K_SPACE:
                    # start jumping
                    direction = 0
                    if self.hold_keys[pygame.K_a][1] > 0 and self.hold_keys[pygame.K_d][1] > 0:
                        # jump
                        direction = 0
                    elif self.hold_keys[pygame.K_a][1] > 0:
                        # left jump
                        direction = -1
                    elif self.hold_keys[pygame.K_d][1] > 0:
                        # right jump
                        direction = 1

                    # print("jump (direction: " + str(direction) + ", holding time: " + str(hold_key[0]) + ")")  # DEBUG

                    self.charging = False

                    # TODO
                    # self.in_ground = False

                # didn't press anymore, so reset it
                self.hold_keys[key] = [0, 0]
            else:
                # pressing, update it
                hold_key[0] = hold_key[1]

    def moving_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_rate:
            self.move_frame += 1
            frame = self.move_frame % len(self.move_images)
            self.image = pygame.transform.flip(self.move_images[frame], self.left, False)
            self.last_update = now

    # for jumping
    def jumping(self):
        if self.jump:
            self.rect.y -= self.jumpCount
            self.jumpCount = self.jumpMax
            if self.jumpCount > -self.jumpMax:
                self.jumpCount -= 1
            else:
                self.jump = False