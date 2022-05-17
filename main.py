import pygame
import os

import setting
import king
import map_setting
import global_var



def main():

    # Init
    pygame.init()
    clock = pygame.time.Clock()

    pygame.display.set_caption(global_var.GAME_TITLE)

    # Create Screen
    game_screen = pygame.display.set_mode(setting.screen_size)

    # Create Character
    king_player = king.MainCharacter(500, 865, setting.character_size, setting.jumping_height, setting.walking_speed)

    # Create Environment

    #backdrop = pygame.transform.scale(backdrop, (1200, 1000))


    global_var.stage_map = map_setting.Map(global_var.stage_no)
    environment_objects = pygame.sprite.Group()
    player = pygame.sprite.Group()
    environment_objects.add(king_player)
    player.add(king_player)

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

        backdrop = pygame.image.load(os.path.join(setting.stage_images_path, f"{global_var.stage_no}.png"))
        backdropbox = game_screen.get_rect()

        game_screen.blit(backdrop, backdropbox)
        player.draw(game_screen)
        pygame.display.flip()



    # End
    pygame.quit()


if __name__ == '__main__':
    main()

