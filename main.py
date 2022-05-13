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


    def update(self):
        key_press = pygame.key.get_pressed()

        if not self.in_ground:
            # TODO: jumping, find next position
            pass

        if not self.moving and self.in_ground and not self.charging:
            self.image = pygame.transform.flip(self.idle_images[0], self.left, False)


        if key_press[pygame.K_SPACE] and self.in_ground:
            self.hold_keys[pygame.K_SPACE][1] += 1
            self.charging = True
            self.image = pygame.transform.flip(self.drop_images[0], self.left, False)

        if key_press[pygame.K_a] and self.in_ground:
            self.hold_keys[pygame.K_a][1] += 1
            self.left = True
            self.right = False
            if not self.charging:
                self.moving = True
                self.rect.x -= self.speed

                # next frame
                self.move_frame = (self.move_frame + 1) % len(self.move_images)

                self.moving_animation()
                self.moving = False

        if key_press[pygame.K_d] and self.in_ground:
            self.hold_keys[pygame.K_d][1] += 1
            self.left = False
            self.right = True
            if not self.charging:
                self.moving = True
                self.rect.x += self.speed

                # next frame
                self.move_frame = (self.move_frame + 1) % len(self.move_images)

                self.moving_animation()
                self.moving = False


        print(self.hold_keys) #DEBUG
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

                    print("jump (direction: " + str(direction) + ", holding time: " + str(hold_key[0]) + ")") #DEBUG

                    self.charging = False

                    # TODO
                    # self.in_ground = False

                # didn't press anymore, so reset it
                self.hold_keys[key] = [0, 0]
            else:
                # pressing, update it
                hold_key[0] = hold_key[1]
        



    def moving_animation(self):
        self.image = pygame.transform.flip(self.move_images[self.move_frame], self.left, False)




def main():

    # Init
    pygame.init()
    clock = pygame.time.Clock()

    # Create Screen
    game_screen = pygame.display.set_mode(setting.screen_size)

    # Create Character
    king = MainCharacter(500, 875, setting.character_size, setting.jumping_height, setting.walking_speed)

    # Create Environment
    backdrop = pygame.image.load(os.path.join(setting.stage_images_path, "Stage1-1.png"))
    backdrop = pygame.transform.scale(backdrop, (1000, 1000))
    backdropbox = game_screen.get_rect()

    environment_objects = pygame.sprite.Group()
    player = pygame.sprite.Group()
    environment_objects.add(king)
    player.add(king)

    game_started = True
    while game_started:
        clock.tick(setting.FPS)

        # Close Window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_started = False

        # Update
        player.update()


        # Background
        game_screen.fill((0, 0, 0))

        game_screen.blit(backdrop, backdropbox)
        player.draw(game_screen)
        pygame.display.flip()



    # End
    pygame.quit()


if __name__ == '__main__':
    main()

