import pygame
import os

import setting

class MainCharacter(pygame.sprite.Sprite):
    def __init__(self, x, y, size, jump_h, walk_s):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.idle_img_index = -1
        for file_index, file in enumerate(os.listdir(setting.character_images_path)):
            img = pygame.image.load(os.path.join(setting.character_images_path, file)).convert()
            img = pygame.transform.scale(img, (size[0], size[1]))
            img.convert_alpha()
            img.set_colorkey((0, 0, 0))
            self.images.append(img)
            if file == setting.idle_img_name:
                self.idle_img_index = file_index

        self.image = self.images[self.idle_img_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = walk_s
        self.jump = jump_h

        self.direction = 'right'

    def update(self):
        key_press = pygame.key.get_pressed()
        if key_press[pygame.K_a]:
            self.rect.x -= self.speed
            if self.direction != 'left':
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction = 'left'
        if key_press[pygame.K_d]:
            self.rect.x += self.speed
            if self.direction != 'right':
                self.image = pygame.transform.flip(self.image, True, False)
                self.direction = 'right'



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

