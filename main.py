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
            img = pygame.transform.scale(img, (50, 70))
            img.convert_alpha()
            img.set_colorkey((0, 255, 0))
            self.images.append(img)
            if file == setting.idle_img_name:
                self.idle_img_index = file_index

        self.image = self.images[self.idle_img_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def main():

    #Init
    pygame.init()

    #Create Screen
    game_screen = pygame.display.set_mode(setting.screen_size)

    # Create Character
    king = MainCharacter(450, 850, setting.character_size, setting.jumping_height, setting.walking_speed)

    # Create Environment
    backdrop = pygame.image.load(os.path.join(setting.stage_images_path, "Stage1-1.png"))
    backdrop = pygame.transform.scale(backdrop, (1000, 1000))
    backdropbox = game_screen.get_rect()
    player = pygame.sprite.Group()
    player.add(king)

    game_started = True
    while game_started:

        # Close Window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_started = False

        # Background
        game_screen.fill((0, 0, 0))

        game_screen.blit(backdrop, backdropbox)
        player.draw(game_screen)
        pygame.display.flip()



    # End
    pygame.quit()


if __name__ == '__main__':
    main()

