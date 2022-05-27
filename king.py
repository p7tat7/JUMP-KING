import pygame
import os
import setting
import global_var
import map_setting
import math

# y = -(direction * x)^dropping_variable
class Exponential():
    def __init__(self, direction, ori_x, ori_y):
        self.direction = direction
        print(f'{ori_x=} {ori_y=}')
        self.ori_x = ori_x
        self.ori_y = ori_y
        self.current_x = 0
        self.starting_point_x = 0
        self.starting_point_y = 0

        print("\n\n\n")
        print(f' y = -({self.direction} * x)^2')

    def next_position(self):

        dist = self.direction * setting.dropping_px_per_frame
        self.current_x += dist

        add_x = self.current_x - self.starting_point_x
        add_y = self.get_current_y() - self.starting_point_y
        print(f'{add_x=} {add_y=}')
        print(f'{self.ori_x=} {self.ori_y=}')
        return self.ori_x + add_x, self.ori_y - add_y, self.direction

    def change_direction(self, x):
        self.direction *= -1
        self.current_x *= -1
        self.starting_point_x = self.current_x
        self.ori_x = x

    def get_current_y(self):
        return -(self.direction * self.current_x) ** setting.dropping_variable


# y = -1/w (x)^2 + c
# y = -1/jump_variable (x)^2 + jump_height
class Parabola():
    def __init__(self, height, direction, ori_x, ori_y):
        self.changed_direction = False
        self.jump_height = height
        # x-intercept
        x_intercept = self.get_x_intercept()

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

    def get_direction(self):
        return self.direction

    # find next position
    def next_position(self):
        temp_direction = self.direction
        if self.direction == 0:
            temp_direction = 1

        dist = temp_direction * setting.jumping_px_per_frame
        self.current_x += dist
        add_x = self.current_x - self.starting_point_x
        add_y = self.get_current_y() - self.starting_point_y

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
        self.changed_direction = True
        self.current_x *= -1
        self.direction *= -1
        self.ori_x = x
        self.starting_point_x = self.current_x


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
        self.jumped = False
        self.jumpCount = 0
        self.parabola = None

        self.exponential = None
        self.drop_height = 0
        self.drop_freeze = False
        self.drop_freeze_frame = 0

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = setting.frame_rate

        # Sound effect
        self.jump_sound = pygame.mixer.Sound(os.path.join(setting.character_sound_path, setting.jump_sound))
        self.land_sound = pygame.mixer.Sound(os.path.join(setting.character_sound_path, setting.land_sound))
        self.hit_wall_sound = pygame.mixer.Sound(os.path.join(setting.character_sound_path, setting.hit_wall_sound))
        self.drop_sound = pygame.mixer.Sound(os.path.join(setting.character_sound_path, setting.drop_sound))



    def init_location(self):
        while self.hit_ground():
            self.rect.y -= 1
        while not self.hit_ground():
            self.rect.y += 1


    def update(self):

        key_press = pygame.key.get_pressed()

        if self.drop_freeze:
            self.image = pygame.transform.flip(self.drop_images[0], self.right, False)
            self.drop_freeze_frame += 1
            print(f'{self.drop_freeze_frame}')
            if self.drop_freeze_frame >= setting.drop_png_frame:
                self.drop_freeze = False
                self.drop_freeze_frame = 0
            return

        if not self.in_ground and self.parabola != None:
            # jumping

            self.jumpCount += 1

            if self.parabola != None:

                if self.parabola.changed_direction:
                    self.image = pygame.transform.flip(self.jump_images[3], self.right, False)
                else:
                    if self.parabola.dropping():
                        self.image = pygame.transform.flip(self.jump_images[2], self.left, False)
                    else:
                        self.image = pygame.transform.flip(self.jump_images[1], self.left, False)

                # find next position
                x, y, direction = self.parabola.next_position()
                save_y = self.rect.y
                self.move_position(x, y, direction)
                if self.rect.y > save_y:
                    self.drop_height += self.rect.y - save_y

        elif not self.on_ground() and self.parabola == None and not self.dropping:
            # TODO: droping without jumping
            if self.right:
                current_direction = 1
            elif self.left:
                current_direction = -1
            self.exponential = Exponential(current_direction, self.rect.x, self.rect.y)
            self.dropping = True

        if self.exponential != None and self.dropping:
            self.image = pygame.transform.flip(self.jump_images[2], self.left, False)
            x, y, direction = self.exponential.next_position()
            # print(f'{x=} {y=} {direction=}')
            save_y = self.rect.y
            self.move_position(x, y, direction)
            if self.rect.y > save_y:
                self.drop_height += self.rect.y - save_y


        # debug
        if key_press[pygame.K_UP]:
            self.rect.y -= 30

        if not key_press[pygame.K_a] and not key_press[pygame.K_d] and self.in_ground and not self.charging and self.on_ground():
            self.image = pygame.transform.flip(self.idle_images[0], self.left, False)

        if key_press[pygame.K_SPACE] and self.in_ground:
            if self.hold_keys[pygame.K_SPACE][1] < setting.maximum_secs_for_jump * setting.frame_rate:
                self.hold_keys[pygame.K_SPACE][1] += 1

            self.charging = True
            self.image = pygame.transform.flip(self.jump_images[0], self.left, False)
        # print(f'{self.hold_keys[pygame.K_SPACE][1]=} {self.hold_keys[pygame.K_SPACE][0]=}')
        if key_press[pygame.K_a] and self.in_ground and self.on_ground():
            self.hold_keys[pygame.K_a][1] += 1
            self.left = True
            self.right = False

            collide_wall = self.hit_wall()
            if not self.charging and not collide_wall:
                self.rect.x -= self.speed

                self.moving_animation()
            elif not self.charging and collide_wall:
                self.image = pygame.transform.flip(self.idle_images[0], self.left, False)

        if key_press[pygame.K_d] and self.in_ground and self.on_ground():
            self.hold_keys[pygame.K_d][1] += 1
            self.left = False
            self.right = True

            collide_wall = self.hit_wall()
            if not self.charging and not collide_wall:
                self.rect.x += self.speed

                self.moving_animation()
            elif not self.charging and collide_wall:
                self.image = pygame.transform.flip(self.idle_images[0], self.left, False)

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
                    height = (hold_key[0] / setting.frame_rate) / setting.maximum_secs_for_jump * self.jump_h
                    # print(f'{height=}')
                    if height > self.jump_h:
                        height = self.jump_h
                    # print("\n\n\n")
                    # print(f"jump ({direction=} {height=})")  # DEBUG
                    pygame.mixer.Sound.play(self.jump_sound)
                    pygame.mixer.music.stop()
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
            if self.parabola != None:
                self.parabola.starting_point_y = self.parabola.get_current_y()
                self.parabola.ori_y = self.rect.y
            if self.exponential != None:
                self.exponential.starting_point_y = self.exponential.get_current_y()
                self.exponential.ori_y = self.rect.y
            print(f'Changed map: {global_var.stage_no}')
            global_var.stage_map = map_setting.Map(global_var.stage_no)


    def move_position(self, x, y, direction):
        if round(y) > self.rect.y:
            add = 1
        elif round(y) < self.rect.y:
            add = -1
        else:
            add = 0

        while True:

            rangeX = range(self.rect.left + direction + 1, self.rect.right + direction - 1)
            # print(f'{self.rect.x=} {self.rect.y=} {self.rect.left=} {self.rect.right=} {direction=}')
            rangeY = range(self.rect.top + add + 1, self.rect.bottom + add - 1)
            # print(f'{rangeX[0]=} {rangeY[0]=} {rangeX[-1]=} {rangeY[-1]=}')
            # print(f'{self.rect.x=} {self.rect.y=} {round(x)=} {round(y)=}')
            # print(f'{self.rect.bottom=} {rangeY[-1]=}')
            if self.rect.x == round(x) and self.rect.y == round(y):
                break

            if direction == 1:
                right = 1
                left = 0
            elif direction == -1:
                left = 1
                right = 0
            else:
                left = 0
                right = 0

            if add == 1:
                top = 0
                bottom = 1
            elif add == -1:
                top = 1
                bottom = 0
            else:
                top = 0
                bottom = 0

            # print(f'{top=} {bottom=} {left=} {right=}')
            top_hit, bottom_hit, left_hit, right_hit = self.detect_next(rangeX, rangeY, top, bottom, left, right)
            # print(f'{top_hit=} {bottom_hit=} {left_hit=} {right_hit=}')

            if left_hit != right_hit:
                pygame.mixer.Sound.play(self.hit_wall_sound)
                pygame.mixer.music.stop()
                difference = abs(self.rect.x - round(x))
                if self.parabola != None:
                    self.parabola.current_x -= difference * direction
                    self.parabola.change_direction(self.rect.x, self.rect.y)
                if self.exponential != None:
                    # print(f'Before: {self.rect.x=} {self.rect.y=}')
                    self.exponential.change_direction(self.rect.x)
                    # print(f'After: {self.rect.x=} {self.rect.y=}')
                self.image = pygame.transform.flip(self.jump_images[3], self.left, False)
                self.right = not self.right
                self.left = not self.left
                break

            if top_hit:
                pygame.mixer.Sound.play(self.hit_wall_sound)
                pygame.mixer.music.stop()
                if self.parabola != None:
                    self.parabola.current_x *= -1
                    self.parabola.ori_x = self.rect.x
                    self.parabola.starting_point_x = self.parabola.current_x
                break

            elif bottom_hit:
                self.in_ground = bottom_hit
                self.parabola = None
                self.exponential = None

                if self.drop_height >= setting.drop_png_height:
                    pygame.mixer.Sound.play(self.drop_sound)
                    pygame.mixer.music.stop()
                    self.image = pygame.transform.flip(self.drop_images[0], self.right, False)
                    self.drop_freeze = True
                else:
                    pygame.mixer.Sound.play(self.land_sound)
                    pygame.mixer.music.stop()

                self.drop_height = 0
                self.jumpCount = 0
                self.jumped = True
                self.dropping = False
                break

            # print(f'{direction=} {add=}')
            if self.rect.x != round(x):
                self.rect.x += direction
            if self.rect.y != round(y) and not bottom_hit:
                self.rect.y += add


        # print(f'Then {self.rect.x=} {self.rect.y=}')

    def moving_animation(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.frame_rate:
            self.move_frame += 1
            frame = self.move_frame % len(self.move_images)
            self.image = pygame.transform.flip(self.move_images[frame], self.left, False)
            self.last_update = now

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
        # print(f'hit wall {self.rect.x=} {self.rect.y=}')
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

    def detect_next(self, x_range, y_range, xtop, xbottom, yleft, yright):
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
            y_coor = y_range[0] - 1

            for x_coor in x_range:
                if y_coor < min_y or y_coor >= max_y:
                    top_hit = False
                    break
                if x_coor >= max_x or x_coor < min_x:
                    # top_hit = True
                    # break
                    continue
                if map_data[y_coor][x_coor] == 'X':

                    top_hit = True
                    break

        elif xbottom == 1:
            y_coor = y_range[-1] + 1
            for x_coor in x_range:
                if y_coor < min_y or y_coor >= max_y:
                    bottom_hit = False
                    break
                if x_coor >= max_x or x_coor < min_x:
                    #bottom_hit = True
                    #break
                    continue
                if map_data[y_coor][x_coor] == 'X':
                    bottom_hit = True
                    break

        # if yleft == 1:
        x_coor = x_range[0]
        if x_coor <= min_x:
            left_hit = True
        else:
            for y_coor in y_range:
                if y_coor >= max_y or y_coor < min_y:
                    #left_hit = True
                    #break
                    continue
                if map_data[y_coor][x_coor] == 'X':
                    left_hit = True
                    break
        # elif yright == 1:
        x_coor = x_range[-1]
        if x_coor >= max_x-1:
            right_hit = True
        else:
            for y_coor in y_range:
                if y_coor >= max_y or y_coor < min_y:
                    #right_hit = True
                    #break
                    continue
                if map_data[y_coor][x_coor] == 'X':
                    right_hit = True
                    break

        return top_hit, bottom_hit, left_hit, right_hit

    def on_ground(self):
        max_y = setting.screen_size[1]
        min_y = 0
        map_data = global_var.stage_map.get_map_data()
        y = self.rect.bottom + 1
        if y < min_y or y > max_y:
            return False
        for x in range(self.rect.left+1, self.rect.right-1):
            if map_data[y][x] == 'X':
                return True
        return False