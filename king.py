import pygame
import os
import setting
import global_var
import map_setting
import math

# y = -1/w (x)^2 + c
# y = -1/jump_variable (x)^2 + jump_height
class Parabola():
    def __init__(self, height, direction, ori_x, ori_y):

        self.jump_height = height
        # x-intercept
        x_intercept = self.get_x_intercept()
        # left: -(0)    right: +(1)

        if direction == -1:
            self.starting_point_x = x_intercept[1]
        elif direction == 1:
            self.starting_point_x = x_intercept[0]
        elif direction == 0:
            self.starting_point_x = x_intercept[0]
        self.current_x = self.starting_point_x
        self.starting_point_y = 0
        self.ori_x = ori_x
        self.ori_y = ori_y

        self.direction = direction

        print(f' y = -1/{setting.jumping_variable}(x)^2 + {height}')
        # print("Parabola():", self.a, self.translate_x, self.current_x, self.direction, self.step)

    def get_direction(self):
        return self.direction

    # find next position
    def next_position(self):
        temp_direction = self.direction
        if self.direction == 0:
            temp_direction = 1

        dist = temp_direction * setting.jumping_variable // (setting.maximum_secs_for_jump / 2 * setting.frame_rate)
        self.current_x += dist
        add_x = self.current_x - self.starting_point_x
        add_y = self.get_current_y() - self.starting_point_y
        print(f'{self.current_x } {add_y=}')

        if self.direction != 0:
            return (self.ori_x + add_x, self.ori_y - add_y, self.direction)
        else:
            return (self.ori_x, self.ori_y - add_y, self.direction)

    def return_back(self, dist):
        temp_direction = self.direction
        if self.direction == 0:
            temp_direction = 1
        self.current_x -= dist * temp_direction

    def change_direction(self, x, y):
        print("\n\n\n")
        print('Change direction.')
        print(f'Before: {self.current_x=} {self.direction=} {self.starting_point_x=}')

        # situation1 = self.direction == 1 and self.current_x < 0
        # situation2 = self.direction == -1 and self.current_x > 0

        # if situation1 or situation2:
        #     self.ori_y = y
        #     self.starting_point_y = y

        self.current_x *= -1
        self.direction *= -1

        self.ori_x = x
        # self.ori_y = y
        self.starting_point_x = self.current_x
        print(f'After: {self.current_x=} {self.direction=} {self.starting_point_x=}')

    def get_current_y(self):
        return -1/setting.jumping_variable * (self.current_x)**2 + self.jump_height

    def get_x_intercept(self):
        intercept = math.sqrt(self.jump_height * setting.jumping_variable)
        return (-intercept, intercept)

    def dropping(self):
        temp_direction = self.direction
        if self.direction == 0:
            temp_direction = 1

        return (self.current_x * temp_direction > 0)

