import pygame
import os

import setting

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, size, jump_h, walk_s):
        pygame.sprite.Sprite.__init__(self)
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


    def update(self):
        key_press = pygame.key.get_pressed()

        if not self.moving:
            self.image = self.idle_images[0]
            if self.left:
                self.image = pygame.transform.flip(self.image, True, False)


        if key_press[pygame.K_a]:
            self.moving = True
            self.rect.x -= self.speed

            self.move_frame = self.move_frame + 1
            if self.move_frame >= len(self.move_images):
                self.move_frame = 0
            self.moving_animation()
            if self.right:
                #self.image = pygame.transform.flip(self.image, True, False)
                self.left = True
                self.right = False
            self.moving = False

        if key_press[pygame.K_d]:
            self.moving = True
            self.rect.x += self.speed

            self.move_frame = self.move_frame + 1
            if self.move_frame >= len(self.move_images):
                self.move_frame = 0
            self.moving_animation()
            if self.left:
                #self.image = pygame.transform.flip(self.image, True, False)
                self.left = False
                self.right = True
            self.moving = False



    def moving_animation(self):
        self.image = self.move_images[self.move_frame]
        if self.left:
            self.image = pygame.transform.flip(self.image, True, False)




def main():

    #Init
    pygame.init()
    clock = pygame.time.Clock()

    #Create Screen
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

