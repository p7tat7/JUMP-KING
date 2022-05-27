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
    pygame.event.set_allowed([pygame.K_a, pygame.K_d, pygame.K_SPACE, pygame.QUIT])
    pygame.display.set_caption(global_var.GAME_TITLE)


    # Create Screen
    game_screen = pygame.display.set_mode(setting.screen_size)
    game_screen.set_alpha(None)

    # Create Character
    king_player = king.MainCharacter(500, 865, setting.character_size, setting.maximum_height, setting.walking_speed)

    # Create Environment

    #backdrop = pygame.transform.scale(backdrop, (1200, 1000))


    global_var.stage_map = map_setting.Map(global_var.stage_no)
    king_player.init_location()
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
        backdropbox = game_screen.get_rect()

        game_screen.blit(global_var.background, backdropbox)
        game_screen.blit(global_var.backdrop, backdropbox)
        player.draw(game_screen)
        game_screen.blit(global_var.foreground, backdropbox)

        pygame.display.flip()

    # End
    pygame.quit()

def update_map():
    global_var.background = pygame.image.load(os.path.join(setting.background_path, f"bg{global_var.stage_no}.png"))
    global_var.background = pygame.transform.scale(global_var.background, setting.screen_size)
    global_var.backdrop = pygame.image.load(os.path.join(setting.stage_images_path, f"{global_var.stage_no}.png"))
    global_var.foreground = pygame.image.load(os.path.join(setting.foreground_path, f"fg{global_var.stage_no}.png"))
    global_var.foreground = pygame.transform.scale(global_var.foreground, setting.screen_size)

if __name__ == '__main__':
    main()