# class Parabola():
#     def __init__(self, a, translate_x, current_x, direction, step):
#         self.a = a
#         self.translate_x = translate_x
#         self.current_x = current_x
#         self.direction = direction
#         self.step = step
#
#         if self.direction < 0:
#             self.direction *= -1
#             self.change_direction()
#
#         #print("Parabola():", self.a, self.translate_x, self.current_x, self.direction, self.step)
#
#     def get_direction(self):
#         return self.direction
#
#     # find next position
#     def next(self):
#         # return change of x and y in tuple.
#         x = self.current_x
#         temp = self.direction * self.step if self.direction != 0 else self.step
#         x += temp
#         y = self.get_y(self.current_x) - self.get_y(x)
#         # x -= self.current_x
#         self.current_x += self.step
#         if self.direction == 0:
#             temp = 0
#         #print("next():", temp//self.step, y//self.step)
#         return temp//self.step, y//self.step
#
#     def change_direction(self):
#         self.direction *= -1
#         self.step *= -1
#         self.translate_x = self.current_x * -2 - self.translate_x
#
#     def get_y(self, x):
#         return self.a * (x+self.translate_x)**2



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
        self.jump_h = jump_h

        self.left = False
        self.right = True
        self.moving = False
        self.in_ground = True
        self.charging = False

        # for jumping
        # vel = 5
        # self.jump = False
        self.jumpCount = 0
        # self.jumpMax = 20
        # self.space_pressed = 0
        self.parabola = None

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = setting.frame_rate




    def init_location(self):
        while self.hit_ground():
            self.rect.y -= 1
        while not self.hit_ground():
            self.rect.y += 1


    def update(self):
        # print(f'Update {self.rect.x=} {self.rect.y=}')
        key_press = pygame.key.get_pressed()
        #print(self.rect.center)

        if not self.in_ground and self.parabola != None:
            # jumping

            self.jumpCount += 1

            # check if hitting ground
            print(f'{self.rect.right=}')
            if self.jumpCount > 1 and self.hit_ground():
                self.in_ground = self.hit_ground()
                self.parabola = None
                self.jumpCount = 0
                while 1:
                    self.rect.y -= 1
                    if not self.hit_ground():
                        self.rect.y += 1
                        break

            if self.jumpCount > 1 and self.hit_ceiling():
                print('\n\n\n\nhit ceiling\n\n\n\n')
                # self.parabola.current_x *= -1

            # if self.parabola != None:
            #     # check if hitting wall
            #     if self.hit_wall() and self.parabola.get_direction() != 0:
            #         # change direction
            #         self.parabola.change_direction()
            #         self.right = not self.right
            #         self.left = not self.left

            if self.parabola != None:

                if self.parabola.dropping():
                    self.image = pygame.transform.flip(self.jump_images[2], self.left, False)
                else:
                    self.image = pygame.transform.flip(self.jump_images[1], self.left, False)
                # check if hitting wall
                # if self.hit_wall() and self.parabola.get_direction() != 0:
                #     # change direction
                #     self.parabola.change_direction(self.rect.x, self.rect.y)
                #     self.image = pygame.transform.flip(self.jump_images[3], self.right, False)
                #     self.right = not self.right
                #     self.left = not self.left

                # find next position
                x, y, direction = self.parabola.next_position()
                print(f'{x=} {y=}')

                if round(y) > self.rect.y:
                    add = 1
                elif round(y) < self.rect.y:
                    add = -1
                else:
                    add = 0
                while True:


                    rangeX = range(self.rect.left + direction, self.rect.right + direction)

                    rangeY = range(self.rect.top + add, self.rect.bottom + add)

                    if self.rect.x == round(x) and self.rect.y == round(y):
                        break

                    if direction == 1:
                        right = 1
                        left = 0
                    elif direction == -1:
                        left = 1
                        right = 0

                    if add == 1:
                        top = 1
                        bottom = 0
                    elif add == -1:
                        top = 0
                        bottom = 1

                    hit = self.detect_next(rangeX, rangeY, top, bottom, left, right)

                    # if self.detect_next(rangeX, rangeY):
                    #     self.parabola.current_x *= -1
                    # elif self.detect_next(rangeX, rangeY) or self.detect_next(rangeX, rangeY):
                    #     self.parabola.change_direction(self.rect.x, self.rect.y)
                    #     self.image = pygame.transform.flip(self.jump_images[3], self.right, False)
                    #     self.right = not self.right
                    #     self.left = not self.left

                    # TODO add hit cases


                    self.rect.x += direction
                    self.rect.y += add


                # self.rect.x = x
                # self.rect.y = y
                if self.hit_wall():
                    if self.right:
                        temp = -1
                    elif self.left:
                        temp = 1
                    if self.hit_ground():
                        while 1:
                            self.rect.y -= 1
                            if not self.hit_ground():
                                self.rect.y += 1
                                break
                    while 1:
                        self.rect.x += temp * 1

                        if not self.hit_wall():
                            self.rect.x += temp * -1
                            break
                    # self.rect.x = self.temp_wall_x + (temp * setting.character_size[0]) + temp * 5
                    print(f'changed: {self.rect.x=} {self.rect.y=}')
                    if not self.hit_ground():
                        self.parabola.change_direction(self.rect.x, self.rect.y)
                        self.image = pygame.transform.flip(self.jump_images[3], self.right, False)
                        self.right = not self.right
                        self.left = not self.left
                print(f'{self.rect.x=} {self.rect.y=}')
                # if y < 0:
                #     self.image = pygame.transform.flip(self.jump_images[1], self.left, False)
                # else:
                #     self.image = pygame.transform.flip(self.jump_images[2], self.left, False)
                # self.rect.x += x
                # self.rect.y += y




        elif not self.hit_ground() and self.parabola == None:
            # TODO: droping without jumping
            # if self.left:
            #     self.parabola = Parabola(-1, 0, 0, -1, 0.1)
            # else:
            #     self.parabola = Parabola(-1, 0, 0, 1, 0.1)
            self.in_ground = False

        # debug
        if key_press[pygame.K_UP]:
            self.rect.y -= 30

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



                    self.charging = False
                    self.in_ground = False

                    # TODO: parabola coefficients and starting x position
                    #       according to the holding time
                    # self.parabola = Parabola(-1, 0, -5, direction, 0.1)
                    height = hold_key[0] * self.jump_h // setting.frame_rate
                    if height > self.jump_h:
                        height = self.jump_h
                    print("\n\n\n")
                    print(f"jump ({direction=} {height=})")  # DEBUG
                    self.parabola = Parabola(height, direction, self.rect.x, self.rect.y)

                # didn't press anymore, so reset it
                self.hold_keys[key] = [0, 0]
            else:
                # pressing, update it
                hold_key[0] = hold_key[1]

        # Change Scene
        if self.rect.bottom <= 0:
            self.rect.bottom = setting.screen_size[1] - 1
            global_var.stage_no += 1
            self.parabola.starting_point_y = self.parabola.get_current_y()
            self.parabola.ori_y = self.rect.y
            print(f'Changed map: {global_var.stage_no} {self.rect.bottom=}')
            global_var.stage_map = map_setting.Map(global_var.stage_no)

        if self.rect.bottom > setting.screen_size[1]:
            self.rect.bottom = 1
            global_var.stage_no -= 1
            self.parabola.starting_point_y = self.parabola.get_current_y()
            self.parabola.ori_y = self.rect.y
            print(f'Changed map: {global_var.stage_no}')
            global_var.stage_map = map_setting.Map(global_var.stage_no)





    def moving_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_rate:
            self.move_frame += 1
            frame = self.move_frame % len(self.move_images)
            self.image = pygame.transform.flip(self.move_images[frame], self.left, False)
            self.last_update = now

    # for jumping
    # def jumping(self):
    #     if self.jump:
    #         self.rect.y -= self.jumpCount
    #         self.jumpCount = self.jumpMax
    #         if self.jumpCount > -self.jumpMax:
    #             self.jumpCount -= 1
    #         else:
    #             self.jump = False

    def hit_ground(self):
        y_coor = self.rect.bottom - 1
        map_data = global_var.stage_map.get_map_data()

        for x_coor in range(self.rect.left + 5, self.rect.right - 5):

            if map_data[y_coor][x_coor] == 'X':
                self.temp_floor_y = y_coor
                return True
        return False

    # Check for hitting wall
    def hit_wall(self):
        if self.right:
            x_coor = self.rect.right
        elif self.left:
            x_coor = self.rect.left
        map_data = global_var.stage_map.get_map_data()
        print(f'hit wall {self.rect.x=} {self.rect.y=}')
        for y_coor in range(self.rect.top, self.rect.bottom-1):
            if y_coor >= setting.screen_size[1] or y_coor < 0:
                continue
            if map_data[y_coor][x_coor] == 'X':
                self.temp_wall_x = x_coor
                return True
        return False

    def hit_ceiling(self):
        y_coor = self.rect.top
        if y_coor < 0 or y_coor > setting.screen_size[1]:
            return False
        map_data = global_var.stage_map.get_map_data()
        for x_coor in range(self.rect.left, self.rect.right):
            if map_data[y_coor][x_coor] == 'X':
                return True
        return False

    def detect_next(self, xrange, yrange, xtop, xbottom, yleft, yright):
        map_data = global_var.stage_map.get_map_data()
        left_hit = False
        right_hit = False
        top_hit = False
        bottom_hit = False
        max_x = setting.screen_size[0]
        min_x = 0
        max_y = setting.screen_size[1]
        min_y = 0

        if xtop == 1:
            y_coor = yrange[0]
            for x_coor in xrange:
                if x_coor > max_x or x_coor < min_x:
                    top_hit = True
                    break
                if map_data[y_coor][x_coor] == 'X':
                    top_hit = True
                    break

        elif xbottom == 1:
            y_coor = yrange[len(yrange) - 1]
            for x_coor in xrange:
                if x_coor > max_x or x_coor < min_x:
                    bottom_hit = True
                    break
                if map_data[y_coor][x_coor] == 'X':
                    bottom_hit = True
                    break

        if yleft == 1:
            x_coor = xrange[0]
            for y_coor in yrange:
                if y_coor > max_y or y_coor < min_y:
                    left_hit = True
                    break
                if map_data[y_coor][x_coor] == 'X':
                    bottom_hit = True
                    break
        elif yright == 1:
            x_coor = xrange[len(xrange) - 1]
            for y_coor in yrange:
                if y_coor > max_y or y_coor < min_y:
                    right_hit = True
                    break
                if map_data[y_coor][x_coor] == 'X':
                    right_hit = True
                    break

        result = (top_hit, bottom_hit, left_hit, right_hit)
        return result
