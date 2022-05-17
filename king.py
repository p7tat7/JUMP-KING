import pygame
import os
import setting
import global_var
import map_setting

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, size, jump_h, walk_s):
        pygame.sprite.Sprite.__init__(self)

        # index 0 = last frame, index 1 = current frame
        # The number inside means holded for how many frames
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
        #print(self.rect.center)

        if not self.in_ground:
            # TODO: jumping, find next position
            pass

        # debug
        if key_press[pygame.K_UP]:
            self.rect.y -= 5

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

            # Changed with function <hit_wall>, since it needs to check for all y coordinates of the character

            # collide_wall = global_var.stage_map.get_map_data()[self.rect.center[1] - (setting.character_size[1] // 2) - 1][self.rect.center[0] - (setting.character_size[0] // 2) - 1] != ' '
            collide_wall = self.hit_wall()
            if not self.charging and not collide_wall:
                self.rect.x -= self.speed

                self.moving_animation()
            elif not self.charging and collide_wall:
                self.image = pygame.transform.flip(self.idle_images[0], self.left, False)

        if key_press[pygame.K_d] and self.in_ground:
            self.hold_keys[pygame.K_d][1] += 1
            self.left = False
            self.right = True

            # Changed with function <hit_wall>, since it needs to check for all y coordinates of the character

            # collide_wall = global_var.stage_map.get_map_data()[self.rect.center[1] - (setting.character_size[1] // 2) - 1][self.rect.center[0] + (setting.character_size[0] // 2) + 1] != ' '
            collide_wall = self.hit_wall()
            if not self.charging and not collide_wall:
                self.rect.x += self.speed

                self.moving_animation()
            elif not self.charging and collide_wall:
                self.image = pygame.transform.flip(self.idle_images[0], self.left, False)

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

                    print("jump (direction: " + str(direction) + ", holding time: " + str(hold_key[0]) + ")")  # DEBUG

                    self.charging = False

                    # TODO
                    # self.in_ground = False

                # didn't press anymore, so reset it
                self.hold_keys[key] = [0, 0]
            else:
                # pressing, update it
                hold_key[0] = hold_key[1]

        # Change Scene
        if self.rect.bottom <= 0:
            self.rect.bottom = setting.screen_size[1]
            global_var.stage_no += 1
            global_var.stage_map = map_setting.Map(global_var.stage_no)


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

    # Check for hitting wall
    def hit_wall(self):
        if self.right:
            y_coor = self.rect.right
        elif self.left:
            y_coor = self.rect.left

        for x_coor in range(self.rect.top, self.rect.bottom + 1):

            map_data = global_var.stage_map.get_map_data()
            if map_data[x_coor][y_coor] == 'X':
                return True
        return False
