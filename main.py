import pygame

import os

import setting
import king
import map_setting
import global_var
import start_menu
import main_menu


def main():

    # Init
    pygame.init()

    clock = pygame.time.Clock()
    pygame.event.set_allowed([pygame.K_a, pygame.K_d, pygame.K_SPACE, pygame.QUIT])
    pygame.display.set_caption(global_var.GAME_TITLE)

    # Create Screen
    game_screen = pygame.display.set_mode(setting.screen_size)
    game_screen.set_alpha(None)

    # Start Menu
    press_start = start_menu.PressStart()
    logo = start_menu.Logo()
    start_menu_start = True
    pygame.mixer.init()
    pygame.mixer.music.set_volume(setting.default_volume)
    pygame.mixer.music.load(setting.background_music1_path)
    pygame.mixer.music.play()
    while start_menu_start:
        clock.tick(setting.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN and logo.completed:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.Sound.play(press_start.click_sound)
                    press_start.clicked = True
        game_screen.fill((0, 0, 0))
        logo.update()
        game_screen.blit(logo.image, logo.rect)
        if logo.completed:
            press_start.update()
            if press_start.show:
                game_screen.blit(press_start.image, press_start.rect)
        if press_start.complete:
            press_start.image = press_start.image.fill((0, 0, 0, 0))
            start_menu_start = False

        pygame.display.flip()

    # press_start.kill()
    press_start.image = press_start.image.fill((0, 0, 0, 0))
    # Main Menu
    main_menu_screen(clock, game_screen)
    main_menu_enter = True
    while main_menu_enter:
        clock.tick(setting.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()



        pygame.display.flip()


    pygame.mixer.music.stop()
    logo.kill()
    # Create Character
    king_player = king.MainCharacter(500, 865, setting.character_size, setting.maximum_height, setting.walking_speed)

    # Create Environment
    global_var.stage_map = map_setting.Map(global_var.stage_no)
    king_player.init_location()
    # environment_objects = pygame.sprite.Group()
    player = pygame.sprite.Group()
    # environment_objects.add(king_player)
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

def main_menu_screen(clock, screen):
    menu_box1 = main_menu.Box(300, 700, (200, 600))
    screen.blit(menu_box1.image, menu_box1.rect)
    size = menu_box1.image.get_size()

    seperate = size[1] // len(setting.options)
    starting_point = menu_box1.rect.y + seperate // 2 - 50

    font = global_var.font1
    for option_index, option in enumerate(setting.options):
        text = font.render(option, True, (255, 255, 255))
        screen.blit(text, (size[0] // 4 + menu_box1.rect.x, seperate * option_index + starting_point))


if __name__ == '__main__':
    main()

